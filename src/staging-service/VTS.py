import json
import websocket
import uuid

class VTS:

    def __init__(self, auth_token: str, port: str, windows_ip: str):
        is_connected = self.connect(windows_ip=windows_ip, vts_auth_token=auth_token, vts_port=port)

        if not is_connected:
            raise ConnectionError("Failed to connect and authenticate with VTube Studio.")
        
        
    
    def connect(self, windows_ip: str, vts_auth_token: str, vts_port: str):
        vtube_studio_url = f"ws://{windows_ip}:{vts_port}"

        try:
            self.VTS = websocket.create_connection(vtube_studio_url, timeout = 5)
        except Exception as e:
            print(f"Failed to connect to VTube Studio at {vtube_studio_url}: {e}")
            raise

        auth_login = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": str(uuid.uuid4()),
            "messageType": "AuthenticationRequest",
            "data": {
                "authToken": vts_auth_token,
                "pluginName": self.PLUGIN_NAME,
                "pluginDeveloper": self.PLUGIN_DEVELOPER,
            }
        }

        try:
            self.VTS.send(json.dumps(auth_login))
            response = json.loads(self.VTS.recv())
            if response.get("messageType") == "AuthenticationResponse" and response.get("success"):
                print("Successfully authenticated with VTube Studio.")
                return True
            else:
                print("Authentication failed with VTube Studio.")
                return False
        except Exception as e:
            print(f"Failed to send authentication request to VTube Studio: {e}")
            return False

        return True
    
