from .NewsAggregationStrategy import NewsAggregationStrategy
from ..NewsArticle import NewsArticle
from typing import List

import datetime
import logging
import feedparser

class RSSAggregationStrategy(NewsAggregationStrategy):
    """
    News aggregation using RSS feeds
    Great for sites with well-maintained RSS feeds
    """
    def fetch_articles(self, 
                       sources: List[str], 
                       max_articles: int = 10) -> List[NewsArticle]:
        articles = []
        
        for rss_url in sources:
            try:
                feed = feedparser.parse(rss_url)
                
                for entry in feed.entries[:max_articles]:
                    try:
                        news_article = NewsArticle(
                            title=entry.title,
                            summary=entry.get('summary', ''),
                            url=entry.link,
                            publish_date=datetime.fromtimestamp(
                                entry.get('published_parsed', 
                                          datetime.now().timestamp())
                            ),
                            source=rss_url,
                            keywords=entry.get('tags', [])
                        )
                        articles.append(news_article)
                    
                    except Exception as entry_error:
                        logging.error(f"Error processing RSS entry from {rss_url}: {entry_error}")
            
            except Exception as rss_error:
                logging.error(f"Error fetching RSS feed {rss_url}: {rss_error}")
        
        return articles