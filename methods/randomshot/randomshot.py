import random
import os

class RandomShotProcessor:
    
    def __init__(self, config, args):
        self.config = config
        self.args = args
        self.stats = {}

    def get_random_shots(self):

        with open(self.config["train"]["src"], "r") as f:
            src = [line.strip() for line in f.readlines()]

        with open(self.config["train"]["tgt"], "r") as f:
            tgt = [line.strip() for line in f.readlines()]

        indices = random.sample(range(len(src)), self.args.num_shots)
        src = [src[i] for i in indices]
        tgt = [tgt[i] for i in indices]

        return src, tgt


    def get_prompt(self, text):

        src_shots, tgt_shots = self.get_random_shots()

        shots = "\n\n".join(
            [
                f"{self.config['src_lang']}: {s}\n{self.config['tgt_lang']}: {t}"
                for s, t in zip(src_shots, tgt_shots)
            ]
        )

        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        file_path = os.path.join(current_dir, 'template.txt')
        
        # read template.txt to a string 
        with open(file_path, 'r') as file:
            template = file.read()
        
        template = template.replace("{src_lang}", self.config["src_lang"])
        template = template.replace("{tgt_lang}", self.config["tgt_lang"])
        template = template.replace("{num_shots}", str(self.args.num_shots))
        template = template.replace("{shots}", shots)
        template = template.replace("{text}", text)

        return template
    
    def get_translation(self, text):
        return text

    def get_stats(self):
        return self.stats