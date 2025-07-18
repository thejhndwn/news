from collectors.NewsAggregator import NewsAggregator

class ContentService:

    def __init__(self, seen_stories_file, content_queue_size = 10):
        self.queue = []
        self.seen_stories_file = seen_stories_file
        self.NewsAggregator = NewsAggregator()
        
        self.queue = self.NewsAggregator.get_stories(content_queue_size)
        pass

    def get_story(self):
        # add story getting logic here
        story = self.queue.pop()

        # do stuff to get a new story, async probably

        return story
    
    def print(self):
        print(self.queue)


