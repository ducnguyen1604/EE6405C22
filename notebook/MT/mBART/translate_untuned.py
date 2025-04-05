import torch
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
import argparse

# Language code mapping for mBART-cc25
lang_code_map = {
    "en": "en_XX",
    "es": "es_XX",
    "it": "it_IT", 
    "cn": "zh_CN"
}

def load_model_and_tokenizer():
    """Load the base mBART-cc25 model and tokenizer"""
    model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-cc25")
    tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-cc25")
    return model, tokenizer

def translate_sentence(model, tokenizer, text, src_lang, tgt_lang):
    """Translate a single sentence"""
    # Set source and target languages
    src_lang_code = lang_code_map[src_lang]
    tgt_lang_code = lang_code_map[tgt_lang]
    
    print(f"DEBUG: Translating from {src_lang_code} to {tgt_lang_code}")
    # Set the source language for the tokenizer
    tokenizer.src_lang = src_lang_code
    
    # Tokenize input
    inputs = tokenizer(
        text, 
        return_tensors="pt", 
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
    """Translate sentences from a file"""
    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', encoding='utf-8') as f_out:
        for line in f_in:
            text = line.strip()
            if text:  # Skip empty lines
                translation = translate_sentence(model, tokenizer, text, src_lang, tgt_lang)
                f_out.write(f"{translation}\n")

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
    print("Loading mBART-cc25 model...")
    model, tokenizer = load_model_and_tokenizer()
    
    if args.text:
        # Translate single sentence
        translation = translate_sentence(model, tokenizer, args.text, args.src_lang, args.tgt_lang)
        print(f"Input: {args.text}")
        print(f"Translation: {translation}")
    elif args.input_file and args.output_file:
        # Translate file
        translate_file(model, tokenizer, args.input_file, args.output_file, args.src_lang, args.tgt_lang)
        print(f"Translation complete. Results saved to {args.output_file}")
    else:
        print("Please provide either --text for single sentence translation or --input_file and --output_file for file translation")

if __name__ == "__main__":
    main() 