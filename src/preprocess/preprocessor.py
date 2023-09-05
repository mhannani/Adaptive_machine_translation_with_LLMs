class Preprocessor:
    """
    Preprocess the raw data as .txt files to json to be exploitable for getting fuzzing matches.
    """

    def __init__(self, source_lang_data: str, target_lang_data: str):
        """
        Class constructor for the Preprocessor class

        :param source_lang_data str
            The source language data filepath
        
        :param target_lang_data str
            The target language data filepath

        :return None
        """

        # source language data
        self.source_lang_data = source_lang_data

        # target_lang_data
        self.target_lang_data = target_lang_data

    def fire(self):
        """
        Fire preprocessing task


        """

        raise NotImplementedError

