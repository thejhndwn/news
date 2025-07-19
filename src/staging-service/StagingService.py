import time
import uuid
import threading
import json
import websocket

from staging_service.OBS import OBS
from staging_service.VTS import VTS

class StagingService:
    PLUGIN_NAME = "NewsAvatar"
    PLUGIN_DEVELOPER = "thejhndwn"

    def __init__(self, windows_ip: str, vts_port: str, vts_auth_token: str, obs_websocket_password: str, obs_websocket_port: str):
        self.OBS = OBS(windows_ip=windows_ip, obs_websocket_password=obs_websocket_password, obs_websocket_port=obs_websocket_port)
        self.VTS = VTS(auth_token=vts_auth_token, port=vts_port, windows_ip=windows_ip)


    def play_story(self, uuid: str):
        audio_file = ''
        viseme_file = ''

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
        return []
    
    def play_audio_in_obs():
        pass

    def play_visemes(visemes, start_time):
        """Play visemes in sync with audio"""
        for timestamp, rhubarb_viseme in visemes:
            target_time = start_time + timestamp
            current_time = time.time()
            
            if target_time > current_time:
                time.sleep(target_time - current_time)
            
            vtube_viseme = rhubarb_to_vtube_viseme(rhubarb_viseme)
            send_viseme_to_vtube_studio(vtube_viseme)

    def get_wave_duration():
        pass

    def rhubarb_to_vtube_viseme(rhubarb_viseme):
        pass

    def send_viseme_to_vtube_studio(vtube_viseme):
        pass




