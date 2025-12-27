"""
scraper/admin.py
"""
from django.contrib import admin
from scraper.models import ScrapedArticle


@admin.register(ScrapedArticle)
class ScrapedArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'source', 'scraped_at']
    list_filter = ['source', 'scraped_at']
    search_fields = ['title', 'url']
    readonly_fields = ['scraped_at']