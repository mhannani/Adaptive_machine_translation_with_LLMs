import os
import json
import chainlit as cl
from tabulate import tabulate
from dotenv import load_dotenv
from src.prompt.gpt import Prompt
from src.helpers.get import parse_toml
from src.selectors.fuzzy import Fuzzy
from src.translators.chatgpt import GPT
from src.evaluation.eval import Evaluator
from src.utils.clean import clean


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
    await cl.Message(author="Translator", content=f"I'm an LLM and I can translate between English and Arabic, start by giving a sentence in English ;)").send()

@cl.on_message
async def main(message: str):
    # res = await cl.AskUserMessage(content="What is your name?", timeout=10).send()
    # if res:
    #     await cl.Message(
    #         content=f"Your name is: {res['content']}",
    #     ).send()

    # reference sentence
    reference_sentence = None

    # splittable
    splittable = False

    if "|" in message:
        splittable = True

        parts = message.split("|")
        message = parts[0].strip()

        reference_sentence = parts[1].strip()

    # Step 1: Getting top k fuzzy matches
    sentence_itself, k_fuzzy_matches = fuzzy.get_top_k(sentence=message, k=top_k)

    await cl.Message(author="Fuzzy macthes", content=f"{k_fuzzy_matches}", indent=2).send()

    # Step 2: Creating LLM prompt
    # creating prompt object
    prompt = Prompt(message, k_fuzzy_matches)

    # gpt prompt
    gpt_prompt = prompt()

    await cl.Message(author="Prompt", content=f"{gpt_prompt}", indent=2).send()

    # call the GPT API
    predicted_sentence = gpt.translate(gpt_prompt)

    # cleaned predicted sentence
    cleaned_predicted_sentence = clean(predicted_sentence)

    # send back the final answer
    await cl.Message(author="Translator", content=f"{cleaned_predicted_sentence}").send()

    try:
        # reference sentence
        if reference_sentence is None:
            reference_sentence = sentence_itself[0]['target_sentence']

    except:
        # we couldn't retreive the reference sentence
        pass
    

    if reference_sentence is not None:
        print("reference_sentence, [predicted_sentence]: ", reference_sentence, [predicted_sentence])
        # evaluation
        evaluator = Evaluator(reference_sentence, [predicted_sentence])

        # calculate metrics
        all_scores = evaluator.all_score()

        # Convert the dictionary into a list of tuples
        table_data = [(metric, score) for metric, score in all_scores.items()]

        # Create the table as a string
        table = tabulate(table_data, headers=["Metric", "Score"], tablefmt="github")

        await cl.Message(author="Evaluator", content=f"{reference_sentence}").send()
        await cl.Message(author="Evaluator", content=f"{table}").send()

    if reference_sentence is None and not splittable:
        await cl.Message(author="Evaluator", content=f"No reference sentence found, please use `'|'` when prompting as seperator: Ex: SENTENCE_TO_BE_TRANSLATED|REFERENCE_SENTENCE ").send()
