from collectors.base import BaseCollector


class TwitterCollector(BaseCollector):
    source_name = 'Twitter'
    
    async def fetch_stories(self) -> List[Dict]:
        """
        Fetch stories from Twitter API
        Uses Twitter API v2 with bearer token
        """
        headers = {
            'Authorization': f'Bearer {self.config.get("twitter_bearer_token")}'
        }
        
        stories = []
        for query in self.sources:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    'https://api.twitter.com/2/tweets/search/recent',
                    params={'query': query, 'max_results': 10},
                    headers=headers
                ) as response:
                    data = await response.json()
                    
                    stories.extend([
                        {
                            'title': tweet['text'][:280],
                            'description': tweet['text'],
                            'link': f'https://twitter.com/x/status/{tweet["id"]}',
                            'published': datetime.utcnow().isoformat(),
                            'categories': []
                        }
                        for tweet in data.get('data', [])
                    ])
        
        return stories