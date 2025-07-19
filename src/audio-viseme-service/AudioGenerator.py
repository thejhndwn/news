
# Use a pipeline as a high-level helper
from transformers import pipeline
from pathlib import Path
import soundfile as sf
import torch
from datasets import load_dataset


class AudioGenerator:
    def __init__(self, output_path):
        self.pipe = pipeline("text-to-speech", model="microsoft/speecht5_tts")
        self.audio_path = output_path 

        embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
        self.speaker_embedding = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

    def generate(self, uuid,  text = "Hello, this is a testing voice!"):
        audio = self.pipe(text, forward_params={"speaker_embeddings": self.speaker_embedding})

        sf.write(f"{self.audio_path}/{uuid}.wav", audio["audio"], audio["sampling_rate"])

        print(f"Audio generated and saved as {uuid}.wav")
