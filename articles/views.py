"""
articles/views.py - COMPLETE FIX
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch, Q
from .models import Category, Article
from .serializers import (
    CategorySerializer, ArticleListSerializer, 
    ArticleDetailSerializer, ArticleCreateUpdateSerializer
)
from .permissions import IsAdminOrReadOnly, IsAuthorOrAdmin
from .filters import ArticleFilter
from .pagination import ArticlePagination

class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing categories.
    Only admins can create, update, or delete categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        """
        Optimize query by prefetching related articles
        """
        return Category.objects.prefetch_related(
            Prefetch('articles', queryset=Article.objects.filter(status='published'))
        )

class ArticleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing articles.
    - Public users can only view published articles
    - Authors can create and edit their own articles (any status)
    - Admins can edit any article
    
    CRITICAL FIX: Authors must be able to access their own articles regardless of status.
    """
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ArticleFilter
    search_fields = ['title', 'description', 'content']
    ordering_fields = ['created_at', 'updated_at', 'views_count', 'title']
    ordering = ['-created_at']
    pagination_class = ArticlePagination
    
    def get_queryset(self):
        """
        SIMPLIFIED FILTERING LOGIC:
        
        1. Unauthenticated users → Only published articles
        2. Admin users → All articles
        3. Authors → Their own articles (ANY status) + published articles by others
        
        This applies to ALL actions (list, retrieve, update, delete).
        """
        queryset = Article.objects.select_related('author', 'category')
        user = self.request.user
        
        # Case 1: Unauthenticated users
        if not user.is_authenticated:
            return queryset.filter(status='published')
        
        # Case 2: Admin users
        if user.is_admin:
            return queryset
        
        # Case 3: Regular authenticated users (authors)
        # They can access:
        # - All their own articles (draft or published)
        # - Published articles by other authors
        return queryset.filter(Q(author=user) | Q(status='published')).distinct()
    
    def get_serializer_class(self):
        """
        Use different serializers for different actions
        """
        if self.action == 'retrieve':
            return ArticleDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ArticleCreateUpdateSerializer
        return ArticleListSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve single article and increment view count
        """
        instance = self.get_object()
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        """
        Set the author to the current user
        """
        serializer.save(author=self.request.user)
    
    def perform_update(self, serializer):
        """
        Ensure authors can only update their own articles
        (Permission is already checked by IsAuthorOrAdmin)
        """
        serializer.save()
    
    def perform_destroy(self, instance):
        """
        Ensure authors can only delete their own articles
        (Permission is already checked by IsAuthorOrAdmin)
        """
        instance.delete()
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_articles(self, request):
        """
        Get all articles by the current user (both draft and published)
        """
        queryset = self.get_queryset().filter(author=request.user)
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def published(self, request):
        """
        Get all published articles (public endpoint)
        """
        queryset = self.get_queryset().filter(status='published')
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def drafts(self, request):
        """
        Get draft articles
        - Authors: see only their own drafts
        - Admins: see all drafts
        - Unauthenticated: 401 error
        """
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if request.user.is_admin:
            queryset = self.get_queryset().filter(status='draft')
        else:
            queryset = self.get_queryset().filter(status='draft', author=request.user)
        
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)