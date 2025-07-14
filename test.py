import asyncio
import json
import time
import threading
import queue
import os
from typing import Dict, List, Optional, Tuple
import websockets
from dataclasses import dataclass
from enum import Enum
import wave
import contextlib

WINDOWS_HOST_IP="10.255.255.254"

class Priority(Enum):
    NORMAL = 1
    BREAKING = 2
    URGENT = 3

@dataclass
class NewsItem:
    audio_file: str
    viseme_file: str
    priority: Priority = Priority.NORMAL
    id: str = ""
    
    def __post_init__(self):
        if not self.id:
            self.id = f"{int(time.time() * 1000)}"

class VTuberStudioAPI:
    def __init__(self, host=None, port=8001):
        self.host = host or WINDOWS_HOST_IP
        self.port = port
        self.websocket = None
        self.authenticated = False
        
    async def connect(self):
        """Connect to VTuber Studio API"""
        try:
            self.websocket = await websockets.connect(f"ws://{self.host}:{self.port}")
            print("Connected to VTuber Studio")
            return True
        except Exception as e:
            print(f"Failed to connect to VTuber Studio: {e}")
            return False
    
    async def authenticate(self):
        """Authenticate with VTuber Studio"""
        auth_request = {
            "apiName": "VTuberStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "auth_request",
            "messageType": "AuthenticationTokenRequest",
            "data": {
                "pluginName": "NewsStreamerBot",
                "pluginDeveloper": "YourName",
                "pluginIcon": ""
            }
        }
        
        try:
            await self.websocket.send(json.dumps(auth_request))
            response = await self.websocket.recv()
            data = json.loads(response)
            
            if data.get("messageType") == "AuthenticationTokenResponse":
                token = data["data"]["authenticationToken"]
                
                # Now authenticate with the token
                auth_with_token = {
                    "apiName": "VTuberStudioPublicAPI",
                    "apiVersion": "1.0",
                    "requestID": "auth_with_token",
                    "messageType": "AuthenticationRequest",
                    "data": {
                        "pluginName": "NewsStreamerBot",
                        "pluginDeveloper": "YourName",
                        "authenticationToken": token
                    }
                }
                
                await self.websocket.send(json.dumps(auth_with_token))
                response = await self.websocket.recv()
                data = json.loads(response)
                
                if data.get("messageType") == "AuthenticationResponse":
                    self.authenticated = data["data"]["authenticated"]
                    print(f"Authentication: {'Success' if self.authenticated else 'Failed'}")
                    return self.authenticated
                    
        except Exception as e:
            print(f"Authentication error: {e}")
            return False
    
    async def send_viseme(self, viseme_data: str):
        """Send viseme data to VTuber Studio"""
        if not self.authenticated:
            print("Not authenticated with VTuber Studio")
            return
            
        # Parse viseme data and send mouth movements
        # This is a simplified version - you'll need to adapt based on your viseme format
        try:
            viseme_request = {
                "apiName": "VTuberStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": f"viseme_{int(time.time() * 1000)}",
                "messageType": "InjectParameterDataRequest",
                "data": {
                    "parameterValues": [
                        {
                            "id": "MouthOpen",
                            "value": self.parse_viseme_intensity(viseme_data)
                        }
                    ]
                }
            }
            
            await self.websocket.send(json.dumps(viseme_request))
            
        except Exception as e:
            print(f"Error sending viseme: {e}")
    
    def parse_viseme_intensity(self, viseme_data: str) -> float:
        """Parse viseme data to mouth intensity (0.0 to 1.0)"""
        # This is a placeholder - adapt based on your viseme format
        # Common visemes: A, E, I, O, U, M, B, P, F, V, etc.
        vowel_intensity = {'A': 0.8, 'E': 0.6, 'I': 0.4, 'O': 0.9, 'U': 0.7}
        consonant_intensity = {'M': 0.2, 'B': 0.3, 'P': 0.3, 'F': 0.1, 'V': 0.2}
        
        # Simple parsing - you'll want to make this more sophisticated
        if viseme_data.strip().upper() in vowel_intensity:
            return vowel_intensity[viseme_data.strip().upper()]
        elif viseme_data.strip().upper() in consonant_intensity:
            return consonant_intensity[viseme_data.strip().upper()]
        else:
            return 0.0
    
    async def disconnect(self):
        """Disconnect from VTuber Studio"""
        if self.websocket:
            await self.websocket.close()
            print("Disconnected from VTuber Studio")

