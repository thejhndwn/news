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
    importance_score: float = 0.0
    keywords: List[str] = None
    full_text: str = ''