
"""
articles/filters.py
"""
from django_filters import rest_framework as filters
from .models import Article

class ArticleFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    category = filters.NumberFilter(field_name='category__id')
    author = filters.NumberFilter(field_name='author__id')
    status = filters.ChoiceFilter(choices=Article.STATUS_CHOICES)
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = Article
        fields = ['title', 'category', 'author', 'status']


