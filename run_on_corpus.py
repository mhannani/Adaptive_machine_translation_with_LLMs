"""
Make prediction for all subtiles present in the data source 
and store predictions for persistence and avoiding cost of model 
invocation for every experiment conducted.

"""

import csv
import json
import os
from dotenv import load_dotenv
from tqdm import tqdm
from pathlib import Path

from src.helpers.get import parse_toml
from src.prompt.gpt import Prompt
from src.selectors.fuzzy import Fuzzy
from src.translators.chatgpt import GPT



if __name__ == "__main__":
    # toml path
    toml_path: str = Path("./configs/tico_19.toml")

    # Load environment variables from .env file
    load_dotenv()

    # OpenAI API key
    openai_api_key: str = "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"

    # parsing toml
    config = parse_toml(toml_path)

    # json_data_filepath
    json_data_filepath: str = os.path.join(
        config['data']['processed'], config['data']['json_output'])

    # Open the JSON file in read mode
    with open(json_data_filepath, 'r') as json_file:

        # Load JSON data from the file
        json_data = json.load(json_file)

    # Fuzzy utility
    fuzzy = Fuzzy(config, json_data)

    # Result root
    result_root = os.path.join(config['results']['root'])

    # CSV path
    pairs_csv_path = os.path.join(result_root, config['results']['pairs_csv'])

    with open(pairs_csv_path, 'a+', newline='') as csv_file:

        # Write the header row
        csv_writer = csv.writer(csv_file, delimiter='\t')

        # Write the data rows
        # csv_writer.writerow(['Source Sentence', 'Target Sentence', 'Predicted Sentence'])

        # Through all the corpus
        for data in tqdm(json_data, desc=f"Discovering corpus", ncols=100):

            # source sentence
            source_sentence = data["source_sentence"]

            # print(source_sentence)
            # break
            # source sentence
            target_sentence = data["target_sentence"]

            # k fuzzy matches
            sentence_itself, k_fuzzy_matches = fuzzy.get_top_k(
                sentence=source_sentence, k=5)
            
            # creating prompt object
            prompt = Prompt(config, k_fuzzy_matches)

            # gpt prompt
            gpt_prompt = prompt.create(source_sentence)

            # gpt instance
            gpt: GPT = GPT(config, openai_api_key)

            # get translation
            predicted_sentence = gpt.translate_with_tenacity(gpt_prompt)

            # write current row
            csv_writer.writerow([source_sentence, target_sentence, predicted_sentence])
