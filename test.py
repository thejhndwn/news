import time
import threading
import json
from pathlib import Path
import websocket
import uuid
import subprocess
import sys
import obsws_python as obs
import wave
import os

# VTube Studio API settings
WINDOWS_IP = "172.18.224.1"
VTUBE_STUDIO_URL = f"ws://{WINDOWS_IP}:8001"
OBS_PASSWORD = "MNQQ30Jkgfv8qz58"
OBS_PORT = 4455

# OBS WebSocket settings (default port)
OBS_URL = f"ws://{WINDOWS_IP}:4455"

# API authentication
PLUGIN_NAME = "NewsStreamerBot"
PLUGIN_DEVELOPER = "YourName"
AUTH_TOKEN = None
WS_CONNECTION = None
OBS_CONNECTION = None
WSL_PREFIX = "//wsl.localhost/Ubuntu"

def get_wav_duration(filepath):
    with wave.open(filepath, 'rb') as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        duration = frames / float(rate)
        return duration


def load_viseme_data(viseme_file):
    """Load and parse rhubarb viseme data"""
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

def rhubarb_to_vtube_viseme(rhubarb_viseme):
    """Convert rhubarb viseme to VTube Studio viseme"""
    mapping = {
        'A': 'a',      # open mouth
        'B': 'i',      # closed mouth
        'C': 'u',      # rounded mouth
        'D': 'd',      # tongue up
        'E': 'e',      # slightly open
        'F': 'f',      # lower lip up
        'G': 'k',      # back of tongue up
        'H': 'n',      # tongue tip up
        'X': 'sil'     # silence/neutral
    }
    return mapping.get(rhubarb_viseme, 'sil')

def connect_to_vtube_studio():
    """Connect to VTube Studio and authenticate"""
    global AUTH_TOKEN, WS_CONNECTION
    
    try:
        print("Connecting to VTube Studio...")
        WS_CONNECTION = websocket.create_connection(VTUBE_STUDIO_URL, timeout=5)
        
        # Request authentication token
        auth_request = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": str(uuid.uuid4()),
            "messageType": "AuthenticationTokenRequest",
            "data": {
                "pluginName": PLUGIN_NAME,
                "pluginDeveloper": PLUGIN_DEVELOPER
            }
        }
        
        WS_CONNECTION.send(json.dumps(auth_request))
        response = json.loads(WS_CONNECTION.recv())
        
        if response["messageType"] == "AuthenticationTokenResponse":
            AUTH_TOKEN = response["data"]["authenticationToken"]
            print(f"✓ Authentication token received")
            print("⚠️  Please click 'Allow' in VTube Studio to authorize this plugin")
            
            # Authenticate with token
            auth_login = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": str(uuid.uuid4()),
                "messageType": "AuthenticationRequest",
                "data": {
                    "pluginName": PLUGIN_NAME,
                    "pluginDeveloper": PLUGIN_DEVELOPER,
                    "authenticationToken": AUTH_TOKEN
                }
            }
            
            time.sleep(3)  # Wait for user to click allow
            
            WS_CONNECTION.send(json.dumps(auth_login))
            response = json.loads(WS_CONNECTION.recv())
            
            if response["messageType"] == "AuthenticationResponse" and response["data"]["authenticated"]:
                print("✓ Successfully authenticated with VTube Studio!")
                return True
            else:
                print("✗ Authentication failed. Make sure to click 'Allow' in VTube Studio")
                return False
        else:
            print(f"✗ Token request failed: {response}")
            return False
            
    except Exception as e:
        print(f"✗ Failed to connect to VTube Studio: {e}")
        return False

def connect_to_obs():
    """Connect to OBS WebSocket"""
    global OBS_CONNECTION
    
    try:
        print("Connecting to OBS...")
        # OBS_CONNECTION = websocket.create_connection(OBS_URL, timeout=5)
        OBS_CONNECTION = obs.ReqClient(host=WINDOWS_IP, port=OBS_PORT, password = OBS_PASSWORD)
        print("flag 1")

        # scene = OBS_CONNECTION.call(requests.GetCurrentProgramScene())
        # Get OBS version info
        print("flag 2")
        # print(scene)
        
        

        # print("Current scene:", scene.getName())
        return True
        
        """
        version_request = {
            "op": 6,  # Request
            "d": {
                "requestType": "GetVersion",
                "requestId": str(uuid.uuid4())
            }
        }
        
        
        OBS_CONNECTION.send(json.dumps(version_request))
        response = json.loads(OBS_CONNECTION.recv())
        
        if response["op"] == 7:  # RequestResponse
            print("✓ Successfully connected to OBS!")
            return True
        else:
            print(f"✗ OBS connection failed: {response}")
            return False
        """
            
    except Exception as e:
        print(f"✗ Failed to connect to OBS: {e}")
        print(type(e))
        print(e.args)
        print(str(e))
        return False

