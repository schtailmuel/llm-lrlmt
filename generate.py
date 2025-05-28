import datetime
import argparse
import json
import time
import os

from methods.zeroshot.zeroshot import ZeroShotProcessor
from methods.randomshot.randomshot import RandomShotProcessor
from methods.fragments.fragments import FragmentsShotProcessor
from methods.pivoted.pivotedshot import PivotedShotProcessor

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

parser = argparse.ArgumentParser()
parser.add_argument("--language_pair", type=str, help="language pair", required=True)
parser.add_argument("--sentence", type=str, default=None, help="sentence to translate")
parser.add_argument("--method", type=str, required=True)
parser.add_argument("--limit", type=int, default=None, help="limit number of prompts")
parser.add_argument("--seed", type=int, default=24, help="seed")
parser.add_argument("--num_shots", type=int, default=3, help="seed")
args = parser.parse_args()

data = json.load(open("data.json"))

if args.language_pair not in data.keys():
    raise Exception(f"Language_pair not valid, choose from: {data.keys()}")

methods = {
    "zeroshot": ZeroShotProcessor,
    "randomshot": RandomShotProcessor,
    "pivoted": PivotedShotProcessor,
    "fragments": FragmentsShotProcessor
}

if args.method not in methods.keys():
    raise Exception(f"Method not valid, choose from: {', '.join(methods.keys())}")

config = data[args.language_pair]

mtd_cls = methods[args.method](config, args)

if args.sentence is not None:
    src_text = [args.sentence]
    tgt_text = [""]
else:
    with open(config["test"]["src"], "r") as f:
        src_text = [line.strip() for line in f.readlines()]

    with open(config["test"]["tgt"], "r") as f:
        tgt_text = [line.strip() for line in f.readlines()]


if args.limit is not None:
    src_text = src_text[:args.limit]
    tgt_text = tgt_text[:args.limit]

current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_dir = f"prompts/{args.language_pair}_{args.method} _{current_time}/gen"
os.makedirs(log_dir)

for i, (s, t) in enumerate(zip(src_text, tgt_text)):

    print(f"Generating {i+1}/{len(src_text)}...", end="\r")

    start_time = time.time()
    prompt = mtd_cls.get_prompt(s)
    end_time = time.time()

    with open(f"{log_dir}/{i}.txt", "w", encoding="utf-8") as f:
        f.write(prompt)

stats = mtd_cls.get_stats()
with open(f"{log_dir}/stats.json", "w", encoding="utf-8") as f:
    json.dump(stats, f, ensure_ascii=False, indent=4)

print(f"Done! {len(src_text)} prompts generated: {log_dir}")