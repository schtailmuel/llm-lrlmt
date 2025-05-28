# 🧠 Compensating for Data with Reasoning: Low-Resource Machine Translation with LLMs

This repository contains the code and data for the paper:  
**_“Compensating for Data with Reasoning: Low-Resource Machine Translation with LLMs”_**

## 📁 Repository Structure

- **`data/`**  
  Contains the datasets used for training and testing the translation models.

- **`data.json`**  
  Configuration file mapping each language pair to its associated corpus and test files.

- **`generate.py`**  
  Script to generate prompts using one of four methods:
  - `zeroshot`
  - `randomshot`
  - `fragments`
  - `pivoted`

- **`translate.py`**  
  Script to translate the prompts using selected LLMs via API access.

---

## 🛠️ Setup

Make sure you have the required dependencies installed:

```
pip install -r requirements.txt
```

Also, ensure that your API keys for the relevant services (OpenAI, DeepSeek, Together) are set as environment variables or stored in a .env file (if applicable).

## 📄 Generate Prompts

To generate prompts for a specific language pair and method, run:

```
python3 generate.py --language_pair <lang_pair> --method <method>
```

**Arguments**:
  - <lang_pair>: Language pair to translate (e.g., lvb-ita, lgh-ita, lvb-lgh)
  - <method>: Prompting method (zeroshot, randomshot, fragments, or pivoted)

**Output**: A new folder in prompts/ containing the generated prompt files.

## 🌐 Translate Prompts

To translate all prompts in a given folder with a selected model, run:

```
python3 translate.py --prompts <path_to_prompts> --model <model_name> --language_pair <lang_pair>
```

**Arguments**:
  - <path_to_prompts>: Path to the prompt folder (e.g., prompts/lvb-ita/fragments)
  - <model_name>: One of the supported models: `gpt-3.5-turbo-0125`, `gpt-4o`, `o1-mini`, `Deepseek-R1`, `Llama-3.3`
  - <lang_pair>: Same as above

**Output**: A new folder with the model name containing a .json file of the translations.