"""
scraper/urls.py
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from scraper.views import ScrapedArticleViewSet

router = DefaultRouter()
router.register(r'articles', ScrapedArticleViewSet, basename='scraped-article')

urlpatterns = [
    path('', include(router.urls)),
]