"""
scraper/scraper.py
"""
import requests
from bs4 import BeautifulSoup
from scraper.models import ScrapedArticle


class ArticleScraper:
    """
    Web scraper to fetch latest articles from various sources
    """
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_dev_to(self, limit=5):
        """
        Scrape latest articles from dev.to
        """
        articles = []
        try:
            url = 'https://dev.to'
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            article_elements = soup.find_all('article', class_='crayons-story', limit=limit)
            
            for article in article_elements:
                try:
                    title_elem = article.find('h2', class_='crayons-story__title') or article.find('h3', class_='crayons-story__title')
                    link_elem = title_elem.find('a') if title_elem else None
                    
                    if link_elem and link_elem.get('href'):
                        title = link_elem.text.strip()
                        article_url = f"https://dev.to{link_elem['href']}"
                        
                        # Save to database
                        scraped_article, created = ScrapedArticle.objects.get_or_create(
                            url=article_url,
                            defaults={
                                'title': title,
                                'source': 'dev.to'
                            }
                        )
                        
                        articles.append({
                            'title': title,
                            'url': article_url,
                            'source': 'dev.to',
                            'is_new': created
                        })
                except Exception as e:
                    print(f"Error parsing article: {str(e)}")
                    continue
            
        except Exception as e:
            print(f"Error scraping dev.to: {str(e)}")
        
        return articles
    
    def scrape_hackernews(self, limit=5):
        """
        Scrape latest articles from Hacker News
        """
        articles = []
        try:
            url = 'https://news.ycombinator.com/'
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            storylinks = soup.find_all('span', class_='titleline', limit=limit)
            
            for story in storylinks:
                try:
                    link_elem = story.find('a')
                    
                    if link_elem:
                        title = link_elem.text.strip()
                        article_url = link_elem.get('href', '')
                        
                        if not article_url.startswith('http'):
                            article_url = f"https://news.ycombinator.com/{article_url}"
                        
                        # Save to database
                        scraped_article, created = ScrapedArticle.objects.get_or_create(
                            url=article_url,
                            defaults={
                                'title': title,
                                'source': 'Hacker News'
                            }
                        )
                        
                        articles.append({
                            'title': title,
                            'url': article_url,
                            'source': 'Hacker News',
                            'is_new': created
                        })
                except Exception as e:
                    print(f"Error parsing article: {str(e)}")
                    continue
            
        except Exception as e:
            print(f"Error scraping Hacker News: {str(e)}")
        
        return articles
    
    def scrape_all(self, limit=5):
        """
        Scrape articles from all sources
        """
        all_articles = []
        
        all_articles.extend(self.scrape_hackernews(limit))
        all_articles.extend(self.scrape_dev_to(limit))
        
        return all_articles[:limit]