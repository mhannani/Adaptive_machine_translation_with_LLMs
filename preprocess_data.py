import os
from src.preprocess.preprocessor import Preprocessor
from src.helpers.get import parse_toml
from pathlib import Path


if __name__ == "__main__":

    # toml path
    toml_path: str = Path("./configs/ted_talks.toml")
    
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
