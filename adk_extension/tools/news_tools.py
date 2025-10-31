"""
News Research Tools
News API integration for market sentiment analysis
"""

import requests
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import logging
from config import NEWS_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsAPITools:
    """
    News API tools for market sentiment and news analysis
    """
    
    def __init__(self):
        self.api_key = NEWS_API_KEY
        self.base_url = "https://newsapi.org/v2"
        self.logger = logger
        
        if not self.api_key:
            self.logger.warning("⚠️ NEWS_API_KEY not found. News tools will not work.")
    
    def get_company_news(self, company_name: str, ticker: str, days_back: int = 7) -> Dict[str, Any]:
        """
        Fetch recent news articles about a company
        
        Args:
            company_name: Full company name (e.g., 'Tesla')
            ticker: Stock ticker (e.g., 'TSLA')
            days_back: Number of days to look back for news
            
        Returns:
            Dict containing news articles and analysis
        """
        try:
            if not self.api_key:
                return {"error": "NEWS_API_KEY not configured"}
            
            self.logger.info(f"Fetching news for {company_name} ({ticker})")
            
            # Calculate date range
            to_date = datetime.now()
            from_date = to_date - timedelta(days=days_back)
            
            # Search query - try both company name and ticker
            query = f'"{company_name}" OR "{ticker}"'
            
            params = {
                'q': query,
                'from': from_date.strftime('%Y-%m-%d'),
                'to': to_date.strftime('%Y-%m-%d'),
                'sortBy': 'publishedAt',
                'language': 'en',
                'pageSize': 10,
                'apiKey': self.api_key
            }
            
            # API request
            response = requests.get(f"{self.base_url}/everything", params=params)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                
                # Process articles
                processed_articles = []
                sentiment_scores = []
                
                for article in articles:
                    processed_article = {
                        'title': article.get('title', 'No Title'),
                        'description': article.get('description', 'No Description'),
                        'source': article.get('source', {}).get('name', 'Unknown'),
                        'published_at': article.get('publishedAt', ''),
                        'url': article.get('url', ''),
                        'sentiment': self._analyze_sentiment(article.get('title', '') + ' ' + article.get('description', ''))
                    }
                    processed_articles.append(processed_article)
                    sentiment_scores.append(processed_article['sentiment']['score'])
                
                # Calculate overall sentiment
                overall_sentiment = self._calculate_overall_sentiment(sentiment_scores)
                
                result = {
                    'company_name': company_name,
                    'ticker': ticker,
                    'total_articles': len(processed_articles),
                    'date_range': f"{from_date.strftime('%Y-%m-%d')} to {to_date.strftime('%Y-%m-%d')}",
                    'overall_sentiment': overall_sentiment,
                    'articles': processed_articles,
                    'retrieved_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                self.logger.info(f"✅ Retrieved {len(processed_articles)} articles for {company_name}")
                return result
                
            else:
                error_msg = f"API request failed with status {response.status_code}"
                self.logger.error(f"❌ {error_msg}")
                return {"error": error_msg}
                
        except Exception as e:
            self.logger.error(f"❌ Error fetching news for {company_name}: {str(e)}")
            return {
                "company_name": company_name,
                "ticker": ticker,
                "error": str(e),
                "retrieved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    
    def get_market_news(self, category: str = "business", country: str = "us") -> Dict[str, Any]:
        """
        Fetch general market/business news
        
        Args:
            category: News category ('business', 'technology', etc.)
            country: Country code ('us', 'gb', etc.)
            
        Returns:
            Dict containing market news
        """
        try:
            if not self.api_key:
                return {"error": "NEWS_API_KEY not configured"}
            
            self.logger.info(f"Fetching {category} news for {country}")
            
            params = {
                'category': category,
                'country': country,
                'pageSize': 5,
                'apiKey': self.api_key
            }
            
            response = requests.get(f"{self.base_url}/top-headlines", params=params)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                
                processed_articles = []
                for article in articles:
                    processed_articles.append({
                        'title': article.get('title', 'No Title'),
                        'description': article.get('description', 'No Description'),
                        'source': article.get('source', {}).get('name', 'Unknown'),
                        'published_at': article.get('publishedAt', ''),
                        'url': article.get('url', '')
                    })
                
                result = {
                    'category': category,
                    'country': country,
                    'total_articles': len(processed_articles),
                    'articles': processed_articles,
                    'retrieved_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                self.logger.info(f"✅ Retrieved {len(processed_articles)} {category} articles")
                return result
                
            else:
                error_msg = f"API request failed with status {response.status_code}"
                self.logger.error(f"❌ {error_msg}")
                return {"error": error_msg}
                
        except Exception as e:
            self.logger.error(f"❌ Error fetching market news: {str(e)}")
            return {"error": str(e)}
    
    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Simple sentiment analysis based on keywords
        (In production, you'd use a proper sentiment analysis model)
        """
        positive_words = ['growth', 'profit', 'increase', 'rise', 'gain', 'positive', 'strong', 'good', 'bullish', 'up']
        negative_words = ['loss', 'decline', 'fall', 'drop', 'negative', 'weak', 'bad', 'bearish', 'down', 'crash']
        
        text_lower = text.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = 'Positive'
            score = 1
        elif negative_count > positive_count:
            sentiment = 'Negative'
            score = -1
        else:
            sentiment = 'Neutral'
            score = 0
        
        return {
            'sentiment': sentiment,
            'score': score,
            'positive_indicators': positive_count,
            'negative_indicators': negative_count
        }
    
    def _calculate_overall_sentiment(self, sentiment_scores: List[int]) -> Dict[str, Any]:
        """Calculate overall sentiment from individual scores"""
        if not sentiment_scores:
            return {'sentiment': 'Neutral', 'confidence': 'Low'}
        
        avg_score = sum(sentiment_scores) / len(sentiment_scores)
        
        if avg_score > 0.3:
            sentiment = 'Positive'
        elif avg_score < -0.3:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        
        confidence = 'High' if abs(avg_score) > 0.5 else 'Medium' if abs(avg_score) > 0.2 else 'Low'
        
        return {
            'sentiment': sentiment,
            'score': round(avg_score, 2),
            'confidence': confidence
        }

# global instance
news_api_tools = NewsAPITools()