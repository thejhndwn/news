from moviepy.editor import *
from pathlib import Path

class VideoGenerator:
    def __init__(self):
        self.root_dir = Path(__file__).resolve().parents[2]  # go up from /src/production
        self.assets_dir = self.root_dir / "src" / "assets"
        self.audio_file = self.root_dir / "output" / "audio" 
        self.output_file = self.root_dir / "output" / "video"

    def generate(self, uuid, text):
        audio = AudioFileClip(str(self.audio_file / f"{uuid}.wav"))
        duration = audio.duration
        image = ImageClip(str(self.assets_dir / "reporter.jpeg")).set_duration(duration)
        video = image.set_audio(audio)
        video = video.resize(height=720)
        video.write_videofile(str(self.output_file/ f"{uuid}.mp4"), fps=24)

        return self.output_file


    def generate_visemes(self, audio):
        # do some viseme generation stuff here
        pass

