"""
accounts/management/commands/create_sample_data.py

Create this file structure:
accounts/
  management/
    __init__.py
    commands/
      __init__.py
      create_sample_data.py  <-- This file
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from articles.models import Category, Article
from django.utils.text import slugify

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample data for testing'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('Creating sample data for Mini CMS...'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        
        # Create users
        self.stdout.write('\n[1] Creating Users...')
        self.stdout.write('-' * 70)
        
        # Admin user
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'role': 'admin',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Created admin user: {admin.username}'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠ Admin user already exists: {admin.username}'))
        
        # Author 1
        author1, created = User.objects.get_or_create(
            username='john_doe',
            defaults={
                'email': 'john@example.com',
                'role': 'author',
                'first_name': 'John',
                'last_name': 'Doe'
            }
        )
        if created:
            author1.set_password('author123')
            author1.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Created author user: {author1.username}'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠ Author user already exists: {author1.username}'))
        
        # Author 2
        author2, created = User.objects.get_or_create(
            username='jane_smith',
            defaults={
                'email': 'jane@example.com',
                'role': 'author',
                'first_name': 'Jane',
                'last_name': 'Smith'
            }
        )
        if created:
            author2.set_password('author123')
            author2.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Created author user: {author2.username}'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠ Author user already exists: {author2.username}'))
        
        # Create categories
        self.stdout.write('\n[2] Creating Categories...')
        self.stdout.write('-' * 70)
        
        categories_data = [
            {'name': 'Technology', 'description': 'Articles about technology and innovation'},
            {'name': 'Programming', 'description': 'Programming tutorials and tips'},
            {'name': 'Web Development', 'description': 'Web development articles'},
            {'name': 'Data Science', 'description': 'Data science and machine learning'},
            {'name': 'DevOps', 'description': 'DevOps and infrastructure articles'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'description': cat_data['description']
                }
            )
            categories.append(category)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created category: {category.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ Category already exists: {category.name}'))
        
        # Create articles
        self.stdout.write('\n[3] Creating Articles...')
        self.stdout.write('-' * 70)
        
        articles_data = [
            {
                'title': 'Introduction to Django REST Framework',
                'description': 'Learn the basics of Django REST Framework',
                'content': 'Django REST Framework is a powerful toolkit for building Web APIs. It provides features like serialization, authentication, and viewsets that make API development easier and more maintainable. In this article, we will explore the core concepts and best practices.',
                'category': categories[1],
                'author': author1,
                'status': 'published'
            },
            {
                'title': 'Building Scalable APIs with Django',
                'description': 'Best practices for building scalable APIs',
                'content': 'When building APIs at scale, there are several considerations including caching strategies, database optimization techniques, proper error handling, and implementing rate limiting. This comprehensive guide covers all essential aspects of building production-ready APIs.',
                'category': categories[2],
                'author': author1,
                'status': 'published'
            },
            {
                'title': 'PostgreSQL Performance Optimization',
                'description': 'Tips for optimizing PostgreSQL queries',
                'content': 'PostgreSQL is a powerful database, but it needs proper optimization through indexing strategies, query planning, connection pooling, and understanding EXPLAIN ANALYZE. Learn how to identify bottlenecks and improve your database performance significantly.',
                'category': categories[0],
                'author': author2,
                'status': 'published'
            },
            {
                'title': 'My Draft Article',
                'description': 'This is a draft article',
                'content': 'Draft content that is not yet published. This article is still being written and reviewed before publication.',
                'category': categories[1],
                'author': author1,
                'status': 'draft'
            },
            {
                'title': 'Machine Learning Basics',
                'description': 'Introduction to machine learning concepts',
                'content': 'Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. This article covers supervised learning, unsupervised learning, and neural networks basics.',
                'category': categories[3],
                'author': author2,
                'status': 'published'
            },
            {
                'title': 'Docker and Kubernetes Guide',
                'description': 'Containerization with Docker and Kubernetes',
                'content': 'Docker and Kubernetes are essential tools for modern DevOps practices. Learn how to containerize your applications, manage deployments, and orchestrate containers at scale. This guide includes practical examples and best practices.',
                'category': categories[4],
                'author': author1,
                'status': 'published'
            },
        ]
        
        for article_data in articles_data:
            article, created = Article.objects.get_or_create(
                title=article_data['title'],
                defaults={
                    'slug': slugify(article_data['title']),
                    'description': article_data['description'],
                    'content': article_data['content'],
                    'category': article_data['category'],
                    'author': article_data['author'],
                    'status': article_data['status']
                }
            )
            if created:
                status_icon = '📝' if article.status == 'draft' else '✓'
                self.stdout.write(self.style.SUCCESS(f'{status_icon} Created article: {article.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ Article already exists: {article.title}'))
        
        # Summary
        self.stdout.write('\n' + '=' * 70)
        self.stdout.write(self.style.SUCCESS('SAMPLE DATA CREATION COMPLETED!'))
        self.stdout.write('=' * 70)
        
        total_users = User.objects.count()
        total_categories = Category.objects.count()
        total_articles = Article.objects.count()
        published = Article.objects.filter(status='published').count()
        drafts = Article.objects.filter(status='draft').count()
        
        self.stdout.write(f'\nDatabase Summary:')
        self.stdout.write(f'  • Users: {total_users}')
        self.stdout.write(f'  • Categories: {total_categories}')
        self.stdout.write(f'  • Articles: {total_articles} (Published: {published}, Drafts: {drafts})')
        
        self.stdout.write('\n' + '=' * 70)
        self.stdout.write('LOGIN CREDENTIALS:')
        self.stdout.write('=' * 70)
        self.stdout.write(self.style.SUCCESS('\nAdmin User:'))
        self.stdout.write('  Username: admin')
        self.stdout.write('  Password: admin123')
        self.stdout.write('  Role: admin')
        self.stdout.write('  Access: Full system access')
        
        self.stdout.write(self.style.SUCCESS('\nAuthor User 1:'))
        self.stdout.write('  Username: john_doe')
        self.stdout.write('  Password: author123')
        self.stdout.write('  Role: author')
        self.stdout.write('  Access: Can manage own articles')
        
        self.stdout.write(self.style.SUCCESS('\nAuthor User 2:'))
        self.stdout.write('  Username: jane_smith')
        self.stdout.write('  Password: author123')
        self.stdout.write('  Role: author')
        self.stdout.write('  Access: Can manage own articles')
        
        self.stdout.write('\n' + '=' * 70)
        self.stdout.write(self.style.SUCCESS('Next Steps:'))
        self.stdout.write('  1. Start server: python manage.py runserver 127.0.0.1:1223')
        self.stdout.write('  2. Run tests: python test_api_complete.py')
        self.stdout.write('  3. View Swagger: http://127.0.0.1:1223/swagger/')
        self.stdout.write('  4. Login at: http://127.0.0.1:1223/api/auth/login/')
        self.stdout.write('=' * 70 + '\n')