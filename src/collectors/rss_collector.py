class RSSCollector(BaseCollector):
    source_name = 'RSS'
    
    async def fetch_stories(self) -> List[Dict]:
        """
        Fetch stories from multiple RSS feeds
        Uses async HTTP for efficient fetching
        """
        stories = []
        async with aiohttp.ClientSession() as session:
            tasks = []
            for feed_url in self.sources:
                tasks.append(self.fetch_feed(session, feed_url))
            
            results = await asyncio.gather(*tasks)
            for result in results:
                stories.extend(result)
        
        return stories
    
    async def fetch_feed(self, session, url: str) -> List[Dict]:
        """
        Fetch individual RSS feed
        """
        try:
            async with session.get(url) as response:
                raw_feed = await response.text()
                feed = feedparser.parse(raw_feed)
                
                # Convert to list of dictionaries
                return [
                    {
                        'title': entry.get('title', ''),
                        'description': entry.get('summary', ''),
                        'link': entry.get('link', ''),
                        'published': entry.get('published', ''),
                        'categories': [
                            tag.get('term', '') 
                            for tag in entry.get('tags', [])
                        ]
                    }
                    for entry in feed.entries[:10]  # Limit to 10 recent stories
                ]
        except Exception as e:
            print(f"RSS Feed Error {url}: {e}")
            return []