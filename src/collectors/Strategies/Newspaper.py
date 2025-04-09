from .NewsAggregationStrategy import NewsAggregationStrategy
from ..NewsArticle import NewsArticle
from typing import List
import logging
import datetime
import newspaper

from newspaper import Article
from newspaper import Config

class NewspaperAggregationStrategy(NewsAggregationStrategy):

    def fetch_articles(self, 
                    sources: List[str], 
                    max_articles: int = 10) -> List[NewsArticle]:
        articles = []
        
        for source_url in sources:
            try:
                # Build source using newspaper
                source = newspaper.build(source_url, memoize_articles=False)
                
                for article in source.articles[:max_articles]:
                    try:
                        article.download()
                        article.parse()
                        
                        news_article = NewsArticle(
                            title=article.title,
                            url=article.url,
                            publish_date=article.publish_date or datetime.datetime.now(),
                            source=source_url,
                            full_text=article.text
                        )
                        articles.append(news_article)
                    
                    except Exception as article_error:
                        logging.error(f"Error processing article from {source_url}: {article_error}")
            
            except Exception as source_error:
                logging.error(f"Error building source {source_url}: {source_error}")
        
        return articles