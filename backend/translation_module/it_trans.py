from mBART.translate import load_model_and_tokenizer, translate_sentence

# Load model/tokenizer once
model_path = "mBART/final"  # Adjust if needed
model, tokenizer = load_model_and_tokenizer(model_path)

def translate_to_italian(query: str) -> str:
    return translate_sentence(model, tokenizer, query, src_lang="en", tgt_lang="it")
