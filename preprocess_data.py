import sys
from src.preprocess.preprocessor import TMXPreprocessor
from src.helpers.get import parse_toml
from pathlib import Path


if __name__ == "__main__":

    # Check if there is at least one command-line argument
    if len(sys.argv) < 2:
        print("Usage: python preprocess_data.py <dataset_name> <lang>")

        # quit
        sys.exit(1)

    # Get the config name from the command-line argument
    dataset_name = sys.argv[1]

    # get the target language
    language = sys.argv[2]

    # toml path
    toml_path: str = Path(f"./configs/{language}/{dataset_name}.toml")
    
    # Ensure the toml file exists
    if not toml_path.exists():
        print(f"Config file '{dataset_name}.toml' not found at ./configs/, path: {toml_path}")

        # quit
        sys.exit(1)

    # parsing toml
    config = parse_toml(toml_path)

    # tmux_file_path
    tmux_file_path: str = Path(config['data']['root']) / Path(config['data']['tmx_file'])

    # output_json_file
    output_json_file: str = Path(config['data']['processed']) / config['data']['json_output']

    # source langugae
    source_language: str = config['data']['source_language']

    # target language
    target_language: str = config['data']['target_language']

    # preprocessor
    preprocessor: TMXPreprocessor = TMXPreprocessor(tmux_file_path, output_json_file, source_language, target_language)

    # preprocessing
    preprocessor.fire()
