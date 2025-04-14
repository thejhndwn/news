# from huggingface_hub import login
from production.AudioGenerator import AudioGenerator


AudioGenerator = AudioGenerator("/home/john-duan/Celia/news/output")
AudioGenerator.generate(11111)
print("done")