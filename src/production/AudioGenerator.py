
import pyttsx3

class AudioGenerator:
    def __init__(self):
        self.engine = pyttsx3.init()

        # Set properties (optional)
        self.engine.setProperty('rate', 150)    # Speed of speech (words per minute)
        self.engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

        print("engine initialized")
    
    def generate(self, text = "Hello, this is a testing voice!"):
        # Save to an audio file
        output_file = "output2.mp3"  # Specify the file name
        self.engine.save_to_file(text, output_file)

        # Run the engine to process the file
        self.engine.runAndWait()

        print(f"Audio file saved as {output_file}")