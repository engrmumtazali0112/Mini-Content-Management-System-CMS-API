"""
articles/tests.py
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Category, Article

User = get_user_model()

class CategoryTests(TestCase):
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
    
    def test_list_categories_public(self):
        """Test that anyone can list categories"""
        Category.objects.create(name='Technology', slug='technology')
        
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_category_admin(self):
        """Test that admin can create category"""
        self.client.force_authenticate(user=self.admin)
        
        response = self.client.post('/api/categories/', {
            'name': 'Programming',
            'description': 'Programming articles'
        })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
    
    def test_create_category_author_forbidden(self):
        """Test that author cannot create category"""
        self.client.force_authenticate(user=self.author)
        
        response = self.client.post('/api/categories/', {
            'name': 'Programming',
            'description': 'Programming articles'
        })
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ArticleTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            role='admin'
        )
        self.author1 = User.objects.create_user(
            username='author1',
            email='author1@example.com',
            password='author123',
            role='author'
        )
        self.author2 = User.objects.create_user(
            username='author2',
            email='author2@example.com',
            password='author123',
            role='author'
        )
        self.category = Category.objects.create(
            name='Technology',
            slug='technology'
        )
    
    def test_list_published_articles_public(self):
        """Test that public users see only published articles"""
        Article.objects.create(
            title='Published Article',
            slug='published-article',
            description='Test',
            content='Content',
            category=self.category,
            author=self.author1,
            status='published'
        )
        Article.objects.create(
            title='Draft Article',
            slug='draft-article',
            description='Test',
            content='Content',
            category=self.category,
            author=self.author1,
            status='draft'
        )
        
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_create_article_authenticated(self):
        """Test that authenticated user can create article"""
        self.client.force_authenticate(user=self.author1)
        
        response = self.client.post('/api/articles/', {
            'title': 'New Article',
            'description': 'Description',
            'content': 'Content',
            'category': self.category.id,
            'status': 'draft'
        })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.get().author, self.author1)
    
    def test_update_own_article(self):
        """Test that author can update their own article"""
        article = Article.objects.create(
            title='My Article',
            slug='my-article',
            description='Test',
            content='Content',
            category=self.category,
            author=self.author1,
            status='draft'
        )
        
        self.client.force_authenticate(user=self.author1)
        
        response = self.client.put(f'/api/articles/{article.id}/', {
            'title': 'Updated Article',
            'description': 'Updated',
            'content': 'Updated content',
            'category': self.category.id,
            'status': 'published'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        article.refresh_from_db()
        self.assertEqual(article.title, 'Updated Article')
    
    def test_cannot_update_others_article(self):
        """Test that author cannot update another author's article"""
        article = Article.objects.create(
            title='Article',
            slug='article',
            description='Test',
            content='Content',
            category=self.category,
            author=self.author1,
            status='draft'
        )
        
        self.client.force_authenticate(user=self.author2)
        
        response = self.client.put(f'/api/articles/{article.id}/', {
            'title': 'Updated',
            'description': 'Updated',
            'content': 'Updated',
            'category': self.category.id,
            'status': 'published'
        })
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_admin_can_update_any_article(self):
        """Test that admin can update any article"""
        article = Article.objects.create(
            title='Article',
            slug='article',
            description='Test',
            content='Content',
            category=self.category,
            author=self.author1,
            status='draft'
        )
        
        self.client.force_authenticate(user=self.admin)
        
        response = self.client.put(f'/api/articles/{article.id}/', {
            'title': 'Admin Updated',
            'description': 'Updated',
            'content': 'Updated',
            'category': self.category.id,
            'status': 'published'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
