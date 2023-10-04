"""
Make prediction for all subtiles present in the data source 
and store predictions for persistence and avoiding cost of model 
invocation for every experiment conducted.

"""

import csv
import json
import os
import sys
from dotenv import load_dotenv
from tqdm import tqdm
from pathlib import Path

from src.helpers.get import parse_toml
from src.prompt.gpt import Prompt
from src.selectors.fuzzy import Fuzzy
from src.translators.llama2 import Llama2


if __name__ == "__main__":

    # Check if there is at least one command-line argument
    if len(sys.argv) < 2:
        print("Usage: python preprocess_data.py <dataset_name>")

        # quit
        sys.exit(1)

    # Get the config name from the command-line argument
    dataset_name = sys.argv[1]

    # toml path
    toml_path: str = Path(f"./configs/{dataset_name}.toml")
    
    # Ensure the toml file exists
    if not toml_path.exists():
        print(f"Config file '{dataset_name}.toml' not found at ./configs/, path: {toml_path}")

        # quit
        sys.exit(1)

    # Load environment variables from .env file
    load_dotenv()

    # Replicate API key
    replicate_api_key: str = os.getenv("REPLICATE_API_TOKEN")

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

        if not os.path.exists(pairs_csv_path):
            # Write the data rows
            csv_writer.writerow(['Source Sentence', 'Target Sentence', 'Predicted Sentence'])

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
            llama_prompt = prompt.create_Llama_prompt(source_sentence)

            # Llama instance
            llama_2: Llama2 = Llama2(config, replicate_api_key)

            # get translation
            predicted_sentence = llama_2.translate_with_tenacity(llama_prompt)

            # write current row
            csv_writer.writerow([source_sentence, target_sentence, predicted_sentence])
