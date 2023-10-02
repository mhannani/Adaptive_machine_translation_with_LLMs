from transformers import pipeline
# https://huggingface.co/Helsinki-NLP/opus-mt-tc-big-en-ar

if __name__ == "__main__":
    pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-tc-big-en-ar")
    print(pipe(">>ara<< I can't help you because I'm busy."))

    # expected output: لا أستطيع مساعدتك لأنني مشغول.