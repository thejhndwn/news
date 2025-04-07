from moviepy.editor import *
from pathlib import Path

class VideoGenerator:
    def __init__(self):
        self.root_dir = Path(__file__).resolve().parents[2]  # go up from /src/production
        self.assets_dir = self.root_dir / "src" / "assets"
        self.audio_file = self.root_dir / "output" / "audio" / "audio.mp3"
        self.output_file = self.root_dir / "output" / "video" / "video.mp4"

    def generate(self):
        audio = AudioFileClip(str(self.audio_file))
        duration = audio.duration
        image = ImageClip(str(self.assets_dir / "reporter.jpeg")).set_duration(duration)
        video = image.set_audio(audio)
        video = video.resize(height=720)
        video.write_videofile(str(self.output_file), fps=24)

        return self.output_file


    def bind_audio_and_video(self, audio, *video):
        pass


    def generate_visemes(self, audio):
        # do some viseme generation stuff here
        pass

