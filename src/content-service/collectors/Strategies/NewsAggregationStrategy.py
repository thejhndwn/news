from abc import ABC, abstractmethod
from typing import List
from ..NewsArticle import NewsArticle

class NewsAggregationStrategy(ABC):
    """
    Abstract base class for news aggregation strategies
    Defines the interface for different news gathering techniques
    """
    @abstractmethod
    def fetch_articles(self, 
                       sources: List[str], 
                       max_articles: int = 10) -> List[NewsArticle]:
        """
        Fetch articles using a specific strategy
        
        :param sources: List of source URLs or RSS feed links
        :param max_articles: Maximum number of articles to fetch
        :return: List of standardized NewsArticle objects
        """
        pass