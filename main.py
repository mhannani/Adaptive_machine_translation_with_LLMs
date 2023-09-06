import os
import json
from dotenv import load_dotenv
from src.selectors.fuzzy import Fuzzy
from src.helpers.get import parse_toml
from src.prompt.gpt import Prompt
from src.translators.chatgpt import GPT


if __name__ == "__main__":
    # toml path
    toml_path: str = "./config/config.toml"
    
    # Load environment variables from .env file
    load_dotenv()

    # OpenAI API key
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    
    # parsing toml
    config = parse_toml(toml_path)

    # json_data_filepath
    json_data_filepath: str = os.path.join(config['data']['processed'], config['data']['json_output'])

    # Open the JSON file in read mode
    with open(json_data_filepath, 'r') as json_file:
        # Load JSON data from the file
        json_data = json.load(json_file)

    # Fuzzy utility
    fuzzy = Fuzzy(config, json_data)

    # source sentence
    source_sentence = "I'm going to take a ride into the cold heart of winter."

    # k fuzzy matches
    k_fuzzy_matches = fuzzy.get_top_k(sentence = source_sentence, k = 5)

    # creating prompt object
    prompt = Prompt(source_sentence, k_fuzzy_matches)

    # gpt prompt
    gpt_prompt = prompt()
    
    # gpt instance
    gpt: GPT = GPT(openai_api_key)

    output = gpt.translate(gpt_prompt)
    print("output: ", output) # لا يمكننا التنبؤ به ولا يمكننا التحكم فيه.