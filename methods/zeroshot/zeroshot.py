import os

class ZeroShotProcessor:
    
    def __init__(self, config, _):
        self.config = config
        self.stats = {}

    def get_prompt(self, text):

        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        file_path = os.path.join(current_dir, 'template.txt')
        
        # read template.txt to a string 
        with open(file_path, 'r') as file:
            template = file.read()
        
        template = template.replace("{src_lang}", self.config["src_lang"])
        template = template.replace("{tgt_lang}", self.config["tgt_lang"])
        template = template.replace("{text}", text)

        return template
    
    def get_translation(self, text):
        return text

    def get_stats(self):
        return self.stats
