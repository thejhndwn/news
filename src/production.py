
from production.ScriptGenerator import ScriptGenerator
from production.AudioGenerator import AudioGenerator
from production.VideoGenerator import VideoGenerator
from production.TwitchUtils import TwitchStreamer

from database.database import get_engine
from sqlalchemy.orm import Session
from database.models import Article

import logging
import uuid
import os

def main():
    logging.basicConfig(level=logging.INFO)
    output_path = os.getenv("OUTPUT_FILEPATH", "/app/output")
    blender_path = os.getenv("BLENDER_FILEPATH", "/usr/local/bin/blender")
    assets_path = os.getenv("ASSETS_FILEPATH", "/app/src/assets")
    session = Session()
    article = None

    with Session(get_engine()) as session:
        article = session.query(Article).first()
        logging.info("grabbed article")


    script_generator = ScriptGenerator()
    audio_generator = AudioGenerator(output_path=output_path)
    video_generator = VideoGenerator(output_path= output_path, blender_path=blender_path,
                                      assets_path=assets_path)

    id = uuid.uuid4()
    context = {}


    text = script_generator.generate(article, context)
    logging.info("starting audio generation")
    audio = audio_generator.generate(id, text)
    logging.info("starting video generation")
    video_path = video_generator.generate(id)

    # we get the file path of the video, we should add it to the dynamic twitch queue

    # 




    
    pass



if __name__ == '__main__':
    main()