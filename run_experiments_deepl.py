"""Usage: run_experiment_deepl.py <dataset_name> <lang>"""


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
from src.translators.deepl_en_de import DeepL
import click

@click.command(context_settings=dict(help_option_names=['-h', '--help'], max_content_width=120))
@click.argument('dataset_name', type=str)
@click.argument('lang', type=str)
@click.argument('continue_exp', type=int, default = -1)


def main(dataset_name: str, lang: str, continue_exp: int) -> None:
    """
    Run Experimentation on dataset, using DeepL encoder-decoder model.

    :param dataset_name str
        Dataset name
    :param lang str
        Target Language
    :param model_name str
        The OpenAI model name
    :param continue_exp int
        From which sentence to continue the experiment
    
    :return None
    """

    print(f'!@@ Dataset: {dataset_name}, Language: {lang}, Model: DeepL @@!')

    # toml path
    toml_path: str = Path(f"./configs/{lang}/{dataset_name}.toml")

    # Load environment variables from .env file
    load_dotenv()

    # parsing toml
    config = parse_toml(toml_path)

    # OpenAI API key
    deepl_api_key: str = config['api_keys']['deepl']

    # DeepL instance
    deepl_instance = DeepL(config, deepl_api_key)

    # json_data_filepath
    json_data_filepath: str = os.path.join(
        config['data']['processed'], config['data']['json_output'])

    # three pairs resulst
    pairs_json_path = Path(config['data']['root']) / config['data']['json_path_deepl']

    # create dataset results root if not exists already
    pairs_json_path.parent.mkdir(parents=True, exist_ok=True)

    # Open the JSON file in read mode
    with open(json_data_filepath, 'r') as json_file:

        # Load JSON data from the file
        json_data = json.load(json_file)

    # Result root
    result_root = Path(config['results']['root']) / config['data']['target_language']

    # CSV path
    pairs_csv_path = result_root / f"temp_exp.model_deepL.dataset_{dataset_name}.{config['results']['pairs_csv']}"

    # create dataset results root if not exists already
    pairs_csv_path.parent.mkdir(parents=True, exist_ok=True)

    # Open the JSON file in append mode
    with open(pairs_json_path.as_posix(), 'a') as json_output_file:

        # Initialize a list to store results
        results_list = []

        with open(pairs_csv_path.as_posix(), 'a+', newline='') as csv_file:

            # Write the header row
            csv_writer = csv.writer(csv_file, delimiter='\t')

            # Write the data rows
            # csv_writer.writerow(['Source Sentence', 'Target Sentence', 'Predicted Sentence'])

            # Through all the corpus
            for data in tqdm(json_data[continue_exp + 1:6000], desc=f"Discovering corpus", ncols=100):

                # source sentence
                source_sentence = data["source_sentence"]

                # source sentence
                target_sentence = data["target_sentence"]

                # get translation
                predicted_sentence = deepl_instance.translate(source_sentence)

                # write current row
                csv_writer.writerow([source_sentence, target_sentence, predicted_sentence])

                # Ensure the data is written to the file after each iteration
                csv_file.flush()

                # Append current result to the list
                results_list.append({
                    "source_sentence": source_sentence,
                    "target_sentence": target_sentence,
                    "predicted_sentence": predicted_sentence
                })

            # Write results list to JSON file
            json_output_file.write(json.dumps(results_list) + '\n')

            # write to json file
            json_output_file.flush()

if __name__ == "__main__":

    # call the main function
    main()


    
