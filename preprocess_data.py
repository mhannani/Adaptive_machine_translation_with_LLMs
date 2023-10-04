import os
import sys
from src.preprocess.preprocessor import Preprocessor
from src.helpers.get import parse_toml
from pathlib import Path


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

    # parsing toml
    config = parse_toml(toml_path)

    # source_lang_data
    source_lang_data: str = Path(config['data']['raw']) / config['data']['source_language']

    # target_lang_data
    target_lang_data: str = Path(config['data']['raw']) / config['data']['target_language']

    # output_json_file
    output_json_file: str = Path(config['data']['processed']) / config['data']['json_output']

    # preprocessor
    preprocessor: Preprocessor = Preprocessor(source_lang_data, target_lang_data, output_json_file)

    # preprocessing
    preprocessor.fire()
