"""
articles/serializers.py - Make sure this matches exactly
The issue might be that ArticleCreateUpdateSerializer doesn't return the ID
"""
from rest_framework import serializers
from django.utils.text import slugify
from .models import Category, Article
from accounts.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    articles_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'articles_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']
    
    def get_articles_count(self, obj):
        return obj.articles.filter(status='published').count()
    
    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['name'])
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if 'name' in validated_data:
            validated_data['slug'] = slugify(validated_data['name'])
        return super().update(instance, validated_data)

class ArticleListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'description', 'category', 'author', 'status', 'featured_image', 'views_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'slug', 'author', 'views_count', 'created_at', 'updated_at']

class ArticleDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'description', 'content', 'category', 'author', 'status', 'featured_image', 'views_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'slug', 'author', 'views_count', 'created_at', 'updated_at']

class ArticleCreateUpdateSerializer(serializers.ModelSerializer):
    # CRITICAL: Add id to fields so it's returned in response
    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'description', 'content', 'category', 'status', 'featured_image']
        read_only_fields = ['id', 'slug']  # Make sure id and slug are read-only
    
    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['title'])
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if 'title' in validated_data:
            validated_data['slug'] = slugify(validated_data['title'])
        return super().update(instance, validated_data)
    
    def validate_category(self, value):
        if not value:
            raise serializers.ValidationError("Category is required.")
        return value

    def to_representation(self, instance):
        """
        Override to return full representation after create/update
        This ensures the response includes all fields including the ID
        """
        representation = super().to_representation(instance)
        # Ensure id is always in the response
        representation['id'] = instance.id
        return representation