class OBSClient:
    def __init__(self, host=None, port=4455, password=""):
        self.host = host or WINDOWS_HOST_IP
        self.port = port
        self.password = password
        self.websocket = None
        self.authenticated = False
        
    async def connect(self):
        """Connect to OBS WebSocket"""
        try:
            self.websocket = await websockets.connect(f"ws://{self.host}:{self.port}")
            print("Connected to OBS WebSocket")
            
            # Authenticate if password is set
            if self.password:
                await self.authenticate()
            else:
                self.authenticated = True
            
            return True
        except Exception as e:
            print(f"Failed to connect to OBS: {e}")
            return False
    
    async def authenticate(self):
        """Authenticate with OBS"""
        # OBS WebSocket authentication logic would go here
        # For now, assuming no auth needed
        self.authenticated = True
        
    async def set_media_source(self, source_name: str, file_path: str):
        """Set media source file in OBS"""
        if not self.authenticated:
            return False
            
        request = {
            "op": 6,  # Request
            "d": {
                "requestType": "SetInputSettings",
                "requestId": f"set_media_{int(time.time() * 1000)}",
                "requestData": {
                    "inputName": source_name,
                    "inputSettings": {
                        "local_file": file_path
                    }
                }
            }
        }
        
        try:
            await self.websocket.send(json.dumps(request))
            response = await self.websocket.recv()
            print(f"Set media source {source_name} to {file_path}")
            return True
        except Exception as e:
            print(f"Error setting media source: {e}")
            return False
    
    async def trigger_media_restart(self, source_name: str):
        """Restart media source playback"""
        request = {
            "op": 6,
            "d": {
                "requestType": "TriggerMediaInputAction",
                "requestId": f"trigger_media_{int(time.time() * 1000)}",
                "requestData": {
                    "inputName": source_name,
                    "mediaAction": "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_RESTART"
                }
            }
        }
        
        try:
            await self.websocket.send(json.dumps(request))
            response = await self.websocket.recv()
            print(f"Triggered restart for {source_name}")
            return True
        except Exception as e:
            print(f"Error triggering media restart: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from OBS"""
        if self.websocket:
            await self.websocket.close()
            print("Disconnected from OBS")

class AudioManager:
    def __init__(self):
        self.current_audio = None
        self.audio_start_time = 0
        
    def get_audio_duration(self, audio_file: str) -> float:
        """Get audio duration without playing"""
        try:
            with contextlib.closing(wave.open(audio_file, 'r')) as f:
                frames = f.getnframes()
                rate = f.getframerate()
                duration = frames / float(rate)
                return duration
        except Exception as e:
            print(f"Error getting audio duration for {audio_file}: {e}")
            return 0.0
    
    def start_audio_tracking(self, audio_file: str) -> float:
        """Start tracking audio playback"""
        self.current_audio = audio_file
        self.audio_start_time = time.time()
        duration = self.get_audio_duration(audio_file)
        print(f"Tracking audio: {audio_file} (Duration: {duration:.2f}s)")
        return duration
    
    def stop_audio_tracking(self):
        """Stop tracking current audio"""
        self.current_audio = None
        self.audio_start_time = 0
        print("Audio tracking stopped")
    
    def is_audio_playing(self) -> bool:
        """Check if audio should still be playing based on duration"""
        if not self.current_audio:
            return False
        
        elapsed = time.time() - self.audio_start_time
        duration = self.get_audio_duration(self.current_audio)
        return elapsed < duration
    
    def get_audio_position(self) -> float:
        """Get current audio position in seconds"""
        if not self.current_audio:
            return 0.0
        return time.time() - self.audio_start_time

class NewsStreamer:
    def __init__(self, audio_source_name="NewsAudio"):
        self.vts_api = VTuberStudioAPI()
        self.obs_client = OBSClient()
        self.audio_manager = AudioManager()
        self.audio_source_name = audio_source_name
        self.news_queue = queue.PriorityQueue()
        self.current_item: Optional[NewsItem] = None
        self.is_running = False
        self.playback_thread = None
        self.sequence_number = 0  # Add sequence counter for queue ordering
        
    async def initialize(self):
        """Initialize VTuber Studio and OBS connections"""
        vts_connected = await self.vts_api.connect()
        if vts_connected:
            await self.vts_api.authenticate()
        
        obs_connected = await self.obs_client.connect()
        
        if not vts_connected:
            print("Warning: VTuber Studio not connected - visemes will be skipped")
        if not obs_connected:
            print("Warning: OBS not connected - using fallback audio tracking")
            
        return vts_connected or obs_connected  # At least one should work
    
    def add_news_item(self, audio_file: str, viseme_file: str, priority: Priority = Priority.NORMAL):
        """Add news item to queue"""
        item = NewsItem(audio_file, viseme_file, priority)
        # Priority queue uses tuple (priority_value, sequence_number, item)
        # Lower number = higher priority
        priority_value = 4 - priority.value  # Invert so URGENT=1, BREAKING=2, NORMAL=3
        self.sequence_number += 1
        self.news_queue.put((priority_value, self.sequence_number, item))
        print(f"Added news item: {audio_file} (Priority: {priority.name})")
    
    def add_breaking_news(self, audio_file: str, viseme_file: str):
        """Add breaking news (interrupts current playback)"""
        print("🚨 BREAKING NEWS ALERT 🚨")
        
        # Stop current playback
        self.stop_current_playback()
        
        # Add breaking news with highest priority
        self.add_news_item(audio_file, viseme_file, Priority.URGENT)
    
    def stop_current_playback(self):
        """Stop current audio/viseme playback"""
        # Stop OBS audio source
        if self.obs_client.authenticated:
            asyncio.create_task(self.obs_client.trigger_media_restart(self.audio_source_name))
        
        # Stop audio tracking
        self.audio_manager.stop_audio_tracking()
        self.current_item = None
        print("Current playback stopped")
    
    def load_viseme_data(self, viseme_file: str) -> List[Tuple[float, str]]:
        """Load viseme data from file"""
        try:
            with open(viseme_file, 'r') as f:
                lines = f.readlines()
            
            viseme_data = []
            for line in lines:
                line = line.strip()
                if line:
                    # Assuming format: timestamp viseme_type
                    # Example: "0.1 A", "0.2 E", etc.
                    parts = line.split()
                    if len(parts) >= 2:
                        timestamp = float(parts[0])
                        viseme = parts[1]
                        viseme_data.append((timestamp, viseme))
            
            return viseme_data
            
        except Exception as e:
            print(f"Error loading viseme data from {viseme_file}: {e}")
            return []
    
    async def play_news_item(self, item: NewsItem):
        """Play a single news item with synchronized audio and visemes"""
        print(f"Playing news item: {item.audio_file}")
        
        # Load viseme data
        viseme_data = self.load_viseme_data(item.viseme_file)
        
        # Set up audio in OBS
        audio_duration = 0
        if self.obs_client.authenticated:
            # Set the media source file and trigger playback
            await self.obs_client.set_media_source(self.audio_source_name, item.audio_file)
            await self.obs_client.trigger_media_restart(self.audio_source_name)
            audio_duration = self.audio_manager.start_audio_tracking(item.audio_file)
        else:
            # Fallback: just track duration without OBS
            audio_duration = self.audio_manager.start_audio_tracking(item.audio_file)
            print(f"OBS not available - simulating audio playback for {audio_duration:.2f}s")
        
        if audio_duration == 0:
            return
        
        # Synchronize visemes with audio
        start_time = time.time()
        viseme_index = 0
        
        while self.audio_manager.is_audio_playing() and viseme_index < len(viseme_data):
            current_time = time.time() - start_time
            
            # Check if it's time for the next viseme
            if viseme_index < len(viseme_data):
                viseme_timestamp, viseme_type = viseme_data[viseme_index]
                
                if current_time >= viseme_timestamp:
                    if self.vts_api.authenticated:
                        await self.vts_api.send_viseme(viseme_type)
                    else:
                        print(f"Viseme at {current_time:.2f}s: {viseme_type}")
                    viseme_index += 1
            
            await asyncio.sleep(0.01)  # Small delay to prevent CPU overload
        
        # Reset mouth to neutral position
        if self.vts_api.authenticated:
            await self.vts_api.send_viseme("")
        
        # Stop audio tracking
        self.audio_manager.stop_audio_tracking()
        print(f"Finished playing: {item.audio_file}")
    
    async def run_playback_loop(self):
        """Main playback loop"""
        print("Starting news playback loop...")
        
        while self.is_running:
            try:
                # Get next item from queue (blocks if empty)
                if not self.news_queue.empty():
                    priority_value, sequence_number, item = self.news_queue.get(timeout=1)
                    self.current_item = item
                    
                    await self.play_news_item(item)
                    
                    self.current_item = None
                    self.news_queue.task_done()
                else:
                    await asyncio.sleep(0.1)
                    
            except queue.Empty:
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"Error in playback loop: {e}")
                await asyncio.sleep(1)
    
    async def start(self):
        """Start the news streamer"""
        if not await self.initialize():
            print("Failed to initialize VTuber Studio connection")
            return
        
        self.is_running = True
        await self.run_playback_loop()
    
    async def stop(self):
        """Stop the news streamer"""
        self.is_running = False
        self.stop_current_playback()
        await self.vts_api.disconnect()
        await self.obs_client.disconnect()
        print("News streamer stopped")

