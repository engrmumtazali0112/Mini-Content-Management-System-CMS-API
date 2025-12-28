"""
articles/urls.py
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .views import ArticleViewSet, CategoryViewSet

# Create router for viewsets
router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'categories', CategoryViewSet, basename='category')

@api_view(['GET'])
def api_root(request, format=None):
    """
    API root view showing all available endpoints
    """
    return Response({
        'articles': reverse('article-list', request=request, format=format),
        'categories': reverse('category-list', request=request, format=format),
        'my_articles': request.build_absolute_uri('/api/articles/my_articles/'),
        'drafts': request.build_absolute_uri('/api/articles/drafts/'),
        'published': request.build_absolute_uri('/api/articles/published/'),
    })

urlpatterns = [
    path('', api_root, name='api-root'),
    path('', include(router.urls)),
]