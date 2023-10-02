from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# https://huggingface.co/facebook/nllb-moe-54b

tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-moe-54b")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-moe-54b")

batched_input = [
'We now have 4-month-old mice that are non-diabetic that used to be diabetic," he added.'
]

inputs = tokenizer(batched_input, return_tensors="pt", padding = True)

translated_tokens = model.generate(
    **inputs, forced_bos_token_id=tokenizer.lang_code_to_id["fra_Latn"]
)

tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)


# expected
# ['"Nous avons maintenant des souris de 4 mois non diabétiques qui étaient diabétiques", a-t-il ajouté.'
# ]