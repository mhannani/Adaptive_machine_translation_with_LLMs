import json
import os
from pathlib import Path
import sys
from dotenv import load_dotenv
import openai
from src.evaluation.eval import Evaluator
from src.helpers.get import parse_toml
from src.selectors.fuzzy import Fuzzy
from src.utils.corpus_eval import evaluate_corpus


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

    evaluate_corpus(config)

    

        
