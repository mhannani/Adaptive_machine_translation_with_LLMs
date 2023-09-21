from nltk.tokenize import word_tokenize
from sacremoses import MosesTokenizer, MosesDetokenizer
from transformers import pipeline
import nltk
# Initialize the Moses tokenizer and detokenizer
mt = MosesTokenizer(lang="ar")
md = MosesDetokenizer(lang="ar")

# Sample Arabic sentences
predicted = ["اليوم هو يوم جميل.", "أنا أحب التفاح."]
reference = [["اليوم هو يوم جميل.", "أنا أحب التفاح."]]  # List of reference translations

# Tokenize the predicted sentences using NLTK
predicted_tokenized = [word_tokenize(sent, language='arabic') for sent in predicted]

# Detokenize the tokenized sentences into strings
predicted_detokenized = [md.detokenize(tokens, return_str=True) for tokens in predicted_tokenized]

# Calculate BLEU score using sacremoses
bleu = pipeline(task="translation", model="facebook/wmt19-en-ar")
results = bleu(predicted_detokenized, reference)

print(results)
