# 🧠 Compensating for Data with Reasoning: Low-Resource Machine Translation with LLMs

This repository contains the code and data for the paper [Compensating for Data with Reasoning: Low-Resource Machine Translation with LLMs](https://arxiv.org/abs/2505.22293)

## 🧩 Fragmentshot Method

In the paper, we introduce `Fragmentshot`, a novel prompting technique tailored for low-resource translation tasks.
To make this approach more accessible, we provide a standalone Python package:

👉 [fragmentshot](https://pypi.org/project/fragmentshot/) on PyPI

Use this package to:
  - Retrieve few-shot examples ("shots") for a given language pair and corpus
  - Seamlessly integrate the shots into your LLM prompts

## 📁 Repository Structure

- **`data/`**  
  Contains the datasets used for training and testing the translation models.

  The data is also available in the 🤗 Hugging Face Datasets repository:
  - [sfrontull/lld_valbadia-ita](https://huggingface.co/datasets/sfrontull/lld_valbadia-ita)
  - [sfrontull/lld_gherd-ita](https://huggingface.co/datasets/sfrontull/lld_gherd-ita)
  - [sfrontull/lld_valbadia-lld_gherd](https://huggingface.co/datasets/sfrontull/lld_valbadia-lld_gherd)

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

## 🌐 Translation

### 🔐 API Key Setup

**Note:** Before running the `translate.py` script, make sure you have set up the necessary API keys. You can do this in two ways:

- **Option 1: Define them in your environment**

```bash
export OPENAI_API_KEY='your_openai_api_key'
export DEEPSEEK_API_KEY='your_deepseek_api_key'
export TOGETHER_API_KEY='your_together_api_key'
```

- **Option 2: Use a `.env` file in the root of your project**  
  Add the following lines to the `.env` file:

```txt
OPENAI_API_KEY=<your_openai_api_key>
TOGETHER_API_KEY=<your_together_api_key>
DEEPSEEK_API_KEY=<your_deepseek_api_key>
``` 
### 💬 Usage

To translate all prompts in a given folder with a selected model, run:

```
python3 translate.py --prompts <path_to_prompts> --model <model_name> --language_pair <lang_pair>
```

**Arguments**:
  - <path_to_prompts>: Path to the prompt folder (e.g., prompts/lvb-ita/fragments)
  - <model_name>: One of the supported models: `gpt-3.5-turbo-0125`, `gpt-4o`, `o1-mini`, `Deepseek-R1`, `Llama-3.3`
  - <lang_pair>: Same as above

**Output**: A new folder with the model name containing a .json file of the translations.


## 📚 Citation

If you use this work, please cite the paper (preprint):

```bibtex
@misc{frontull:stroehle:2025,
      title={Compensating for Data with Reasoning: Low-Resource Machine Translation with LLMs}, 
      author={Samuel Frontull and Thomas Ströhle},
      year={2025},
      eprint={2505.22293},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2505.22293}, 
}
```