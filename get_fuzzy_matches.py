import os
import json
from pathlib import Path
from src.helpers.get import parse_toml
from src.selectors.fuzzy import Fuzzy


if __name__ == "__main__":

    # toml path
    toml_path: str = Path("./configs/ted_talks.toml")
    
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
    k_fuzzy_matches = fuzzy.get_top_k(sentence="however she has symptoms quite similar to mine", k = 5)

    # print 5 fuzzy matches
    print("k_fuzzy_matches: ", k_fuzzy_matches)
