import openai
from typing import List
from tenacity import retry, stop_after_attempt, wait_fixed, wait_random_exponential
from langchain.schema.messages import AIMessage
from langchain.chat_models import ChatOpenAI


class GPT:
    """
    GPT as translator model
    """

    def __init__(self, config, openai_api_key: str, model_name: str = 'gpt-3.5-turbo', temperature: float = 0.3, max_tokens: int = 50) -> None:
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
        self.model_name: str = model_name

        # temperator
        self.temperature: float = temperature

        # max_tokens
        self.max_tokens: int = max_tokens

        # setting openai api key
        openai.api_key = self.openai_api_key

        # openAI API key
        self.openai_api_key = self.openai_api_key

        # instantiate the chatOpenAI class
        self.chat_llm = ChatOpenAI(openai_api_key = self.openai_api_key, model_name = self.model_name, temperature = self.temperature)

    def translate(self, chat_prompt: List) -> AIMessage:
        """
        Translate sentence using Chain-of-thoughts with Langchain

        :param chat_prompt List
            List of chat_prompt to the LLM

        :return AIMessage
        """

        # generate resposne
        llm_output = self.chat_llm.predict_messages(chat_prompt)

        return llm_output.content

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def translate_with_tenacity(self, chat_prompt: List) -> AIMessage:
        """
        Translate sentence using Chain-of-thoughts with Langchain

        :param chat_prompt List
            List of chat_prompt to the LLM

        :return AIMessage
        """

        # generate resposne
        llm_output = self.chat_llm.predict_messages(chat_prompt)

        return llm_output.content