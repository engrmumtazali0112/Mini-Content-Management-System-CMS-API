"""
articles/views.py
"""
from accounts.serializers import UserSerializer
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch
from .models import Category, Article
from articles.serializers import (
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
    - Authors can create and edit their own articles
    - Admins can edit any article
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
        Optimize queries and filter based on user permissions
        """
        queryset = Article.objects.select_related('author', 'category')
        
        user = self.request.user
        
        # Public users and non-authenticated users only see published articles
        if not user.is_authenticated:
            return queryset.filter(status='published')
        
        # Admins see all articles
        if user.is_admin:
            return queryset
        
        # Authors see their own articles (all statuses) and published articles by others
        if user.is_author:
            from django.db.models import Q
            return queryset.filter(Q(author=user) | Q(status='published'))
        
        # Default: only published articles
        return queryset.filter(status='published')
    
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
        """
        article = self.get_object()
        user = self.request.user
        
        if article.author != user and not user.is_admin:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only edit your own articles.")
        
        serializer.save()
    
    def perform_destroy(self, instance):
        """
        Ensure authors can only delete their own articles
        """
        user = self.request.user
        
        if instance.author != user and not user.is_admin:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only delete your own articles.")
        
        instance.delete()
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_articles(self, request):
        """
        Get all articles by the current user
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
        Get all published articles
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
        Get all draft articles (only for authenticated users)
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




