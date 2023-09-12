import os
import openai
from typing import List
from dotenv import load_dotenv
import datetime
from langchain.schema.messages import AIMessage
from langchain.chat_models import ChatOpenAI


class GPT:
    """
    GPT as translator model
    """

    def __init__(self, config, openai_api_key: str, model: str = 'gpt-3.5-turbo', temperature: float = 0.0, max_tokens: int = 50) -> None:
        """
        Class constructor for GPT model as API.

        :param config
            Configuration object
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

        # configuration object
        self.config = config

        # openai_api_key
        self.openai_api_key: str = openai_api_key

        # model name
        self.model: str = model

        # temperator
        self.temperature: float = temperature

        # max_tokens
        self.max_tokens: int = max_tokens

        # setting openai api key
        openai.api_key = self.openai_api_key

        # openAI API key
        self.openai_api_key = self.openai_api_key


    def translate(self, chat_prompt: List) -> AIMessage:
        """
        Translate sentence using Chain-of-thoughts with Langchain

        :param chat_prompt List
            List of chat_prompt to the LLM

        :return
        """

        # instantiate the chatOpenAI class
        chat_llm = ChatOpenAI(openai_api_key = self.openai_api_key)

        # generate resposne
        llm_output = chat_llm.predict_messages(chat_prompt)

        return llm_output.content
