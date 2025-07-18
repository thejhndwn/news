from dataclasses import dataclass
from datetime import datetime

@dataclass
class NewsArticle:
    """
    Standardized data structure for news articles
    Ensures consistent representation across different aggregation methods
    """
    title: str
    url: str
    publish_date: datetime
    source: str
    full_text: str = ''

    @classmethod
    def from_db_article(cls, db_article):
        """
        Converts a database article object to a NewsArticle instance
        """
        return cls(
            title=db_article.title,
            url=db_article.url,
            publish_date=db_article.publish_date,
            source=db_article.source,
            full_text=db_article.full_text
        )