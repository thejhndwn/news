
# Use a pipeline as a high-level helper
from transformers import pipeline
from pathlib import Path
import soundfile as sf
import torch
from datasets import load_dataset


class AudioGenerator:
    def __init__(self):
        self.pipe = pipeline("text-to-speech", model="microsoft/speecht5_tts")

        embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
        self.speaker_embedding = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

    def generate(self, audio_path: str, text = "Hello, this is a testing voice!"):
        audio = self.pipe(text, forward_params={"speaker_embeddings": self.speaker_embedding})

        sf.write(audio_path, audio["audio"], audio["sampling_rate"])

        print(f"Audio generated and saved as {audio_path}")
