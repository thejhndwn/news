
# Use a pipeline as a high-level helper
from transformers import pipeline
from pathlib import Path
import soundfile as sf
import torch
from datasets import load_dataset
import numpy as np

class AudioGenerator:
    def __init__(self, tmp_dir):
        self.tmp_dir = tmp_dir
        self.pipe = pipeline("text-to-speech", model="microsoft/speecht5_tts")

        embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
        self.speaker_embedding = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

    def generate_long_audio(self, text: str, audio_path: str):
        # split text up, smartly (not splitting words)
        # TODO: remove shortener
        text = text[:1000]

        words = text.split()
        splits = [words[i:i+50] for i in range(0, len(words), 50)]
        splits = [' '.join(split) for split in splits]
        # generate audio per split and save
        audios = []
        for split in splits:
            audio = self.pipe(split, forward_params = {"speaker_embeddings": self.speaker_embedding})
            audios.append(audio["audio"])

        # stitch audio together and save, delete tmp files
        combined_audio = np.concatenate(audios)
        sf.write(audio_path, combined_audio, samplerate = 16000)
