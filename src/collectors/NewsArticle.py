from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class NewsArticle:
    """
    Standardized data structure for news articles
    Ensures consistent representation across different aggregation methods
    """
    title: str
    summary: str
    url: str
    publish_date: datetime
    source: str
    full_text: str = ''