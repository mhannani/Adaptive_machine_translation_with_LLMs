import os
import json
from pathlib import Path
from src.helpers.get import parse_toml
from src.selectors.fuzzy import Fuzzy
import sys


if __name__ == "__main__":

    # Check if there is at least one command-line argument
    if len(sys.argv) < 2:
        print("Usage: python get_fuzzy_matches.py <dataset_name> <lang>")

        # quit
        sys.exit(1)

    # Get the config name from the command-line argument
    dataset_name = sys.argv[1]

    # get the language name
    lang = sys.argv[2]

    # toml path
    toml_path: str = Path(f"./configs/{lang}/{dataset_name}.toml")
    
    # Ensure the toml file exists
    if not toml_path.exists():
        print(f"Config file '{dataset_name}.toml' not found at ./configs/{lang}, path: {toml_path}")

        # quit
        sys.exit(1)
        
    # parsing toml
    config = parse_toml(toml_path)

    # json data
    json_data_filepath: str = os.path.join(config['data']['processed'], config['data']['json_output'])

    # Open the JSON file in read mode
    with open(json_data_filepath, 'r') as json_file:
        # Load JSON data from the file
        json_data = json.load(json_file)

    # Fuzzy class instance
    fuzzy = Fuzzy(config, json_data)

    # 5-fuzzy matches
    k_fuzzy_matches = fuzzy.get_top_k(sentence="however she has symptoms quite similar to mine", k = 2)

    # print 5 fuzzy matches
    print("k_fuzzy_matches: ", k_fuzzy_matches)
