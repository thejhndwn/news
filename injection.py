import threading
import queue
import time

class StoryProcessor:
    def __init__(self):
        self.story_queue = queue.Queue()
        self.staging_queue = queue.Queue()
        self.running = True
        
    def input_listener(self):
        """Runs in separate thread to listen for user input"""
        while self.running:
            try:
                user_input = input("Enter 'inject:<story>' or 'quit': ")
                if user_input.lower() == 'quit':
                    self.running = False
                elif user_input.startswith('inject:'):
                    story = user_input[7:]  # Remove 'inject:' prefix
                    # Priority queue - injected stories go to front
                    temp_queue = queue.Queue()
                    temp_queue.put(('injected', story))
                    while not self.story_queue.empty():
                        temp_queue.put(self.story_queue.get())
                    self.story_queue = temp_queue
                    print(f"✅ Injected story: '{story[:50]}...'")
            except EOFError:
                break
    
    def pull_story(self):
        """Your existing story pulling logic"""
        # Simulate fetching a story
        time.sleep(2)  # Simulate API call delay
        return f"Auto-generated story at {time.time()}"
    
    def main_loop(self):
        """Your main processing loop"""
        while self.running:
            try:
                # Check if there's an injected story first
                if not self.story_queue.empty():
                    story_type, story = self.story_queue.get(timeout=0.1)
                    print(f"📝 Processing {story_type} story: {story}")
                else:
                    # Normal story pulling
                    story = self.pull_story()
                    print(f"📝 Processing auto story: {story}")
                
                # Add to staging (your existing logic)
                self.staging_queue.put(story)
                print(f"📤 Added to staging. Queue size: {self.staging_queue.qsize()}")
                
                time.sleep(1)  # Simulate processing time
                
            except queue.Empty:
                continue
            except KeyboardInterrupt:
                print("Received Ctrl+C, shutting down...")
                self.running = False
    
    def run(self):
        # Start input listener thread
        input_thread = threading.Thread(target=self.input_listener, daemon=True)
        input_thread.start()
        
        print("🚀 Story processor started. Type 'inject:<your_story>' to inject a story.")
        print("Press Ctrl+C to stop.")
        
        try:
            self.main_loop()
        finally:
            self.running = False
            print("👋 Shutting down...")

# Usage
if __name__ == "__main__":
    processor = StoryProcessor()
    processor.run()
