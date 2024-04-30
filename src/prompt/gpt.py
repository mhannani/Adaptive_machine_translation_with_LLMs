from typing import List
from langchain.prompts.chat import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate, AIMessagePromptTemplate

from src.translators.deepl_en_de import DeepL


class Prompt:
    """
    LLM Prompt construction class
    """

    def __init__(self, config: object, fuzzy_matches: List, deepl: DeepL = None) -> None:
        """
        Prompt class constructor

        :param source_sentence str
            The source sentence to translate

        :param fuzzy_matches List
            List of fuzzy matches

        :return None
        """

        # configuration object
        self.config = config

        # source language
        self.source_language = self.config['prompting']['source_language']

        # target language
        self.target_language = self.config['prompting']['target_language']

        # fuzzy_match
        self.fuzzy_matches: List = fuzzy_matches

        # DeepL
        self.deepl = deepl

    def create_gpt_prompt(self, request_sentence: str) -> str:
        """
        Create a prompt given source and target languages for GPT model

        :param request_sentence str
            Request sentence

        :return str
        """

        # assisstant template
        template = "Act like a good translator from {source_language} subtitles to {target_language} subtitles. Translate the following {source_language} sentence into {target_language}"

        # create system message
        system_message_prompt = SystemMessagePromptTemplate.from_template(
            template)

        # chat prompt template
        chat_messages = []

        # Iterate over fuzzy matches and add user and assistant messages
        for match in self.fuzzy_matches:

            # source sentence
            source_sentence = match["source_sentence"]

            # target sentence
            target_sentence = self.deepl.translate(source_sentence) if self.deepl is not None else match["target_sentence"]

            # human message template
            human_message_template = f"{source_sentence}"

            # human message
            human_message_prompt = HumanMessagePromptTemplate.from_template(
                human_message_template)

            # ai message template
            ai_message_template = f"{target_sentence}"

            # print("ai_message_template: ", ai_message_template)
            # ai message
            ai_message_prompt = AIMessagePromptTemplate.from_template(
                ai_message_template)

            # add to chat messages
            chat_messages.extend([human_message_prompt, ai_message_prompt])

        # user request message template
        user_message_template = "{text}"

        # user message
        user_message_prompt = HumanMessagePromptTemplate.from_template(
            user_message_template)

        # format message with kwargs
        user_message_prompt.format_messages(text=request_sentence)

        # add user request for translation
        chat_messages.append(user_message_prompt)

        # combine messages
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, *chat_messages])

        # format chat prompt
        chat_prompt = chat_prompt.format_messages(
            source_language=self.source_language, target_language=self.target_language, text=request_sentence)

        return chat_prompt
    
    def create_Llama_prompt(self, request_sentence: str) -> dict:
        """
        Creates Llama 2 prompt to work with Replicate

        :request_sentence str
            The provided user request sentence to translate

        :return 
        """

        # assisstant template
        llama_2_prompt = f"Act like a good translator from {self.source_language} subtitles to {self.target_language} subtitles. Translate the following {self.source_language} text into Arabic. Give me only the Arabic sentence, no Note , Translation, and how to prounounce it."

        # prompt
        prompt = """"""
        
        # Iterate over fuzzy matches and add user and assistant messages
        for match in self.fuzzy_matches:
            # source sentence
            source_sentence = match["source_sentence"]

            # target sentence
            target_sentence = match["target_sentence"]

            # add source sentence to the prompt
            prompt = prompt + f"[INST] {source_sentence} [/INST]\n"

            # add target sentence
            prompt = prompt + f"{target_sentence}\n"
        
        # prompt
        prompt = prompt + f"[INST] {request_sentence} [/INST]"

        return {"prompt": prompt, "system_prompt": llama_2_prompt}
