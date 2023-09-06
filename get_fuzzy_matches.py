import os
import json
from src.helpers.get import parse_toml
from src.selectors.fuzzy import Fuzzy


if __name__ == "__main__":
    # toml path
    toml_path: str = "./config/config.toml"
    
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
    k_fuzzy_matches = fuzzy.get_top_k(sentence="The weather is the last truly wild thing on Earth.", k = 5)

    # print 5 fuzzy matches
    print("k_fuzzy_matches: ", k_fuzzy_matches)
