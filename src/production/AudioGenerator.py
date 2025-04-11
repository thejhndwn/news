
# Use a pipeline as a high-level helper
from transformers import pipeline
from pathlib import Path
import soundfile as sf
import torch
from datasets import load_dataset


class AudioGenerator:
    def __init__(self):
        self.pipe = pipeline("text-to-speech", model="microsoft/speecht5_tts")
        self.root_dir = Path(__file__).resolve().parents[2]  # go up from /src/production
        self.audio_file = self.root_dir / "output" / "audio" 

        embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
        self.speaker_embedding = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

    def generate(self, uuid,  text = "Hello, this is a testing voice!"):
        audio = self.pipe(text, forward_params={"speaker_embeddings": self.speaker_embedding})

        sf.write(f"{uuid}.wav", audio["audio"], audio["sampling_rate"])

        print("Audio generated and saved as output.wav")
