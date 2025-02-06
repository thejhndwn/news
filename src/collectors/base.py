import asyncio
import re
from typing import List, Dict
from datetime import datetime
import json
from abc import ABC, abstractmethod

class BaseCollector(ABC):
    def __init__(self, config, queue):
        """
        Base collector with common initialization
        
        :param config: Configuration dictionary
        :param queue: Async queue to push collected stories
        """
        self.config = config
        self.queue = queue
        self.sources = self.config.get('sources', [])
        self.interval = self.config.get('polling_interval', 300)  # Default 5 minutes
    
    @abstractmethod
    async def fetch_stories(self) -> List[Dict]:
        """
        Abstract method to fetch stories from source
        Must be implemented by each specific collector
        """
        pass
    
    async def process_story(self, raw_story: Dict) -> Dict:
        """
        Standardize story format across different sources
        
        :param raw_story: Raw story from source
        :return: Normalized story dictionary
        """
        return {
            'id': self.generate_unique_id(raw_story),
            'title': self.clean_text(raw_story.get('title', '')),
            'description': self.clean_text(raw_story.get('description', '')),
            'source': self.source_name,
            'url': raw_story.get('link', ''),
            'published_at': self.parse_timestamp(raw_story),
            'categories': raw_story.get('categories', []),
            'raw_content': json.dumps(raw_story),
            'urgency': self.detect_urgency(raw_story)
        }
    
    def generate_unique_id(self, story: Dict) -> str:
        """Generate a unique ID for the story"""
        return hashlib.md5(
            f"{story.get('title', '')}_{story.get('link', '')}".encode()
        ).hexdigest()
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove HTML tags, extra whitespace
        text = re.sub(r'<[^>]+>', '', text)
        return ' '.join(text.split())
    
    def parse_timestamp(self, story: Dict) -> str:
        """Parse timestamp from various formats"""
        try:
            # Try multiple timestamp formats
            formats = [
                '%a, %d %b %Y %H:%M:%S %z',
                '%Y-%m-%dT%H:%M:%S%z',
                '%d %b %Y %H:%M:%S %Z'
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(
                        story.get('published', ''), 
                        fmt
                    ).isoformat()
                except (ValueError, TypeError):
                    continue
            
            return datetime.utcnow().isoformat()
        except Exception:
            return datetime.utcnow().isoformat()
    
    def detect_urgency(self, story: Dict) -> int:
        """
        Detect story urgency based on content
        
        Urgency levels:
        0: Normal news
        1: Potentially important
        2: Breaking news
        """
        urgency_keywords = {
            2: ['breaking', 'urgent', 'emergency', 'alert'],
            1: ['important', 'significant', 'major']
        }
        
        title = story.get('title', '').lower()
        description = story.get('description', '').lower()
        
        for level, keywords in urgency_keywords.items():
            if any(keyword in title or keyword in description for keyword in keywords):
                return level
        
        return 0
    
    async def collect(self):
        """
        Main collection method
        Polls sources at configured interval
        """
        while True:
            try:
                stories = await self.fetch_stories()
                
                for raw_story in stories:
                    processed_story = await self.process_story(raw_story)
                    await self.queue.put(processed_story)
                
            except Exception as e:
                print(f"Collection error: {e}")
            
            await asyncio.sleep(self.interval)
