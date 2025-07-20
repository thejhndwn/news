
class ScriptGenerator:
    def __init__(self):
        # initalize the models and etc.
        pass
    
    def generate(self, text, context = {}):
        # generate a script based on story and context
        # first pass, straight up script
        # second pass, add in buffering words
        # third pass, add in context
        print(f"Generating script for text: {text[:200]}...")
        return text[:200]