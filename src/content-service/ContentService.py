from uuid import uuid4
from collectors.NewsAggregator import NewsAggregator

from ..audio_viseme_service.AudioGenerator import AudioGenerator
from ..audio_viseme_service.VisemeGenerator import VisemeGenerator
from ..audio_viseme_service.ScriptGenerator import ScriptGenerator

'''
ContentService.queue will always be processed. 

TODO: make processing async, so we can process while staging is happening

'''
class ContentService:

    def __init__(self, output_path, content_queue_size = 10):
        print("Initializing Content Service...")
        self.queue = []
        self.output_path = output_path
        self.NewsAggregator = NewsAggregator()
        self.AudioGenerator = AudioGenerator()
        self.ScriptGenerator = ScriptGenerator()
        self.VisemeGenerator = VisemeGenerator()
        articles = self.NewsAggregator.get_stories(content_queue_size)

        # process all stories
        for article in articles:
            self.queue.append(self.process_article(article))

        print(f"Content Service initialized")

    def process_article(self, article):
        uuid = uuid4()

        audio_file_path = self.output_path + f"/audio/{uuid}.wav"
        viseme_file_path = self.output_path + f"/visemes/{uuid}.json"
        print(f"Processing article: {article['title']} with UUID: {uuid}")


        script = self.generate_script(article['full_text'])
        self.generate_audio_file(script, audio_file_path)
        self.generate_visemes(viseme_file_path) 
        
        return uuid
    def generate_script(self, article, context):
        return self.ScriptGenerator.generate(article['full_text'], context)
    def generate_audio_file(self, script, audio_file_path):
        self.AudioGenerator.generate(audio_file_path, script)
        pass
    def generate_visemes(self, viseme_file_path):
        self.VisemeGenerator.generate(viseme_file_path)
        pass


    def get_story(self):
        # add story getting logic here
        story_id = self.queue.pop()

        # do stuff to get a new story, async probably

        article = self.NewsAggregator.get_stories(1)[0]
        uuid = self.process_article(article)
        self.queue.append(uuid)
        return story_id
    
    def print(self):
        print(self.queue)


