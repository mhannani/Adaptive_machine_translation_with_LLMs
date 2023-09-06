import os
import json
import chainlit as cl
from dotenv import load_dotenv
from src.prompt.gpt import Prompt
from src.helpers.get import parse_toml
from src.selectors.fuzzy import Fuzzy
from src.translators.chatgpt import GPT


# toml path
toml_path: str = "./config/config.toml"

# Load environment variables from .env file
load_dotenv()

# OpenAI API key
openai_api_key: str = os.getenv("OPENAI_API_KEY")

# parsing toml
config = parse_toml(toml_path)

# json_data_filepath
json_data_filepath: str = os.path.join(
    config['data']['processed'], config['data']['json_output'])

# Open the JSON file in read mode
with open(json_data_filepath, 'r') as json_file:
    # Load JSON data from the file
    json_data = json.load(json_file)

# Fuzzy utility
fuzzy = Fuzzy(config, json_data)

# gpt instance
gpt: GPT = GPT(openai_api_key)

# top_k
top_k = 5

@cl.on_chat_start
async def main():
    # send back the final answer
    await cl.Message(content=f"I'm an LLM and I can translate between English and Arabic, start by giving a sentence in English ;)").send()

@cl.on_message
async def main(message: str):
    # Step 1: Getting top k fuzzy matches
    k_fuzzy_matches = fuzzy.get_top_k(sentence=message, k=top_k)

    await cl.Message(author="Fuzzy macthes", content=f"{k_fuzzy_matches}", indent=2).send()

    # Step 2: Creating LLM prompt
    # creating prompt object
    prompt = Prompt(message, k_fuzzy_matches)

    # gpt prompt
    gpt_prompt = prompt()

    await cl.Message(author="Prompt", content=f"{gpt_prompt}", indent=2).send()

    # call the GPT API
    output = gpt.translate(gpt_prompt)

    # send back the final answer
    await cl.Message(content=f"{output}").send()
