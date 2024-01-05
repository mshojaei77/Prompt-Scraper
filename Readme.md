# Midjourney Prompt Scrapper

## Overview

This project involves the extraction, processing, and transformation of Midjourney prompts obtained from [https://prompthero.com/midjourney-prompts](https://prompthero.com/midjourney-prompts). The goal is to create a dataset suitable for training language models, specifically tailored for image generation prompts.

## Project Structure

The project consists of four Python scripts:

1. **link_extracter.py**
    - **Description:** Scrapes prompt links from the Midjourney prompts website using Selenium and BeautifulSoup.
    - **Dependencies:** `csv`, `BeautifulSoup`, `selenium`

2. **text_extracter.py**
    - **Description:** Fetches text content from the extracted prompt links, considering rate-limiting and retries.
    - **Dependencies:** `csv`, `requests`, `BeautifulSoup`, `time`, `HTTPAdapter`, `Retry`

3. **addsubject.py**
    - **Description:** Identifies main subjects in the prompts using spaCy and NLTK, then replaces placeholders with these subjects.
    - **Dependencies:** `csv`, `spacy`, `nltk`

4. **convert2json.py**
    - **Description:** Converts the processed CSV data into a JSON format suitable for training a language model.
    - **Dependencies:** `csv`, `json`

## Usage

1. **Clone the Repository:**
    ```bash
    git clone [repository_url]
    cd Midjourney-Prompts-Project
    ```

2. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Scripts:**
    ```bash
    python link_extracter.py
    python text_extracter.py
    python addsubject.py
    python convert2json.py
    ```

4. **Generated Files:**
    - `prompt_links.csv`: Contains the extracted prompt links.
    - `partial_prompt_texts.csv`: Contains text extracted from the prompt links.
    - `prompts_with_subject.csv`: Contains prompts with identified subjects.
    - `prompts_with_subject.jsonl`: JSON file suitable for language model training.

## Hugging Face Dataset Card

Explore the dataset on Hugging Face: [Midjourney Art Prompts](https://huggingface.co/datasets/mshojaei77/Midjourney-Art-Prompts)

## Dataset Usage

The generated JSON file is specifically formatted for fine-tuning models using Hugging Face's Transformers library, such as ChatGPT. The CSV files, on the other hand, can be used for training or fine-tuning other Language Model Models (LLMs).

## Acknowledgments

- The [prompthero.com](https://prompthero.com) website for providing the Midjourney prompts.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
