
from production.ScriptGenerator import ScriptGenerator
from production.AudioGenerator import AudioGenerator
from production.VideoGenerator import VideoGenerator
from production.TwitchUtils import TwitchStreamer

from database.database import get_engine
from sqlalchemy.orm import Session
from database.models import Article

import logging
import uuid

def main():
    logging.basicConfig(level=logging.INFO)
    session = Session()
    article = None

    with Session(get_engine()) as session:
        article = session.query(Article).first()
        logging.info("grabbed article")


    script_generator = ScriptGenerator()
    audio_generator = AudioGenerator()
    video_generator = VideoGenerator()

    id = uuid.uuid4()
    context = {}
    text = script_generator.generate(article, context)
    audio = audio_generator.generate(id, text)
    video_path = video_generator.generate(id)

    # we get the file path of the video, we should add it to the dynamic twitch queue

    # 




    
    pass



if __name__ == '__main__':
    main()