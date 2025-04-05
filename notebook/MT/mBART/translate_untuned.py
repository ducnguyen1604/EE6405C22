import torch
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
import argparse

# Language code mapping for mBART-cc25
lang_code_map = {
    REMOVED_SECRETenREMOVED_SECRET: REMOVED_SECRETen_XXREMOVED_SECRET,
    REMOVED_SECRETesREMOVED_SECRET: REMOVED_SECRETes_XXREMOVED_SECRET,
    REMOVED_SECRETitREMOVED_SECRET: REMOVED_SECRETit_ITREMOVED_SECRET, 
    REMOVED_SECRETcnREMOVED_SECRET: REMOVED_SECRETzh_CNREMOVED_SECRET
}

def load_model_and_tokenizer():
    REMOVED_SECRETREMOVED_SECRETREMOVED_SECRETLoad the base mBART-cc25 model and tokenizerREMOVED_SECRETREMOVED_SECRETREMOVED_SECRET
    model = MBartForConditionalGeneration.from_pretrained(REMOVED_SECRETfacebook/mbart-large-cc25REMOVED_SECRET)
    tokenizer = MBart50TokenizerFast.from_pretrained(REMOVED_SECRETfacebook/mbart-large-cc25REMOVED_SECRET)
    return model, tokenizer

def translate_sentence(model, tokenizer, text, src_lang, tgt_lang):
    REMOVED_SECRETREMOVED_SECRETREMOVED_SECRETTranslate a single sentenceREMOVED_SECRETREMOVED_SECRETREMOVED_SECRET
    # Set source and target languages
    src_lang_code = lang_code_map[src_lang]
    tgt_lang_code = lang_code_map[tgt_lang]
    
    print(fREMOVED_SECRETDEBUG: Translating from {src_lang_code} to {tgt_lang_code}REMOVED_SECRET)
    # Set the source language for the tokenizer
    tokenizer.src_lang = src_lang_code
    
    # Tokenize input
    inputs = tokenizer(
        text, 
        return_tensors=REMOVED_SECRETptREMOVED_SECRET, 
        padding=True, 
        truncation=True, 
        max_length=64
    )
    
    # Generate translation
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            forced_bos_token_id=tokenizer.lang_code_to_id[tgt_lang_code],
            max_length=64,
            num_beams=4,
            early_stopping=True,
            no_repeat_ngram_size=2,
            repetition_penalty=1.5,
            length_penalty=1.0,
            temperature=0.7,
            do_sample=False,
            decoder_start_token_id=tokenizer.lang_code_to_id[tgt_lang_code]
        )
    
    # Set target language for decoding
    tokenizer.tgt_lang = tgt_lang_code
    
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

def main():
    parser = argparse.ArgumentParser(description='Translate text using base mBART-cc25 model')
    parser.add_argument('--src_lang', type=str, required=True, 
                        help='Source language code (en, es, it, cn)')
    parser.add_argument('--tgt_lang', type=str, required=True, 
                        help='Target language code (en, es, it, cn)')
    parser.add_argument('--input_file', type=str, 
                        help='Path to input file with sentences to translate')
    parser.add_argument('--output_file', type=str, 
                        help='Path to output file for translations')
    parser.add_argument('--text', type=str, 
                        help='Single sentence to translate')
    
    args = parser.parse_args()
    
    # Load model and tokenizer
    print(REMOVED_SECRETLoading mBART-cc25 model...REMOVED_SECRET)
    model, tokenizer = load_model_and_tokenizer()
    
    if args.text:
        # Translate single sentence
        translation = translate_sentence(model, tokenizer, args.text, args.src_lang, args.tgt_lang)
        print(fREMOVED_SECRETInput: {args.text}REMOVED_SECRET)
        print(fREMOVED_SECRETTranslation: {translation}REMOVED_SECRET)
    elif args.input_file and args.output_file:
        # Translate file
        translate_file(model, tokenizer, args.input_file, args.output_file, args.src_lang, args.tgt_lang)
        print(fREMOVED_SECRETTranslation complete. Results saved to {args.output_file}REMOVED_SECRET)
    else:
        print(REMOVED_SECRETPlease provide either --text for single sentence translation or --input_file and --output_file for file translationREMOVED_SECRET)

if __name__ == REMOVED_SECRET__main__REMOVED_SECRET:
    main() 