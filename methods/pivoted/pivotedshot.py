import os
import copy

from methods.fragments.fragments import FragmentsShotProcessor


class PivotedShotProcessor:

    def __init__(self, config, args):
        self.config = config
        self.args = args

        self.NUM_SRC_MID = 3
        self.NUM_MID_TGT = 3

        self.fragmentshotProcessor1 = self._create_processor(
            src=config["src-pivot"]["src"],
            tgt=config["src-pivot"]["tgt"],
            lang_pair=f"{config['src']}-{config['mid']}",
            tgt_lang=config["mid_lang"]
        )

        self.fragmentshotProcessor2 = self._create_processor(
            src=config["pivot-tgt"]["src"],
            tgt=config["pivot-tgt"]["tgt"],
            lang_pair=f"{config['mid']}-{config['tgt']}",
            src_lang=config["mid_lang"]
        )

    def _create_processor(self, src, tgt, lang_pair, src_lang=None, tgt_lang=None):
        new_config = self.config.copy()
        new_config["train"] = {"src": src, "tgt": tgt}

        if src_lang:
            new_config["src_lang"] = src_lang
        if tgt_lang:
            new_config["tgt_lang"] = tgt_lang

        new_args_dict = copy.deepcopy(vars(self.args))
        new_args_dict["language_pair"] = lang_pair
        new_args = type(self.args)(**new_args_dict)

        return FragmentsShotProcessor(new_config, new_args)

    def get_prompt(self, text):
        
        shots_source_pivot = self.fragmentshotProcessor1.get_fragment_shots(text)
        shots_str = ""
        for e in shots_source_pivot:
            if not e["examples"]:
                continue
            shots_str += f"Examples that illustrate the usage of **{e['fragment']}**:\n\n"
            for sp_ex in e["examples"][:self.NUM_SRC_MID]:
                shots_str += f"\t- {self.config['src_lang']}: {sp_ex['src_text']}\n"
                shots_str += (
                    f"\t- {self.config['mid_lang']}: {sp_ex['tgt_text']}\n\n"
                )

                shots_pivot_target = self.fragmentshotProcessor2.get_fragment_shots(sp_ex["tgt_text"])
                for pt_entry in shots_pivot_target:

                    # exclude identical match
                    examples = [x for x in pt_entry["examples"] if x["src_text"] != sp_ex["tgt_text"]]
                    if not examples:
                        continue
                    
                    shots_str += f"\tExamples that illustrate the usage of **{pt_entry['fragment']}**:\n\n"
                    for pt_ex in examples[:self.NUM_MID_TGT]:
                        shots_str += f"\t\t- {self.config['mid_lang']}: {pt_ex['src_text']}\n"
                        shots_str += f"\t\t- {self.config['tgt_lang']}: {pt_ex['tgt_text']}\n\n"

        shots_str = shots_str.strip()

        current_dir = os.path.dirname(os.path.abspath(__file__))

        file_path = os.path.join(current_dir, "template.txt")

        with open(file_path, "r") as file:
            template = file.read()

        # replace the placeholders in the template with the actual values
        template = template.replace("{src_lang}", self.config["src_lang"])
        template = template.replace("{tgt_lang}", self.config["tgt_lang"])
        template = template.replace("{shots}", shots_str)
        template = template.replace("{text}", text)

        return template

    def get_stats(self):

        stats = {
            f"{self.fragmentshotProcessor1.config['src']}-{self.fragmentshotProcessor1.config['mid']}": self.fragmentshotProcessor1.get_stats(),
            f"{self.fragmentshotProcessor2.config['mid']}-{self.fragmentshotProcessor2.config['tgt']}": self.fragmentshotProcessor2.get_stats(),
        }

        return stats
