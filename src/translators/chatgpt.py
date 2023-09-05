import os
import openai
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")


class GPT:
    """
    GPT as translator model
    """

    def __init__(self, model_name: str = 'gpt-3.5-turbo', temperator: float = 0.0, max_tokens: int = 30) -> None:
        """
        Class constructor for GPT model as API.

        param model_name str
            Model name
        param temeperator float
            Temperator
        param max_tokens int
            Max tokens
        param messages List
            Messages to pass to the model

        return None
        """

        # model name
        self.model_name = model_name

        # temperator
        self.temperator = temperator

        # max_tokens
        self.max_tokens = max_tokens


    def translate(self, messages: List = [{"role": "user", "content": "Hi!"}]):
        """
        Make the translation job
        """

        raise NotImplementedError


