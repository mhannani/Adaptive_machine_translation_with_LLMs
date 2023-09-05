import os
import openai
from typing import List
from dotenv import load_dotenv
import datetime


class GPT:
    """
    GPT as translator model
    """

    def __init__(self, openai_api_key: str, model: str = 'gpt-3.5-turbo', temperature: float = 0.0, max_tokens: int = 30) -> None:
        """
        Class constructor for GPT model as API.

        :param openai_api_key str
            OpenAI API key
        :param model str
            Model name
        :param temperature float
            Temperature
        :param max_tokens int
            Max tokens
        :param messages List
            Messages to pass to the model

        return None
        """

        # openai_api_key
        self.openai_api_key = openai_api_key

        # model name
        self.model = model

        # temperator
        self.temperature = temperature

        # max_tokens
        self.max_tokens = max_tokens

        # setting openai api key
        openai.api_key = self.openai_api_key

    def translate(self, messages: List = [{"role": "user", "content": "Hi!"}]):
        """
        Make the translation job

        :param messages List
            List of messages for model input

        :return dict
        """

        return openai.ChatCompletion.create(model=self.model, temperature=self.temperature, max_tokens=self.max_tokens, messages=messages)


# For testing purposes
if __name__ == "__main__":

    # Load environment variables from .env file
    load_dotenv()

    # OpenAI API key
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # gpt instance
    gpt = GPT(openai_api_key)

    # source_lang
    source_lang = "English"

    # target_lang
    target_lang = "Arabic"

    # source sentence
    source_sentence = "The weather is the last truly wild thing on Earth."

    # messages
    messages = [
        {"role": "user", "content": f"Translate the following {source_lang} sentence to {target_lang}"},
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
