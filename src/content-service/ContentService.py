from collectors.NewsAggregator import NewsAggregator

class ContentService:

    def __init__(self, content_queue_size = 10):
        self.queue = []
        self.finished_queue = []
        self.NewsAggregator = NewsAggregator()
        
        self.queue = self.NewsAggregator.get_stories(content_queue_size)
        pass

    def get_story(self):
        # add story getting logic here
        story = self.finished_queue.pop()

        # do stuff to get a new story, async probably
        self.queue.extend(self.NewsAggregator.get_stories(1))
        return story
    
    def print(self):
        print(self.queue)


