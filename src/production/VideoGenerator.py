import subprocess
import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

class VideoGenerator:
    def __init__(self, output_path, blender_path, assets_path):
        self.assets_dir = assets_path
        self.blender_file = blender_path
        self.audio_path = Path(output_path) / "audio"
        self.video_path = Path(output_path) / "video"

    def generate(self, uuid):

        logging.info("Starting video generation")

        file_path = Path(self.assets_dir) / "reporter.blend1"

        if file_path.exists():
            print("File exists")
        else:
            print("File does not exist")

        logging.info("checks out")

        file_path = Path("/app/src/blender.py")

        if file_path.exists():
            print("File exists")
        else:
            print("File does not exist")

        logging.info("checks out again")

        blender_command = [
            self.blender_file,
                "-b" , self.assets_dir + "/reporter.blend1",
                "-P", "/app/src/blender.py"
        ]

        logging.info("Running blender command")

        try:
            # Run Blender command
            result = subprocess.run(
                blender_command,
                check=True,
                text=True
            )
            print("Blender output:", result.stdout)
        except subprocess.CalledProcessError as e:
            print("Blender error:", e.stderr)
            raise
        except FileNotFoundError:
            print(f"Blender not found")
            raise

        logging.info("Blender finished successfully")

        command =[
            "ffmpeg",
            "-i", self.video_path / f"blendertest.mp4",          # Input video
            "-i", self.audio_path / f"{uuid}.wav",         # Input audio
            "-c:v", "copy",           # Copy video stream (no re-encoding)
            "-c:a", "aac",            # Encode audio to AAC (for MP4 compatibility)
            "-map", "0:v:0",          # Map video stream from first input
            "-map", "1:a:0",          # Map audio stream from second input
            "-shortest",              # Match duration to shortest input
            "-y",                     # Overwrite output if it exists
            self.video_path / f"TEST_{uuid}.mp4"               # Output file path
        ]

        logging.info("Running ffmpeg command")

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

        return self.video_path / f"TEST_{uuid}.mp4"


    def generate_visemes(self, audio):
        # do some viseme generation stuff here
        pass

