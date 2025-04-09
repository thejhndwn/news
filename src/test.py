from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
import torch
import soundfile as sf
from huggingface_hub import login



login(token="")

# Load the processor and model
processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
## websites list npr , bcc, 
        
# Input text (your news snippet)
text = "Breaking news: Markets soar to new highs today!"

# Process the text
inputs = processor(text=text, return_tensors="pt")

# Use a speaker embedding (pre-trained, from a dataset)
speaker_embeddings = torch.randn(1, 512)  # Random for now; real embeddings need a dataset

# Generate speech
speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)

# Save to file
sf.write("news.wav", speech.numpy(), samplerate=16000)