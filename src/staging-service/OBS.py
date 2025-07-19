import obswspython as obs

class OBS:
    MEDIA_SOURCE_NAME = "AudioSource"


    def __init__(self, windows_ip: str, obs_websocket_password: str, obs_websocket_port: str):
        self.OBS = None
        is_connected = self.connect(windows_ip=windows_ip, obs_websocket_password=obs_websocket_password, obs_websocket_port=obs_websocket_port)

        if not is_connected:
            raise ConnectionError("Failed to connect to OBS WebSocket.")

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

    def close(self):
        if self.OBS:
            try:
                self.OBS.disconnect()
                print("Closed connection to OBS WebSocket.")
            except Exception as e:
                print(f"Error closing connection to OBS WebSocket: {e}")
            finally:
                self.OBS = None