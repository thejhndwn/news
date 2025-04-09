
from production.ScriptGenerator import ScriptGenerator
from production.AudioGenerator import AudioGenerator
from production.VideoGenerator import VideoGenerator
from production.TwitchUtils import TwitchStreamer

from database.database import get_engine, Session
from database.models import Article

import logging
import uuid


def main():
    logging.basicConfig(level=logging.INFO)

    ScriptGenerator = ScriptGenerator()
    AudioGenerator = AudioGenerator()
    VideoGenerator = VideoGenerator()



    # database connection
    engine = get_engine()
    session = Session()
    context = {}

    uuid = uuid.uuid4()
    story = session.query(Article).first()
    logging.info(story.title)

    text = ScriptGenerator.generate(story, context)
    audio = AudioGenerator.generate(uuid, text)
    video_path = VideoGenerator.generate(uuid, text, audio)

    # production orchestration
    # figures out what videos are queued to be played, if we need more video and all that

    # TwitchStreamer(stream_key, video_path).start_stream()




    
    pass



if __name__ == '__main__':
    main()