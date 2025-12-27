"""
scraper/views.py
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny

from scraper.models import ScrapedArticle
from scraper.serializers import ScrapedArticleSerializer
from scraper.scraper import ArticleScraper


class ScrapedArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing scraped articles
    Only admins can trigger scraping
    """
    queryset = ScrapedArticle.objects.all()
    serializer_class = ScrapedArticleSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
    def scrape(self, request):
        """
        Trigger scraping of articles (Admin only)
        """
        limit = request.data.get('limit', 5)
        
        try:
            scraper = ArticleScraper()
            articles = scraper.scrape_all(limit=limit)
            
            return Response({
                'message': 'Scraping completed successfully',
                'articles_scraped': len(articles),
                'articles': articles
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'error': f'Scraping failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """
        Get latest scraped articles
        """
        limit = request.query_params.get('limit', 10)
        articles = ScrapedArticle.objects.all()[:int(limit)]
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)