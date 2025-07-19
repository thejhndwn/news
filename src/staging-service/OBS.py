import obswspython as obs

class OBS:
    def __init__(self, windows_ip: str, obs_websocket_password: str, obs_websocket_port: str):
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