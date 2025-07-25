import obsws_python as obs

class OBS:
    MEDIA_SOURCE_NAME = "AudioPlayer"


    def __init__(self, twitch_key:str , windows_ip: str, obs_websocket_password: str, obs_websocket_port: str):
        self.OBS = None
        is_connected = self.connect(windows_ip=windows_ip, obs_websocket_password=obs_websocket_password, obs_websocket_port=obs_websocket_port)

        if not is_connected:
            raise ConnectionError("Failed to connect to OBS WebSocket.")
        
        self.set_twitch_key(twitch_key)

    def connect(self, windows_ip: str, obs_websocket_password: str, obs_websocket_port: str):
        try:
            self.OBS = obs.ReqClient(host=windows_ip, port=obs_websocket_port, password=obs_websocket_password)
            print("Successfully connected to OBS WebSocket.")
            return True
        except Exception as e:
            print(f"Failed to connect to OBS WebSocket at {windows_ip}:{obs_websocket_port}: {e}")
            return False
        
    def play_audio(self, audio_file: str):
        self.OBS.set_input_settings(name=self.MEDIA_SOURCE_NAME, settings={"local_file": audio_file}, overlay=True)
        self.OBS.trigger_media_input_action(name=self.MEDIA_SOURCE_NAME, action="OBS_WEBSOCKET_MEDIA_INPUT_ACTION_RESTART")

    def set_scene(self, scene:str):
        pass
    def play_image(self, image:str):
        pass

    def close(self):
        if self.OBS:
            try:
                self.OBS.disconnect()
                print("Closed connection to OBS WebSocket.")
            except Exception as e:
                print(f"Error closing connection to OBS WebSocket: {e}")
            finally:
                self.OBS = None
    
    def set_twitch_key(self, twitch_key: str):
        try:
            self.OBS.set_stream_service_settings(ss_type = "rtmp_common", 
                                                 ss_settings={
                                                     "key": twitch_key,
                                                     "server": "auto",
                                                     "service": "Twitch"
                                                   })
            print("Successfully set Twitch stream key in OBS.")
            return True
        except Exception as e:
            print(f"Failed to set Twitch stream key in OBS: {e}")
            return False
        
    def start_streaming(self):
        try:
            self.OBS.start_stream()
            print("Started streaming in OBS.")
            return True
        except Exception as e:
            print(f"Failed to start streaming in OBS: {e}")
            return False
        
    def stop_streaming(self):
        try:
            self.OBS.stop_stream()
            print("Stopped streaming in OBS.")
            return True
        except Exception as e:
            print(f"Failed to stop streaming in OBS: {e}")
            return False
        
