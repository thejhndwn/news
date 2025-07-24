from .Strategies.NewsAggregationStrategy import NewsAggregationStrategy
from .Strategies.Newspaper import NewspaperAggregationStrategy
from .NewsArticle import NewsArticle

import logging
from typing import List


class NewsAggregator:
    """
    Main aggregation service that can use different strategies
    """
    def __init__(self,
                 sources = [
                    "https://www.apnews.com",
                    "https://www.npr.org"
                 ], 
                 strategies: List[NewsAggregationStrategy] = [NewspaperAggregationStrategy()]):

        self.strategies = strategies


    def get_articles(self, num):
        pass
