import os
import openai
from typing import List
from dotenv import load_dotenv
import codecs
import datetime

# Load environment variables from .env file
load_dotenv()

# OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# setting


class GPT:
    """
    GPT as translator model
    """

    def __init__(self, model: str = 'gpt-3.5-turbo', temperature: float = 0.0, max_tokens: int = 30) -> None:
        """
        Class constructor for GPT model as API.

        param model str
            Model name
        :param temperature float
            Temperature
        :param max_tokens int
            Max tokens
        :param messages List
            Messages to pass to the model

        return None
        """

        # model name
        self.model = model

        # temperator
        self.temperature = temperature

        # max_tokens
        self.max_tokens = max_tokens

        # setting openai api key
        openai.api_key = openai_api_key

    def translate(self, messages: List = [{"role": "user", "content": "Hi!"}]):
        """
        Make the translation job

        :param messages List
            List of messages for model input

        :return dict
        """

        return openai.ChatCompletion.create(model=self.model, temperature=self.temperature, max_tokens=self.max_tokens, messages=messages)


if __name__ == "__main__":

    # gpt instance
    gpt = GPT()

    # source sentence
    source_sentence = "The weather is the last truly wild thing on Earth."

    # messages
    messages = [
        {"role": "user", "content": "Translate the following English sentence to Arabic:"},
        {"role": "assistant", "content": source_sentence},
        {"role": "user", "content": "Arabic:"},
    ]

    # invoke model
    output = gpt.translate(messages)

    # Get the current date and time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Specify the directory to save the file
    output_directory = "../../data/output_translations/"

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Define the filename with the timestamp
    filename = os.path.join(output_directory, f"translation_{timestamp}.txt")

    # translated text
    translated_text = output["choices"][0]["message"]["content"] # الطقس هو آخر شيء بريء حقا على وجه الأر

    # Write the translated text to the file
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"{source_sentence}, {translated_text}")
