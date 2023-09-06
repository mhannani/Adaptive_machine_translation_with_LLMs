import os
import json
from typing import List
from nltk.tokenize import word_tokenize


class Preprocessor:
    """
    Preprocess the raw data as .txt files to json to be exploitable for getting fuzzing matches.
    """

    def __init__(self, source_lang_data: str, target_lang_data: str, output_json_file: str) -> None:
        """
        Class constructor for the Preprocessor class

        :param source_lang_data str
            The source language data filepath
        
        :param target_lang_data str
            The target language data filepath

        :param output_json_file str
            The target language data filepath

        :return None
        """

        # source language data
        self.source_lang_data: str = source_lang_data

        # target_lang_data
        self.target_lang_data: str = target_lang_data

        # output JSON file
        self.output_json_file: str = output_json_file


    def fire(self, tokenize = False) -> None:
        """
        Fire preprocessing task

        :param tokenize bool
            Whether to store the tokenized sentence along with the sentence itself or not

        :return None

        """

        # Check if both source and target language data files exist
        if not os.path.exists(self.source_lang_data) or not os.path.exists(self.target_lang_data):
            raise FileNotFoundError("One or both of the data files do not exist.")

        # Initialize a list to store the JSON data
        json_data: List = []

        # Read data from source and target language files
        with open(self.source_lang_data, 'r', encoding='utf-8') as source_file, open(self.target_lang_data, 'r', encoding='utf-8') as target_file:
            for i, (source_sentence, target_sentence) in enumerate(zip(source_file, target_file)):
                # Remove leading/trailing whitespace and newline characters
                source_sentence: str = source_sentence.strip()
                target_sentence: str = target_sentence.strip()

                if tokenize:
                    # Tokenize the source langauge sentence
                    en_tokenized: List = word_tokenize(source_sentence)

                    # Tokenize the source langauge sentence
                    ar_tokenized: List = word_tokenize(target_sentence)

                    # Create a JSON entry
                    entry: dict = {
                        "key": i,
                        "source_sentence": source_sentence,
                        "en_tokenizd": en_tokenized,
                        "target_sentence": target_sentence,
                        "ar_tokenized": ar_tokenized
                    }
                else:
                    # Create a JSON entry
                    entry: dict = {
                        "key": i,
                        "source_sentence": source_sentence,
                        "target_sentence": target_sentence,
                    }

                # Append the entry to the JSON data list
                json_data.append(entry)

        # Write the JSON data to the output JSON file
        with open(self.output_json_file, 'w', encoding='utf-8') as json_output:
            json.dump(json_data, json_output, ensure_ascii=False, indent=4)


# for testing purposes
if __name__ == "__main__":

    # source_lang_data
    source_lang_data: str = "../../data/raw/OpenSubtitles.ar-en-small.en.txt"

    # target_lang_data
    target_lang_data: str = "../../data/raw/OpenSubtitles.ar-en-small.ar.txt"

    # output_json_file
    output_json_file: str = "../../data/processed/data.json"

    # preprocessor
    preprocessor: Preprocessor = Preprocessor(source_lang_data, target_lang_data, output_json_file)

    # preprocessing
    preprocessor.fire()
