import subprocess

class TwitchStreamer:
    def __init__(self, stream_key, video_file, audio_file=None):
        self.stream_key = stream_key
        self.video_file = video_file
        self.audio_file = audio_file

    def start_stream(self):
        command = [
            "ffmpeg",
            "-re",
            "-i", self.video_file,
        ]

        if self.audio_file:
            command.extend(["-i", self.audio_file])

        command.extend([
            "-c:v", "libx264",
            "-c:a", "aac",
            "-preset", "fast",
            "-f", "flv",
            f"rtmp://live.twitch.tv/app/{self.stream_key}"
        ])

        subprocess.run(command)