def play_audio_in_obs(audio_file):
    """Send audio file to OBS to play"""
    global OBS_CONNECTION
    
    if not OBS_CONNECTION:
        print("  ✗ No OBS connection")
        return 0
    
    try:
        # Method 1: Use OBS Media Source
        # This assumes you have a media source called "AudioPlayer" in OBS

        full_path_audio = os.path.abspath(audio_file)

        OBS_CONNECTION.set_input_settings(name="AudioPlayer", settings={"local_file": WSL_PREFIX + full_path_audio}, overlay=True)
        OBS_CONNECTION.trigger_media_input_action(name="AudioPlayer", action="OBS_WEBSOCKET_MEDIA_INPUT_ACTION_RESTART")
        print("playing audio")
        print("is it working")

        try:
            duration = get_wav_duration(audio_file)
            return duration
        except:
            print("couldn't get duration")
            return 5.0
 

        """
        media_request = {
            "op": 6,
            "d": {
                "requestType": "SetInputSettings",
                "requestId": str(uuid.uuid4()),
                "requestData": {
                    "inputName": "AudioPlayer",
                    "inputSettings": {
                        "local_file": str(Path(audio_file).absolute()),
                        "restart_on_activate": True
                    }
                }
            }
        }
        
        OBS_CONNECTION.send(json.dumps(media_request))
        response = json.loads(OBS_CONNECTION.recv())
        
        if response["op"] == 7:  # RequestResponse
            print(f"✓ Audio sent to OBS: {audio_file}")
            
            # Get duration using ffprobe if available
            try:
                result = subprocess.run([
                    'ffprobe', '-v', 'quiet', '-show_entries', 
                    'format=duration', '-of', 'csv=p=0', audio_file
                ], capture_output=True, text=True)
                duration = float(result.stdout.strip())
                return duration
            except:
                print("  ⚠️  Could not get audio duration, using 5s default")
                return 5.0
        else:
            print(f"  ✗ Failed to send audio to OBS: {response}")
            return 0
    """
            
    except Exception as e:
        print(f"  ✗ Error sending audio to OBS: {e}")
        return 0

def send_viseme_to_vtube_studio(viseme):
    """Send Rhubarb lip sync viseme data to VTube Studio"""
    global WS_CONNECTION, AUTH_TOKEN
    
    if not WS_CONNECTION:
        print("✗ No WebSocket connection available")
        return False
    
    if not AUTH_TOKEN:
        print("✗ No authentication token available")
        return False
    
    print(f"  → Viseme: {viseme}")
    
    try:
        # Rhubarb lip sync viseme categories mapped to VTube Studio vowel parameters
        # Using the standard VTube Studio mouth parameters: ParamA, ParamI, ParamU, ParamE, ParamO
        rhubarb_to_expression = {
            'X': {'ParamA': 0.0, 'ParamI': 0.0, 'ParamU': 0.0, 'ParamE': 0.0, 'ParamO': 0.0},  # Silence
            'A': {'ParamA': 1.0, 'ParamI': 0.0, 'ParamU': 0.0, 'ParamE': 0.0, 'ParamO': 0.0},  # Open vowels (ah)
            'B': {'ParamA': 0.0, 'ParamI': 0.0, 'ParamU': 0.0, 'ParamE': 0.0, 'ParamO': 0.0},  # Closed mouth (p, b, m)
            'C': {'ParamA': 0.0, 'ParamI': 0.0, 'ParamU': 0.0, 'ParamE': 0.8, 'ParamO': 0.0},  # Mid vowels (e, eh)
            'D': {'ParamA': 0.6, 'ParamI': 0.0, 'ParamU': 0.0, 'ParamE': 0.3, 'ParamO': 0.0},  # Mixed (ai, ay)
            'E': {'ParamA': 0.0, 'ParamI': 0.0, 'ParamU': 0.9, 'ParamE': 0.0, 'ParamO': 0.0},  # Rounded (oo, uw)
            'F': {'ParamA': 0.0, 'ParamI': 0.0, 'ParamU': 0.0, 'ParamE': 0.4, 'ParamO': 0.0},  # Narrow (f, v)
            'G': {'ParamA': 0.0, 'ParamI': 0.0, 'ParamU': 0.0, 'ParamE': 0.2, 'ParamO': 0.0},  # Tongue/teeth (k, g, t, d)
            'H': {'ParamA': 0.0, 'ParamI': 0.7, 'ParamU': 0.0, 'ParamE': 0.0, 'ParamO': 0.0}   # Narrow front (i, ih)
        }
        
        # Get expression values for this Rhubarb viseme
        expression_values = rhubarb_to_expression.get(viseme, {'ParamA': 0.0, 'ParamI': 0.0, 'ParamU': 0.0, 'ParamE': 0.0, 'ParamO': 0.0})
        
        # Send parameter injection request to VTube Studio
        param_request = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": str(uuid.uuid4()),
            "messageType": "InjectParameterDataRequest",
            "data": {
                "faceFound": True,
                "mode": "set",
                "parameterValues": [
                    {
                        "id": param_name,
                        "value": value
                    }
                    for param_name, value in expression_values.items()
                ]
            }
        }
        WS_CONNECTION.send(json.dumps(param_request))
        # Optional: Wait for response to confirm success
        try:
            response = json.loads(WS_CONNECTION.recv())
            if response["messageType"] == "InjectParameterDataResponse":
                return True
            else:
                print(f"    ⚠ Unexpected response: {response}")
                return False
        except Exception as e:
            print(f"    ⚠ Response error: {e}")
            return False
        
    except Exception as e:
        print(f"    ✗ Error sending viseme: {e}")
        return False

