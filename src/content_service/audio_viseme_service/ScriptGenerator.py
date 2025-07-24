from content_service.news_aggregator_service.NewsArticle import NewsArticle   
from transformers import pipeline
from transformers import AutoTokenizer

class ScriptGenerator:
    def __init__(self, model = "Qwen/Qwen2.5-7B-Instruct"):
        # initalize the models and etc.
        self.model = model
        self.pipe = pipeline(
                "text-generation",
                model=self.model,
                torch_dtype="auto",
                device_map="auto"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(self.model)
    
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
        messages = [{"role": "user", "content": prompt}]
        response = self.pipe(messages,
                             max_new_tokens = 1000,
                             temperature = 0.7,
                             do_sample = True
                             )


        return response[0]['generated_text'][-1]['content']
