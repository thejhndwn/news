import time
import wave
import threading
import os

from staging_service.OBS import OBS
from staging_service.VTS import VTS

class StagingService:
    PLUGIN_NAME = "NewsAvatar"
    PLUGIN_DEVELOPER = "thejhndwn"

    def __init__(self, output_path, windows_ip: str, vts_port: str, vts_auth_token: str, obs_websocket_password: str, obs_websocket_port: str):
        print("Initializing Staging Service...")
        self.output_path = output_path
        self.audio_path = output_path / "audio"
        self.viseme_path = output_path / "viseme"

        self.OBS = OBS(windows_ip=windows_ip, obs_websocket_password=obs_websocket_password, obs_websocket_port=obs_websocket_port)
        self.VTS = VTS(auth_token=vts_auth_token, port=vts_port, windows_ip=windows_ip)


    def play_story(self, uuid: str):
        audio_file = self.audio_path / f"{uuid}.wav"
        viseme_file = self.viseme_path / f"{uuid}.json"

        visemes = self.load_viseme(viseme_file)
        duration = self.get_wav_duration(audio_file)

        if duration > 0:
            self.play_audio_in_obs(audio_file)
            start_time = time.time()
            if visemes:
                viseme_thread = threading.Thread(target=self.play_visemes, args=(visemes, start_time))
            
            # wait for audio to finish
            time.sleep(duration)

    def load_viseme(viseme_file):
        visemes = []
        try:
            with open(viseme_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split()
                        if len(parts) >= 2:
                            timestamp = float(parts[0])
                            viseme = parts[1]
                            visemes.append((timestamp, viseme))
        except FileNotFoundError:
            print(f"Warning: Viseme file {viseme_file} not found")
            return []
        
        print(f"Loaded {len(visemes)} visemes from {viseme_file}")
        return visemes
        
    def play_audio_in_obs(self, audio_file: str):
        WSL_PREFIX = "//wsl.localhost/Ubuntu"
        full_audio_path = WSL_PREFIX + os.path.abspath(audio_file)
        self.OBS.play_audio(full_audio_path)

    def play_visemes(self, visemes, start_time):
        """Play visemes in sync with audio"""
        for timestamp, rhubarb_viseme in visemes:
            target_time = start_time + timestamp
            current_time = time.time()
            
            if target_time > current_time:
                time.sleep(target_time - current_time)
            
            vtube_viseme = self.rhubarb_to_vtube_viseme(rhubarb_viseme)
            self.VTS.send_viseme(vtube_viseme)

    def get_wave_duration(file_path: str):
        with wave.open(file_path, 'rb') as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            duration = frames / float(rate)
            return duration

    def rhubarb_to_vtube_viseme(rhubarb_viseme):
        pass


    def cleanup(self):
        print("Cleaning up StagingService resources...")
        if self.OBS:
            self.OBS.close()
        if self.VTS:
            self.VTS.close() 
        print("StagingService cleanup complete.")




