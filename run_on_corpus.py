"""Usage: run_on_corpus.py <dataset_name> <lang> <model_name> <k_fm>"""


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
import click

@click.command(context_settings=dict(help_option_names=['-h', '--help'], max_content_width=120))
@click.argument('dataset_name', type=str)
@click.argument('lang', type=str)
@click.argument('model_name', type=str)
@click.argument('k_fm', type=int)

def main(dataset_name: str, lang: str, model_name: str, k_fm: int):
    """
    Run Experimentation on dataset, language and with `km` fuzzy matches.

    :param dataset_name str
        Dataset name
    :param lang str
        Target Language
    :param model_name str
        The OpenAI model name
    
    :param k_fm int
        The Fuzzy matches to use for the experiment
    """

    print(f'!@@ Dataset: {dataset_name}, Language: {lang}, Model: {model_name}, k: {k_fm} @@!')

    # toml path
    toml_path: str = Path(f"./configs/{lang}/{dataset_name}.toml")

    # Load environment variables from .env file
    load_dotenv()

    # OpenAI API key
    openai_api_key: str = "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" 
    # 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 # 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

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

    # gpt instance
    gpt: GPT = GPT(config, openai_api_key)

    # Result root
    result_root = Path(config['results']['root'])

    # CSV path
    pairs_csv_path = result_root / f"exp.fm_{k_fm}.model_{gpt.model_name}.temp_{gpt.temperature}.dataset_{dataset_name}.{config['results']['pairs_csv']}"

    # create dataset results root if not exists already
    pairs_csv_path.parent.mkdir(parents=True, exist_ok=True)

    with open(pairs_csv_path.as_posix(), 'a+', newline='') as csv_file:

        # Write the header row
        csv_writer = csv.writer(csv_file, delimiter='\t')

        # Write the data rows
        # csv_writer.writerow(['Source Sentence', 'Target Sentence', 'Predicted Sentence'])

        # Through all the corpus
        for data in tqdm(json_data, desc=f"Discovering corpus", ncols=100):

            # source sentence
            source_sentence = data["source_sentence"]

            # source sentence
            target_sentence = data["target_sentence"]

            # k fuzzy matches
            _, k_fuzzy_matches = fuzzy.get_top_k(
                sentence=source_sentence, k=k_fm)
            
            # creating prompt object
            prompt = Prompt(config, k_fuzzy_matches)

            # gpt prompt
            gpt_prompt = prompt.create_gpt_prompt(source_sentence)

            # get translation
            predicted_sentence = gpt.translate_with_tenacity(gpt_prompt)

            # write current row
            csv_writer.writerow([source_sentence, target_sentence, predicted_sentence])


if __name__ == "__main__":

    # call the main function
    main()


    
