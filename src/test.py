# from huggingface_hub import login
from production.AudioGenerator import AudioGenerator


AudioGenerator = AudioGenerator()
AudioGenerator.generate()
print("done")