from uuid import uuid4

from content_service.news_aggregator_service.NewsAggregator import NewsAggregator
from content_service.news_aggregator_service.Strategies.Newspaper import NewspaperAggregationStrategy

from content_service.audio_viseme_service.AudioGenerator import AudioGenerator
from content_service.audio_viseme_service.VisemeGenerator import VisemeGenerator
from content_service.audio_viseme_service.ScriptGenerator import ScriptGenerator
from content_service.media_generation_service.ImageGenerator import ImageGenerator
from content_service.media_generation_service.AnimationGenerator import AnimationGenerator


'''
ContentService.queue will always be processed. 

TODO: make processing async, so we can process while staging is happening

'''
class ContentService:

    def __init__(self, output_path, tmp_dir, content_queue_size = 10):
        print("Initializing Content Service...")
        self.queue = []
        self.output_path = output_path
        self.tmp_dir = tmp_dir
        self.NewsAggregator = NewspaperAggregationStrategy()
        self.AudioGenerator = AudioGenerator(tmp_dir)
        self.ScriptGenerator = ScriptGenerator()
        self.VisemeGenerator = VisemeGenerator()
        self.ImageGenerator = ImageGenerator()
        self.AnimationGenerator = AnimationGenerator()

        # load existing content from viseme directory, grabbing the UUID file names, 
        # then subtract the difference and get_articles
        self.load_content(output_path / "viseme", file_extension=".json")
        print(f"Loaded {len(self.queue)} existing content items")
        articles = self.NewsAggregator.get_articles(content_queue_size - len(self.queue))

        # process all stories
        for article in articles:
            self.queue.append(self.process_article(article))

        print(f"Content Service initialized")

    def process_article(self, article):
        uuid = uuid4()

        audio_file_path = self.output_path / f"audio/{uuid}.wav"
        viseme_file_path = self.output_path / f"viseme/{uuid}.json"
        print(f"Processing article: {article.title} with UUID: {uuid}")

        script = self.generate_script(article, {} )
        print("this is the script:", script)
        images = self.ImageGenerator.generate(script)
        animations = self.AnimationGenerator.generate(script)
        self.generate_audio_file(script, audio_file_path)
        self.generate_visemes(viseme_file_path, audio_file_path) 
        
        return uuid
    def generate_script(self, article, context = {}):
        return self.ScriptGenerator.generate(article)
    def generate_audio_file(self, script, audio_file_path):
        self.AudioGenerator.generate_long_audio(script, audio_file_path)
    def generate_visemes(self, viseme_file_path, audio_file_path):
        self.VisemeGenerator.generate(viseme_file_path, audio_file_path)

    def make_story_from_url(self, url):
        article = self.NewsAggregator.get_article_from_url(url)
        uuid = self.process_article(article)
        return uuid


    def get_story(self):
        # add story getting logic here
        story_id = self.queue.pop()

        # do stuff to get a new story, async probably
        if len(self.queue) >= 10:
            return story_id
        article = self.NewsAggregator.get_articles(1)[0]
        uuid = self.process_article(article)
        self.queue.append(uuid)
        return story_id
    
    # if there is existing content, not deleted then load it into the queue
    def load_content(self, content_dir, file_extension = ".txt"):
        # get a list of all files in the content_dir, take there names minus the extension and add them to self.queue
        from pathlib import Path
        content_dir = Path(content_dir)
        for file in content_dir.glob(f"*{file_extension}"):
            self.queue.append(file.stem)

    # donations are a list of (donator_name, "amount", message)
    def generate_donation(self, donations):
        uuid = uuid4()

        audio_file_path = self.output_path / f"audio/{uuid}.wav"
        viseme_file_path = self.output_path / f"viseme/{uuid}.json"
        script = """
        And now a word from our sponsors.

        """
        for donator_name, amt, msg in donations:
            script += f"{donator_name} says {msg}"

        self.AudioGenerator.generate_long_audio(script, audio_file_path)
        self.VisemeGenerator.generate(viseme_file_path, audio_file_path)
        return uuid
    
    def print(self):
        print(self.queue)

    def cleanup(self):
        print("Cleaning up Content Service...")
        # add shutdown generators
        print("Content Service cleaned up.")
