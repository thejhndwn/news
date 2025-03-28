from .Strategies import NewspaperAggregationStrategy
from .Strategies import RSSAggregationStrategy
from .Strategies import NewsAggregationStrategy
from .NewsArticle import NewsArticle

import logging
from typing import List


class NewsAggregator:
    """
    Main aggregation service that can use different strategies
    """
    def __init__(self, strategies: List[NewsAggregationStrategy] = None):
        self.strategies = strategies or [
            NewspaperAggregationStrategy()
        ]
    
    def add_strategy(self, strategy: NewsAggregationStrategy):
        """
        Dynamically add a new aggregation strategy
        """
        self.strategies.append(strategy)
    
    def aggregate_news(self, 
                       sources: List[str], 
                       max_articles: int = 10) -> List[NewsArticle]:
        """
        Aggregate news using all available strategies
        """
        all_articles = []
        
        for strategy in self.strategies:
            try:
                articles = strategy.fetch_articles(sources, max_articles)
                all_articles.extend(articles)
            except Exception as strategy_error:
                logging.error(f"Error in strategy {strategy.__class__.__name__}: {strategy_error}")
        
        # Remove duplicates
        unique_articles = list({article.url: article for article in all_articles}.values())
        
        return unique_articles