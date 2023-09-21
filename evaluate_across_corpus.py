import json
import os
from dotenv import load_dotenv
import openai
from src.evaluation.eval import Evaluator
from src.helpers.get import parse_toml
from src.selectors.fuzzy import Fuzzy
from src.utils.corpus_eval import evaluate_corpus


if __name__ == "__main__":

    # toml path
    toml_path: str = "./config/config.toml"
    
    # Load environment variables from .env file
    load_dotenv()

    # OpenAI API key
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    
    # parsing toml
    config = parse_toml(toml_path)

    evaluate_corpus(config)

    

        
