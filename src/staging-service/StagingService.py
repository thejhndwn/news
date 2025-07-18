import time
import threading

class StagingService:


    def __init__(self):
        self.OBS = None
        self.VTS = None

        vts_connected = self.connect_to_vts()
        obs_connected = self.connect_to_obs()

        if not vts_connected or not obs_connected:
            print(f"Something failed to connect...OBS:{obs_connected}, VTS:{vts_connected}") 


    def connect_to_vts():
        


        return True

    def connect_to_obs():
        return True
    
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

    def play_visemes():
        pass

    def get_wave_duration():
        pass




