
from production.ScriptGenerator import ScriptGenerator
from production.AudioGenerator import AudioGenerator
from production.VideoGenerator import VideoGenerator
from production.TwitchUtils import TwitchStreamer

from dotenv import load_dotenv
import os    
from pathlib import Path



def get_story():
    return ""

def main():



    # Build path to parent directory
    base_dir = Path(__file__).resolve().parent.parent
    secrets_path = base_dir / ".secrets"

    # Load from .secrets (default is .env, but you can name it anything)
    load_dotenv(dotenv_path=secrets_path)

    # Now you can grab it like any environment variable
    stream_key = os.getenv("TWITCH_STREAM_KEY")


    story = get_story()

    
    # staging
    context = {}
    text = ScriptGenerator.generate(story, context)

    audio = AudioGenerator.generate(text)
    
    # content generation
    video_path = VideoGenerator.generate(text, audio)

    # production orchestration
    # figures out what videos are queued to be played, if we need more video and all that

    TwitchStreamer(stream_key, video_path).start_stream()




    
    pass



if __name__ == '__main__':
    main()