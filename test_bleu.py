import sacrebleu
from nltk import sent_tokenize, word_tokenize

predicted_sentences = ['الطقس هو آخر شيء بريء حقا على وجه الأرض.', 'لا يمكننا التنبؤ بها ولا يمكننا التحكم فيها.', 'أنا دونال ماكلنتاير، وسأقوم بالسفر حول العالم للبحث عن أقسى أنواع الطقس الموجودة.', 'في هذه السلسلة، سأعيش تجربة أسرع الرياح على وجه الأرض.']

target_sentences = ['الطقس آخر شيء برّي حقاً على الأرضِ.', 'نحن لا نَستطيعُ تَوَقُّعه ونحن لا نَستطيعُ السَيْطَرَة عليه.', 'أَنا دونال ماكلنتاير , وسَأُسافرُ حول العالمِ للبَحْث عن الطقسِ الأكثر وحشيةً هناك.', 'في هذه السلسلةِ، سَأُواجهُ الرياح الأسرع على الأرضِ.']

corrected_predicted_sentences = []

for predicted_sentence, target_sentence in zip(predicted_sentences, target_sentences):
    if len(sent_tokenize(predicted_sentence)) > len(sent_tokenize(target_sentence)) and len(word_tokenize(predicted_sentence)) > len(word_tokenize(target_sentence)):
        corrected_predicted_sentences.append(sent_tokenize(predicted_sentence))
    else:
        corrected_predicted_sentences.append(predicted_sentence)

score = sacrebleu.corpus_bleu(corrected_predicted_sentences, [target_sentences])

print(score.score)
