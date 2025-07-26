
# Use a pipeline as a high-level helper
from transformers import pipeline
from pathlib import Path
import soundfile as sf
import torch
from datasets import load_dataset
import numpy as np

from kokoro import KPipeline

class AudioGenerator:
    def __init__(self, tmp_dir):
        self.tmp_dir = tmp_dir
        self.pipe = KPipeline(lang_code="a")

    def generate_long_audio(self, text: str, audio_path: str):
        generator = self.pipe(text, voice='af_heart')
        segments = [ x for (gs,ps,x )in generator]
        final_audio = np.concatenate(segments)
        sf.write(audio_path, final_audio, samplerate = 24000) 
