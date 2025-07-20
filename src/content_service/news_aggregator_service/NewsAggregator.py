from .Strategies.NewsAggregationStrategy import NewsAggregationStrategy
from .Strategies.Newspaper import NewspaperAggregationStrategy
from .NewsArticle import NewsArticle

import logging
from typing import List


class NewsAggregator:
    """
    Main aggregation service that can use different strategies
    """
    def __init__(self,  sources = [
    "https://www.apnews.com",
    "https://www.npr.org"
], strategies: List[NewsAggregationStrategy] = None):
        self.sources = sources
        self.strategies = strategies or [
            NewspaperAggregationStrategy()
        ]
    
    def get_articles(self, 
                       max_articles: int = 10) -> List[NewsArticle]:
        """
        Aggregate news using all available strategies
        """
        all_articles = []
        
        for strategy in self.strategies:
            try:
                articles = strategy.fetch_articles(self.sources, max_articles)
                all_articles.extend(articles)
            except Exception as strategy_error:
                logging.error(f"Error in strategy {strategy.__class__.__name__}: {strategy_error}")
        
        # Remove duplicates
        unique_articles = list({article.url: article for article in all_articles}.values())
        
        return unique_articles