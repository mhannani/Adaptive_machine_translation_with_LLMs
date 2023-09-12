from typing import List
from langchain.prompts.chat import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate


class Prompt:
    """
    LLM Prompt construction class
    """

    def __init__(self, source_sentence: str, fuzzy_matches: List) -> None:
        """
        Prompt class constructor

        :param source_sentence str
            The source sentence to translate
        
        :param fuzzy_matches List
            List of fuzzy matches

        :return None
        """
        
        # source_sentence
        self.source_sentence: str = source_sentence

        # fuzzy_match
        self.fuzzy_matches: List = fuzzy_matches
    
    def __call__(self, source_language: str = "English", target_language: str = "Arabic") -> str:
        """
        Construct a promp given sentence, and fuzzy matches

        :param source_language str
            The source language
        
        :param target_language str
            The target langauge

        :return str
        """

        # Initialize the prompt list with a system message
        prompt = [{"role": "system", "content": f"Act like a good translator from {source_language} to {target_language}"}]

        # Iterate over fuzzy matches and add user and assistant messages
        for match in self.fuzzy_matches:
            # source sentence
            source_sentence = match["source_sentence"]

            # target sentence
            target_sentence = match["target_sentence"]

            # user message
            user_message = {"role": "user", "content": f"English: {source_sentence}"}
            
            # assistant message
            assistant_message = {"role": "assistant", "content": f"Arabic: {target_sentence}"}

            # append current user message
            prompt.append(user_message)

            # append current assistant message
            prompt.append(assistant_message)

        # Finally, add the user's original sentence to the prompt
        user_message = {"role": "user", "content": f"English: {self.source_sentence}"}

        # append the query sentence
        prompt.append(user_message)

        # return the constructed prompt
        return prompt

    def create(self, source_language: str = "English", target_language: str = "Arabic") -> str:
        """
        Create a prompt given source and target languages

        :param source_language str
            Source language
        :param target_language str
            Target language
        
        :return str
        """
        
        # source language
        source_language = self.config['languages']['source_language']

        # target language
        target_language = self.config['languages']['target_language']

        # assisstant template
        template = "Please translate from {source_language} to {target_language}."

        # create system message
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)


