import torch
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
import argparse

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

def main():
    parser = argparse.ArgumentParser(description='Translate text using trained mBART model')
    parser.add_argument('--model_path', type=str, default=REMOVED_SECRET./mbart50-ecommerce/finalREMOVED_SECRET,
                        help='Path to the trained model directory (default: ./mbart50-ecommerce/final)')
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
    print(fREMOVED_SECRETLoading model from {args.model_path}...REMOVED_SECRET)
    model, tokenizer = load_model_and_tokenizer(args.model_path)
    
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