import torch
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
import argparse
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='..../.env')
model_path = os.getenv('mBART_path')

# Language code mapping
lang_code_map = {
    REMOVED_SECRETenREMOVED_SECRET: REMOVED_SECRETen_XXREMOVED_SECRET,
    REMOVED_SECRETesREMOVED_SECRET: REMOVED_SECRETes_XXREMOVED_SECRET,
    REMOVED_SECRETitREMOVED_SECRET: REMOVED_SECRETit_ITREMOVED_SECRET, 
    REMOVED_SECRETcnREMOVED_SECRET: REMOVED_SECRETzh_CNREMOVED_SECRET
}

def load_model_and_tokenizer(model_path):
    REMOVED_SECRETREMOVED_SECRETREMOVED_SECRETLoad the model and tokenizer from the saved checkpointREMOVED_SECRETREMOVED_SECRETREMOVED_SECRET
    model = MBartForConditionalGeneration.from_pretrained(model_path)
    tokenizer = MBart50TokenizerFast.from_pretrained(model_path)
    return model, tokenizer

def translate_sentence(model, tokenizer, text, src_lang, tgt_lang):
    REMOVED_SECRETREMOVED_SECRETREMOVED_SECRETTranslate a single sentenceREMOVED_SECRETREMOVED_SECRETREMOVED_SECRET
    # Set source and target languages
    tokenizer.src_lang = lang_code_map[src_lang]
    
    # Tokenize input
    inputs = tokenizer(text, return_tensors=REMOVED_SECRETptREMOVED_SECRET, padding=True, truncation=True, max_length=64)
    
    # Generate translation
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            forced_bos_token_id=tokenizer.lang_code_to_id[lang_code_map[tgt_lang]],
            max_length=64,
            num_beams=4,
            early_stopping=True,
            no_repeat_ngram_size=3,  # Prevent repeating n-grams
            repetition_penalty=2.0,   # Penalize repetition
            length_penalty=1.0,       # Balance between length and score
            temperature=0.7,          # Control randomness
            do_sample=True           # Enable sampling
        )
    
    # Decode the output
    translation = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    return translation

def translate_file(model, tokenizer, input_file, output_file, src_lang, tgt_lang):
    REMOVED_SECRETREMOVED_SECRETREMOVED_SECRETTranslate sentences from a fileREMOVED_SECRETREMOVED_SECRETREMOVED_SECRET
    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', encoding='utf-8') as f_out:
        for line in f_in:
            text = line.strip()
            if text:  # Skip empty lines
                translation = translate_sentence(model, tokenizer, text, src_lang, tgt_lang)
                f_out.write(fREMOVED_SECRET{translation}\nREMOVED_SECRET)