# Test script
async def main():
    streamer = NewsStreamer()
    
    # Check if test files exist
    audio_dir = "output/audio"
    viseme_dir = "output/viseme"
    
    if not os.path.exists(audio_dir) or not os.path.exists(viseme_dir):
        print(f"Please ensure {audio_dir} and {viseme_dir} directories exist with test files")
        return
    
    # Add test news items
    test_items = [
        ("1.wav", "1.txt", Priority.NORMAL),
        ("2.wav", "2.txt", Priority.NORMAL),
        ("3.wav", "3.txt", Priority.NORMAL),
    ]
    
    for audio, viseme, priority in test_items:
        audio_path = os.path.join(audio_dir, audio)
        viseme_path = os.path.join(viseme_dir, viseme)
        
        if os.path.exists(audio_path) and os.path.exists(viseme_path):
            streamer.add_news_item(audio_path, viseme_path, priority)
        else:
            print(f"Missing files: {audio_path} or {viseme_path}")
    
    # Start the streamer
    try:
        # Run for a bit, then test breaking news
        streamer_task = asyncio.create_task(streamer.start())
        
        # Wait a bit then inject breaking news
        await asyncio.sleep(5)
        
        # Test breaking news injection
        breaking_audio = os.path.join(audio_dir, "2.wav")  # Use existing file for test
        breaking_viseme = os.path.join(viseme_dir, "2.txt")
        
        if os.path.exists(breaking_audio) and os.path.exists(breaking_viseme):
            streamer.add_breaking_news(breaking_audio, breaking_viseme)
        
        # Let it run for a while
        await asyncio.sleep(30)
        
    except KeyboardInterrupt:
        print("\nStopping streamer...")
    finally:
        await streamer.stop()

if __name__ == "__main__":
    print("VTuber News Streamer Tester")
    print("===========================")
    print(f"WSL → Windows setup - connecting to Windows host at {WINDOWS_HOST_IP}")
    print("Make sure VTuber Studio is running and API is enabled!")
    print("Make sure OBS is running with WebSocket server enabled!")
    print("Create a Media Source named 'NewsAudio' in OBS!")
    print("Press Ctrl+C to stop")
    print()
    
    asyncio.run(main())
