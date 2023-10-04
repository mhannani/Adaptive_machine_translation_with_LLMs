import openai
from typing import List
from tenacity import retry, stop_after_attempt, wait_fixed, wait_random_exponential
from langchain.schema.messages import AIMessage
import replicate


class Llama2:
    """
    Llama 2 as translator model
    """

    def __init__(self, config, replicate_api_key: str, model: str = 'llama-2-70b', temperature: float = 0.3, max_tokens: int = 50) -> None:
        """
        Class constructor for GPT model as API.

        :param config
            Configuration object
        :param replicate_api_key str
            Replicate API key
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

        # configuration object
        self.config = config

        # openai_api_key
        self.replicate_api_key: str = replicate_api_key

        self.models = {
            'llama-2-70b': 'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3'
        }

        # model name
        self.model: str = self.models[model]

        # temperator
        self.temperature: float = temperature

        # max_tokens
        self.max_tokens: int = max_tokens

    def translate_with_tenacity(self, chat_prompt: List) -> AIMessage:
        """
        Translate sentence using Chain-of-thoughts with Langchain

        :param chat_prompt List
            List of chat_prompt to the LLM

        :return AIMessage
        """

        # generate resposne
        llm_output = replicate.run(self.model, input = chat_prompt)

        # predicted sentence
        predicted_sentence = ""

        for item in llm_output:
            predicted_sentence = predicted_sentence + item

        return predicted_sentence
