import subprocess
import os
from pathlib import Path

class VideoGenerator:
    def __init__(self):
        self.root_dir = Path(__file__).resolve().parents[2]  # go up from /src/production
        self.assets_dir = self.root_dir / "src" / "assets"
        self.audio_file = self.root_dir / "output" / "audio"
        self.blender_file = self.root_dir / "output" / "blender"
        self.output_file = self.root_dir / "output" / "video"

    def generate(self, uuid):

        blender_command = [
            "/home/john-duan/Downloads/blender-4.3.1-linux-x64/blender",
                "-b" , "/home/john-duan/Celia/news/src/assets/reporter.blend1",
                "-P", "/home/john-duan/Celia/news/src/blender.py"
        ]

        try:
            # Run Blender command
            result = subprocess.run(
                blender_command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print("Blender output:", result.stdout)
        except subprocess.CalledProcessError as e:
            print("Blender error:", e.stderr)
            raise
        except FileNotFoundError:
            print(f"Blender not found")
            raise



        command =[
            "-i", self.video_path / f"{uuid}.mp4",          # Input video
            "-i", self.audio_path / f"{uuid}.wav",         # Input audio
            "-c:v", "copy",           # Copy video stream (no re-encoding)
            "-c:a", "aac",            # Encode audio to AAC (for MP4 compatibility)
            "-map", "0:v:0",          # Map video stream from first input
            "-map", "1:a:0",          # Map audio stream from second input
            "-shortest",              # Match duration to shortest input
            "-y",                     # Overwrite output if it exists
            self.output_file / f"TEST_{uuid}.mp4"               # Output file path
        ]

        try:
            # Run FFmpeg command
            result = subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(f"Successfully created video")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg error: {e.stderr}")
            raise
        except FileNotFoundError:
            print("FFmpeg not found. Ensure it's installed and in your system PATH.")
            raise

        return self.output_file / f"TEST_{uuid}.mp4"


    def generate_visemes(self, audio):
        # do some viseme generation stuff here
        pass

