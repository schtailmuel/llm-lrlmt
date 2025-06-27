import argparse
import random
import datetime
import json
import os
import re

from openai import OpenAI
from together import Together

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

parser = argparse.ArgumentParser()
parser.add_argument("--prompts", type=str, help="prompts folder", required=True)
parser.add_argument("--model", type=str, default="gpt-3.5-turbo-0125", help="model")
parser.add_argument("--output", type=str, default=None, help="output folder")
parser.add_argument("--limit", type=int, default=200, help="seed")
parser.add_argument("--seed", type=int, default=24, help="seed")
args = parser.parse_args()


if args.model.lower().startswith("deepseek"):
    client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
elif args.model.lower().startswith("llama"):
    client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
else:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


prompts_dir = os.path.join(args.prompts, "gen")

def read_prompt(i):
    with open(os.path.join(prompts_dir, f"{i}.txt"), "r") as f:
        return f.read().strip()

idx = sorted(
    [int(os.path.splitext(f)[0]) for f in os.listdir(prompts_dir) if f.endswith(".txt")]
)

idx = idx[:args.limit] if args.limit > 0 else idx

if args.output is None:
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_dir = f"{args.prompts}/{args.model}_{current_time}"
    os.makedirs(log_dir)
else:
    log_dir = args.output

print("DIR:", log_dir)

tgt_gen = []
total_cost = 0
start_time = datetime.datetime.now()

for _i, id in enumerate(idx):

    if os.path.exists(f"{log_dir}/{id}.json"):
        print(f"Skipping {id}...")
        continue    

    prompt = read_prompt(id)

    print(f"Translating {_i}/{len(idx)}...", end="\r")

    try:

        query_start = datetime.datetime.now()
        completion = client.chat.completions.create(
            model=args.model,
            messages=[{"role": "user", "content": prompt}],
            seed=args.seed,
        )
        
        output = completion.choices[0].message.content
        query_end = datetime.datetime.now()
        
        data = {
            "output": output,
            "start": query_start.isoformat(),
            "end": query_end.isoformat(),
            "duration": (query_end - query_start).total_seconds(),
        } 

        with open(f"{log_dir}/{id}.json", "w", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    data,
                    ensure_ascii=False,
                    indent=4,
                )
            )
        
        tgt_gen.append(output)

    except Exception as e:
        data["error"] = str(e)

