from mBART.translate import load_model_and_tokenizer, translate_sentence

model_path = REMOVED_SECRETmBART/finalREMOVED_SECRET
model, tokenizer = load_model_and_tokenizer(model_path)

def translate_to_spanish(query: str) -> str:
    return translate_sentence(model, tokenizer, query, src_lang=REMOVED_SECRETenREMOVED_SECRET, tgt_lang=REMOVED_SECRETesREMOVED_SECRET)
