import asyncio
import websockets
import json
import subprocess
import os
import uuid
from datetime import datetime

class VTubeStudioController:
    def __init__(self):
        self.websocket = None
        self.host_ip = self.get_windows_host_ip()
        self.port = 8001
        self.uri = f"ws://{self.host_ip}:{self.port}"
        self.auth_token = None
        self.plugin_name = "WSL Python Controller"
        self.plugin_developer = "Your Name"
        self.plugin_icon = None
        self.authenticated = False
        self.available_expressions = []
        self.current_model = None
        
    def get_windows_host_ip(self):
        """Get Windows host IP from WSL"""
        result = subprocess.run(['ip', 'route', 'show'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if 'default' in line:
                return line.split()[2]
        return "172.18.224.1"  # fallback
    
    def load_auth_token(self):
        """Load saved auth token from file"""
        try:
            with open('vtube_auth_token.txt', 'r') as f:
                self.auth_token = f.read().strip()
                print(f"Loaded saved auth token: {self.auth_token[:20]}...")
        except FileNotFoundError:
            print("No saved auth token found. Will need to authenticate.")
    
    def save_auth_token(self):
        """Save auth token to file"""
        with open('vtube_auth_token.txt', 'w') as f:
            f.write(self.auth_token)
        print("Auth token saved for future use.")
    
    async def connect(self):
        """Connect to VTube Studio"""
        try:
            self.websocket = await websockets.connect(self.uri)
            print(f"✓ Connected to VTube Studio at {self.uri}")
            return True
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            return False
    
    async def send_request(self, message_type, data=None):
        """Send a request to VTube Studio API"""
        if not self.websocket:
            print("Not connected to VTube Studio")
            return None
            
        request = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": str(uuid.uuid4()),
            "messageType": message_type
        }
        
        if data:
            request["data"] = data
            
        try:
            await self.websocket.send(json.dumps(request))
            response = await self.websocket.recv()
            return json.loads(response)
        except Exception as e:
            print(f"Error sending request: {e}")
            return None
    
    async def authenticate(self):
        """Handle authentication flow"""
        # Load any existing token
        self.load_auth_token()
        
        # Try to authenticate with existing token
        if self.auth_token:
            print("Trying to authenticate with saved token...")
            auth_response = await self.send_request("AuthenticationRequest", {
                "pluginName": self.plugin_name,
                "pluginDeveloper": self.plugin_developer,
                "authenticationToken": self.auth_token
            })
            
            if auth_response and auth_response.get("data", {}).get("authenticated"):
                print("✓ Authentication successful with saved token!")
                self.authenticated = True
                return True
            else:
                print("Saved token is invalid, requesting new one...")
        
        # Request new token
        print("Requesting authentication token...")
        token_response = await self.send_request("AuthenticationTokenRequest", {
            "pluginName": self.plugin_name,
            "pluginDeveloper": self.plugin_developer,
            "pluginIcon": self.plugin_icon
        })
        
        if not token_response or token_response.get("messageType") == "APIError":
            print("✗ Failed to request token")
            return False
        
        print("✓ Token requested! Please allow the plugin in VTube Studio.")
        print("Press Enter after allowing the plugin in VTube Studio...")
        input()
        
        # Now authenticate with the new token
        auth_response = await self.send_request("AuthenticationRequest", {
            "pluginName": self.plugin_name,
            "pluginDeveloper": self.plugin_developer,
            "authenticationToken": token_response["data"]["authenticationToken"]
        })
        
        if auth_response and auth_response.get("data", {}).get("authenticated"):
            print("✓ Authentication successful!")
            self.auth_token = token_response["data"]["authenticationToken"]
            self.save_auth_token()
            self.authenticated = True
            return True
        else:
            print("✗ Authentication failed")
            return False
    
    async def get_available_expressions(self):
        """Get list of available expressions"""
        if not self.authenticated:
            print("Not authenticated")
            return
            
        response = await self.send_request("ExpressionStateRequest")
        if response and response.get("data"):
            self.available_expressions = response["data"]["expressions"]
            print(f"Found {len(self.available_expressions)} expressions")
    
    async def get_current_model(self):
        """Get current model info"""
        if not self.authenticated:
            print("Not authenticated")
            return
            
        response = await self.send_request("CurrentModelRequest")
        if response and response.get("data"):
            self.current_model = response["data"]
            print(f"Current model: {self.current_model.get('modelName', 'Unknown')}")
    
    async def trigger_expression(self, expression_file, duration=3.0):
        """Trigger an expression"""
        if not self.authenticated:
            print("Not authenticated")
            return
            
        response = await self.send_request("ExpressionActivationRequest", {
            "expressionFile": expression_file,
            "active": True
        })
        
        if response and response.get("data", {}).get("expressionActivated"):
            print(f"✓ Triggered expression: {expression_file}")
            
            # Wait for duration, then deactivate
            await asyncio.sleep(duration)
            
            await self.send_request("ExpressionActivationRequest", {
                "expressionFile": expression_file,
                "active": False
            })
            print(f"✓ Deactivated expression: {expression_file}")
        else:
            print(f"✗ Failed to trigger expression: {expression_file}")
    
    async def list_expressions(self):
        """List all available expressions"""
        if not self.available_expressions:
            await self.get_available_expressions()
        
        print("\nAvailable expressions:")
        for i, expr in enumerate(self.available_expressions, 1):
            print(f"{i:2d}. {expr['file']} - {expr['name']}")
    
    async def expression_sequence(self, expressions, delay=1.0):
        """Play a sequence of expressions"""
        print(f"Starting expression sequence with {len(expressions)} expressions...")
        
        for i, expr in enumerate(expressions, 1):
            print(f"Step {i}/{len(expressions)}: {expr}")
            await self.trigger_expression(expr, duration=2.0)
            if i < len(expressions):  # Don't wait after the last expression
                await asyncio.sleep(delay)
        
        print("✓ Expression sequence completed!")
    
    def show_help(self):
        """Show available commands"""
        print("\n=== VTube Studio Controller Commands ===")
        print("help          - Show this help message")
        print("list          - List all available expressions")
        print("trigger <num> - Trigger expression by number from list")
        print("name <name>   - Trigger expression by name/file")
        print("model         - Show current model info")
        print("sequence      - Run a demo expression sequence")
        print("custom        - Create custom expression sequence")
        print("status        - Show connection status")
        print("quit          - Exit the program")
        print("=====================================\n")
    
    async def run_interactive(self):
        """Run interactive command loop"""
        print("=== VTube Studio Interactive Controller ===")
        print(f"Connecting to {self.uri}...")
        
        if not await self.connect():
            return
        
        if not await self.authenticate():
            return
        
        await self.get_available_expressions()
        await self.get_current_model()
        
        self.show_help()
        
        while True:
            try:
                command = input("VTube> ").strip().lower()
                
                if command == "quit" or command == "exit":
                    break
                elif command == "help":
                    self.show_help()
                elif command == "list":
                    await self.list_expressions()
                elif command.startswith("trigger "):
                    try:
                        num = int(command.split()[1])
                        if 1 <= num <= len(self.available_expressions):
                            expr = self.available_expressions[num-1]
                            await self.trigger_expression(expr['file'])
                        else:
                            print(f"Invalid number. Use 1-{len(self.available_expressions)}")
                    except (ValueError, IndexError):
                        print("Usage: trigger <number>")
                elif command.startswith("name "):
                    expr_name = command[5:]  # Remove "name "
                    await self.trigger_expression(expr_name)
                elif command == "model":
                    await self.get_current_model()
                elif command == "sequence":
                    # Demo sequence - adjust these to your actual expressions
                    demo_expressions = []
                    if len(self.available_expressions) >= 3:
                        demo_expressions = [
                            self.available_expressions[0]['file'],
                            self.available_expressions[1]['file'],
                            self.available_expressions[2]['file']
                        ]
                        await self.expression_sequence(demo_expressions)
                    else:
                        print("Need at least 3 expressions for demo sequence")
                elif command == "custom":
                    await self.create_custom_sequence()
                elif command == "status":
                    print(f"Connected: {self.websocket is not None}")
                    print(f"Authenticated: {self.authenticated}")
                    print(f"Model: {self.current_model.get('modelName', 'Unknown') if self.current_model else 'Unknown'}")
                    print(f"Expressions available: {len(self.available_expressions)}")
                elif command == "":
                    continue
                else:
                    print(f"Unknown command: {command}. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
        
        if self.websocket:
            await self.websocket.close()
        print("Disconnected from VTube Studio")
    
    async def create_custom_sequence(self):
        """Create a custom expression sequence"""
        print("\n=== Create Custom Expression Sequence ===")
        print("Enter expression numbers separated by spaces (e.g., 1 3 5)")
        print("Or type 'cancel' to cancel")
        
        await self.list_expressions()
        
        user_input = input("Expression numbers> ").strip()
        
        if user_input.lower() == 'cancel':
            return
        
        try:
            numbers = [int(x) for x in user_input.split()]
            expressions = []
            
            for num in numbers:
                if 1 <= num <= len(self.available_expressions):
                    expressions.append(self.available_expressions[num-1]['file'])
                else:
                    print(f"Invalid number: {num}")
                    return
            
            delay = input("Delay between expressions (seconds, default 1.0): ").strip()
            try:
                delay = float(delay) if delay else 1.0
            except ValueError:
                delay = 1.0
            
            await self.expression_sequence(expressions, delay)
            
        except ValueError:
            print("Invalid input. Please enter numbers separated by spaces.")

async def main():
    controller = VTubeStudioController()
    await controller.run_interactive()

if __name__ == "__main__":
    asyncio.run(main())
