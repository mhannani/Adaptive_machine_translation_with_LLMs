# https://www.deepl.com/en/docs-api
# pip install --upgrade deepl
import deepl


if __name__ == "__main__":
    auth_key = "f63c02c5-f056-..."  # Replace with your key
    translator = deepl.Translator(auth_key)

    result = translator.translate_text("Hello, world!", target_lang="FR")
    print(result.text)  # "Bonjour, le monde !"



    # https://www.kaggle.com/datasets/samirmoustafa/arabic-to-english-translation-sentences