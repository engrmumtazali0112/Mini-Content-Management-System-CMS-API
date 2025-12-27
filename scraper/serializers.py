"""
scraper/serializers.py
"""
from rest_framework import serializers
from scraper.models import ScrapedArticle


class ScrapedArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapedArticle
        fields = ['id', 'title', 'url', 'source', 'scraped_at']
        read_only_fields = ['id', 'scraped_at']