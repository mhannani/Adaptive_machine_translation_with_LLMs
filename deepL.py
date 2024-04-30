# https://www.deepl.com/en/docs-api
# pip install --upgrade deepl
import deepl


if __name__ == "__main__":
    auth_key = "75b4d5bf-87b0-ba6a-2653-c7f265240d10"  # Replace with your key
    translator = deepl.Translator(auth_key)

    result = translator.translate_text("Hello, world!", target_lang="FR")
    print(result.text)  # "Bonjour, le monde !"



    # https://www.kaggle.com/datasets/samirmoustafa/arabic-to-english-translation-sentences