from src.content_service.news_aggregator_service.NewsArticle import NewsArticle   
from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer
import torch

class ScriptGenerator:
    def __init__(self, model = "Qwen/Qwen2-1.5B-Instruct"):
        # initalize the models and etc.
        self.model = model
        self.tokenizer = AutoTokenizer.from_pretrained(self.model)

        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        self.pipe = AutoModelForCausalLM.from_pretrained(
                self.model,
                torch_dtype="auto",
                device_map="auto",
                trust_remote_code=True,
                low_cpu_mem_usage=True
        )
    
    def generate(self, article: NewsArticle, context = {}):
        prompt = f"""
            Given this news article:
            Title: {article.title}
            Body: {article.full_text}
            Generate a news anchor script summarizing the key points. 
            Use a professional yet engaging tone, as if delivering the story on a television news broadcast. 
            Structure the script jumping straight into the main story details. 
            Keep it clear, concise, and suitable for a general audience.
            """ 
        messages = [
                {"role": "system", "content": "You are a script writer for a news station"},
                {"role": "user", "content": prompt}]

        text = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
                )

        model_inputs = self.tokenizer(
                text, 
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length = 2048
                )

        device = next(self.pipe.parameters()).device
        model_input = {k: v.to(device) for k, v in model_inputs.items()}

        with torch.no_grad():
            generated_ids = self.pipe.generate(
                    **model_input,
                    max_new_tokens=512,
                    min_new_tokens=50,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9,
                    repetition_penalty=1.1,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    use_cache=True
                    )

        input_length = model_input['input_ids'].shape[1]
        new_tokens = generated_ids[:, input_length:]

        response = self.tokenizer.batch_decode(
                new_tokens,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=True
                )
        return response[0] if response else ""