def play_visemes(visemes, start_time):
    """Play visemes in sync with audio"""
    for timestamp, rhubarb_viseme in visemes:
        target_time = start_time + timestamp
        current_time = time.time()
        
        if target_time > current_time:
            time.sleep(target_time - current_time)
        
        vtube_viseme = rhubarb_to_vtube_viseme(rhubarb_viseme)
        send_viseme_to_vtube_studio(vtube_viseme)

def play_story(story_num):
    """Play a single story (audio in OBS + visemes in VTube Studio)"""
    audio_file = f"./output/audio/{story_num}.wav"
    viseme_file = f"./output/viseme/{story_num}.txt"
    
    print(f"\n=== Playing Story {story_num} ===")
    
    # Load viseme data
    visemes = load_viseme_data(viseme_file)
    
    # Start audio in OBS
    start_time = time.time()
    duration = play_audio_in_obs(audio_file)
    
    if duration > 0:
        # Start viseme playback
        if visemes:
            viseme_thread = threading.Thread(target=play_visemes, args=(visemes, start_time))
            viseme_thread.daemon = True
            viseme_thread.start()
        
        # Wait for audio to finish
        time.sleep(duration)
        time.sleep(0.5)  # Small gap between stories
    
    print(f"Story {story_num} completed")

def cleanup():
    """Clean up connections"""
    global WS_CONNECTION, OBS_CONNECTION
    
    if WS_CONNECTION:
        try:
            WS_CONNECTION.close()
            print("✓ Disconnected from VTube Studio")
        except:
            pass
    
    if OBS_CONNECTION:
        try:
            OBS_CONNECTION.close()
            print("✓ Disconnected from OBS")
        except:
            pass

def main():
    # Connect to services
    vtube_connected = connect_to_vtube_studio()
    obs_connected = connect_to_obs()
    
    if not vtube_connected and not obs_connected:
        print("Failed to connect to both VTube Studio and OBS. Exiting...")
        return
    if not obs_connected:
        print("Faile to connect obs")
        return
   
    if not vtube_connected:
        print("Faile to connect vtube")
        return
    
    print("Starting audio + viseme test...")
    print("NOTE: Make sure you have a Media Source called 'AudioPlayer' in OBS")
    
    # Play all 3 stories in succession
    for story_num in range(1, 4):
        audio_file = f"./output/audio/{story_num}.wav"
        
        if not Path(audio_file).exists():
            print(f"Warning: Audio file {audio_file} not found, skipping story {story_num}")
            continue
            
        play_story(story_num)
    
    print("\nAll stories completed!")
    cleanup()

if __name__ == "__main__":
    main()
