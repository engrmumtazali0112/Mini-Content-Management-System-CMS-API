"""
scraper/models.py - FIXED VERSION
"""
from django.db import models


class ScrapedArticle(models.Model):
    title = models.CharField(max_length=500)
    url = models.URLField(max_length=1000, unique=True)
    source = models.CharField(max_length=255)
    scraped_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # REMOVE OR COMMENT THIS LINE - Let Django use default table name
        # db_table = 'scraped_articles'
        ordering = ['-scraped_at']
    
    def __str__(self):
        return self.title