import subprocess

class VisemeGenerator:
    def __init__(self):
        # Initialize any necessary resources or configurations
        pass

    def generate(self, audio_file_path, viseme_file_path):
        # Logic to generate visemes from the provided audio file
        print(f"Generating visemes for {audio_file_path}")
        # Placeholder for actual viseme generation logic

        subprocess.run(["rhubarb", "-o", viseme_file_path, audio_file_path], check=True)


        pass