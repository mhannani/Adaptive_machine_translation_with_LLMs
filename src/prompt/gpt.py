from typing import List
from langchain.prompts.chat import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate, AIMessagePromptTemplate


class Prompt:
    """
    LLM Prompt construction class
    """

    def __init__(self, config: object, fuzzy_matches: List) -> None:
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

    def create(self, request_sentence: str) -> str:
        """
        Create a prompt given source and target languages

        :param request_sentence str
            Request sentence

        :return str
        """

        # assisstant template
        template = "Please provide high-quality {source_language} text for translation into {target_language}."

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
            target_sentence = match["target_sentence"]

            # human message template
            human_message_template = f"{source_sentence}"

            # human message
            human_message_prompt = HumanMessagePromptTemplate.from_template(
                human_message_template)

            # ai message template
            ai_message_template = f"{target_sentence}"

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
