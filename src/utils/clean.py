import re


def clean(predicted_sentence: str) -> str:
    """
    Clean given text and keep only non-latin letter

    :param predicted_sentence str
        The predicted sentence in Arabic. Ex: "Arabic: هل تشكل اللغة الالمانية عائق في هذه الحالة"

    :return str
        Cleaned text Ex: "هل تشكل اللغة الالمانية عائق في هذه الحالة"
    """

    # Use a regular expression to match Arabic characters (Unicode range)
    arabic_pattern = re.compile(r'[\u0600-\u06FF\s]+')

    # Find all matches of Arabic text in the predicted sentence
    arabic_matches = arabic_pattern.findall(predicted_sentence)

    # Join the matched Arabic text to form the cleaned text
    cleaned_text = ''.join(arabic_matches)

    return cleaned_text


if __name__ == "__main__":
    cleaned = clean("Arabic: هل تشكل اللغة الالمانية عائق في هذه الحالة")

    print(cleaned)
