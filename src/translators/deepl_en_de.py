import deepl


class DeepL:
    """
    DeepL encoder-decoder translator
    """

    def __init__(self, config: object, deepl_api_key: str) -> None:
        """
        Class constructor

        :param deepl_api_key str
            The DeepL api key

        :param config object
            The configuration object

        :return None
        """

        # DeepL api key
        self.deepl_api_key = deepl_api_key
    
        # dataset configuration
        self.config = config

        # target language
        self.target_language = config['data']['target_language']

        # DeepL translator instance
        self.translator = deepl.Translator(self.deepl_api_key)

    def translate(self, sentence: str) -> str:
        """
        Translate the given sentence to the traget language in the configuration file `self.config`

        :param sentence str
            The source sentence

        :return str
            The translated sentence
        """

        # request the API
        result = self.translator.translate_text(sentence, target_lang = self.target_language)
        
        return result.text
