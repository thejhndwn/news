from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Index, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'
    
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    url = Column(Text, nullable=False, unique=True)
    publish_date = Column(DateTime, default=datetime.utcnow, nullable=False) 
    source = Column(String(100))
    full_text = Column(Text)
    
    # Define indexes
    __table_args__ = (
        Index('idx_articles_source', source),
        Index('idx_articles_published_date', publish_date),
    )
    
    def __repr__(self):
        return f"<Article(id={self.id}, title='{self.title[:30]}...', source='{self.source}')>"
