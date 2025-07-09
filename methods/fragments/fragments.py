import os
import re
import random

from fragmentshot.retriever import FragmentShotsRetriever

class FragmentsShotProcessor:

    def __init__(self, config, args):
        self.config = config
        self.args = args
        self.num_shots = args.num_shots

        self.stats = {
            "fragments": [],
            "not_found": [],
            "coverage": [],
            "num_shots_used": [],
            "num_shots_found": [],
        }

        with open(self.config["train"]["src"], "r") as f:
            src = [line.strip() for line in f.readlines()]

        with open(self.config["train"]["tgt"], "r") as f:
            tgt = [line.strip() for line in f.readlines()]

        self.retriever = FragmentShotsRetriever(src, tgt, max_fragment_size=7, overlaps=False)

    def get_fragment_shots(self, text):        
        result = self.retriever.get_fragment_shots(text)

        self.stats["coverage"].append((result['num_words'] - len(result['unknown'])) / result['num_words'])
        self.stats["fragments"].append([x['fragment'] for x in result['shots']])
        self.stats["num_shots_used"].append(sum([len(x['examples']) for x in result['shots'][:self.num_shots]]))
        self.stats["num_shots_found"].append(sum([len(x['examples']) for x in result['shots']]))
        self.stats["not_found"].append(result['unknown'])

        return result['shots']

    def get_prompt(self, text):
        shots = self.get_fragment_shots(text)
        
        shots_str = ""
        for e in shots:
            shots_str += f"Examples that illustrate the usage of **{e['fragment']}**:\n\n"
            for t in e["examples"][:self.num_shots]:
                shots_str += f"\t - {self.config['src_lang']}: {t['src_text']}\n"
                shots_str += f"\t - {self.config['tgt_lang']}: {t['tgt_text']}\n\n"

        shots_str = shots_str.strip()

        current_dir = os.path.dirname(os.path.abspath(__file__))

        file_path = os.path.join(current_dir, "template.txt")

        with open(file_path, "r") as file:
            template = file.read()

        template = template.replace("{src_lang}", self.config["src_lang"])
        template = template.replace("{tgt_lang}", self.config["tgt_lang"])
        template = template.replace("{shots}", shots_str)
        template = template.replace("{text}", text)

        return template

    def get_stats(self):

        avg_coverage = sum(self.stats["coverage"]) / len(self.stats["coverage"])
        avg_shots_found = sum(self.stats["num_shots_found"]) / len(self.stats["num_shots_found"])
        avg_shots_used = sum(self.stats["num_shots_used"]) / len(self.stats["num_shots_used"])

        win_stats = {}
        win_separate_stats = {}
        for i in range(1, 9):
            win_stats[i] = sum(
                [
                    1
                    for ws in self.stats["fragments"]
                    for w in ws
                    if len(w.split()) == i
                ]
            )
            win_separate_stats[i] = [
                len([w for w in ws if len(w.split()) == i])
                for ws in self.stats["fragments"]
            ]

        return {
            "coverage": {
                "average": avg_coverage,
                "raw": self.stats["coverage"],
                "count": {str(i): win_separate_stats[i] for i in range(1, 9)},
            },
            "shots": {
                "average": {
                    "found": avg_shots_found, 
                    "used": avg_shots_used
                }, 
                "raw": {
                    "found": self.stats["num_shots_found"], 
                    "used": self.stats["num_shots_used"]
                }
            },
            "fragments": {
                "count": {str(i): win_stats[i] for i in range(1, 9)},
                "raw": self.stats["fragments"],
                "not_found": self.stats["not_found"],
            },
        }
