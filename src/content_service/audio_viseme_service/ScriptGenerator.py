from content_service.news_aggregator_service.NewsArticle import NewsArticle   
import ollama
from transformers import AutoTokenizer

class ScriptGenerator:
    def __init__(self, model = "llama3.1:8b"):
        # initalize the models and etc.
        self.model = model
        tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B")
    
    def generate(self, article: NewsArticle, context = {}):
       prompt = f"""
            Given this news article:
            Title: {article.title}
            Body: {article.full_text}
            Generate a concise video narration script summarizing the key points. Structure it as:
            - Introduction (1–2 sentences)
            - Main events (3–5 key points, bullet points)
            - Conclusion (1–2 sentences)
            Keep it in a conversational tone suitable for a general audience.
            """ 
       try:
           response = ollama.generate(model = self.model, prompt = prompt)
           return response['response']
       except Exception as e:
           print("There was a problem generating the script")
           return "Error"
