"""
scraper/tests.py
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import ScrapedArticle

User = get_user_model()

class ScraperTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            role='admin',
            is_staff=True
        )
        self.author = User.objects.create_user(
            username='author',
            email='author@example.com',
            password='author123',
            role='author'
        )
    
    def test_list_scraped_articles(self):
        """Test listing scraped articles"""
        ScrapedArticle.objects.create(
            title='Test Article',
            url='https://example.com/article',
            source='Example'
        )
        
        response = self.client.get('/api/scraper/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_trigger_scraping_admin(self):
        """Test that admin can trigger scraping"""
        self.client.force_authenticate(user=self.admin)
        
        response = self.client.post('/api/scraper/articles/scrape/', {
            'limit': 5
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_trigger_scraping_author_forbidden(self):
        """Test that author cannot trigger scraping"""
        self.client.force_authenticate(user=self.author)
        
        response = self.client.post('/api/scraper/articles/scrape/', {
            'limit': 5
        })
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)