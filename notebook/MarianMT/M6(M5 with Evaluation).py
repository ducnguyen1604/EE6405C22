import pandas as pd
from transformers import MarianMTModel, MarianTokenizer
from langdetect import detect
from rapidfuzz import fuzz
from bert_score import score as bert_score
import nltk
from nltk.translate.meteor_score import single_meteor_score


# Auto-install spellchecker if not present
try:
    from spellchecker import SpellChecker
except ModuleNotFoundError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, REMOVED_SECRET-mREMOVED_SECRET, REMOVED_SECRETpipREMOVED_SECRET, REMOVED_SECRETinstallREMOVED_SECRET, REMOVED_SECRETpyspellcheckerREMOVED_SECRET])
    from spellchecker import SpellChecker

spell = SpellChecker()

# Load dataset
amazon_df = pd.read_csv(REMOVED_SECRETC:\\Users\\65988\\Documents\\GitHub\\EE6405C22\\NLP\\dataset\\Amazon_en_to_es.csvREMOVED_SECRET)

# Load MarianMT models
models = {
    REMOVED_SECRETen→esREMOVED_SECRET: REMOVED_SECRETHelsinki-NLP/opus-mt-en-esREMOVED_SECRET,
    REMOVED_SECRETes→enREMOVED_SECRET: REMOVED_SECRETHelsinki-NLP/opus-mt-es-enREMOVED_SECRET
}
translation_pipelines = {}
for direction, model_name in models.items():
    print(fREMOVED_SECRET🔄 Loading model: {direction}REMOVED_SECRET)
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    translation_pipelines[direction] = (tokenizer, model)

# Translation function
def translate(text, direction):
    tokenizer, model = translation_pipelines[direction]
    inputs = tokenizer(text, return_tensors=REMOVED_SECRETptREMOVED_SECRET, padding=True)
    outputs = model.generate(**inputs)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Token + fuzzy match search
def search_dataset(df, column, query, fuzzy_threshold=70):
    query_tokens = query.lower().split()
    token_matches = df[df[column].str.lower().apply(
        lambda text: all(token in text for token in query_tokens)
    )]
    if not token_matches.empty:
        return token_matches

    fuzzy_matches = []
    for _, row in df.iterrows():
        score = fuzz.partial_ratio(query.lower(), str(row[column]).lower())
        if score >= fuzzy_threshold:
            fuzzy_matches.append(row)
    return pd.DataFrame(fuzzy_matches)

# Main search loop
while True:
    user_input = input(REMOVED_SECRET\nEnter your product search query (English/Spanish, or type 'exit' to quit): REMOVED_SECRET)
    if user_input.lower() in [REMOVED_SECRETexitREMOVED_SECRET, REMOVED_SECRETquitREMOVED_SECRET]:
        print(REMOVED_SECRET👋 Exiting search. Goodbye!REMOVED_SECRET)
        break

    corrected_input = REMOVED_SECRET REMOVED_SECRET.join([spell.correction(w) or w for w in user_input.split()])
    if corrected_input.lower() != user_input.lower():
        print(fREMOVED_SECRET📝 Corrected input: {corrected_input}REMOVED_SECRET)
    else:
        corrected_input = user_input

    detected_lang = detect(corrected_input)
    print(fREMOVED_SECRET🔍 Detected language: {detected_lang}REMOVED_SECRET)

    # Non-English/Spanish fallback
    if detected_lang not in [REMOVED_SECRETenREMOVED_SECRET, REMOVED_SECRETesREMOVED_SECRET]:
        if all(c.isascii() and (c.isalpha() or c.isspace()) for c in corrected_input):
            print(fREMOVED_SECRET⚠️ Detected '{detected_lang}', trying both English and Spanish due to input format.REMOVED_SECRET)
            en_results = search_dataset(amazon_df, REMOVED_SECRETtitleREMOVED_SECRET, corrected_input)
            es_to_en_query = translate(corrected_input, REMOVED_SECRETes→enREMOVED_SECRET)
            es_results = search_dataset(amazon_df, REMOVED_SECRETtitleREMOVED_SECRET, es_to_en_query)

            if not en_results.empty:
                print(REMOVED_SECRET✅ Interpreted as English.REMOVED_SECRET)
                search_query_en = corrected_input
                detected_lang = REMOVED_SECRETenREMOVED_SECRET
                results = en_results
            elif not es_results.empty:
                print(REMOVED_SECRET✅ Interpreted as Spanish.REMOVED_SECRET)
                search_query_en = es_to_en_query
                detected_lang = REMOVED_SECRETesREMOVED_SECRET
                results = es_results
            else:
                print(REMOVED_SECRET❌ No matching results found in either English or Spanish.REMOVED_SECRET)
                continue
        else:
            print(REMOVED_SECRET⚠️ Only English or Spanish are supported. Try again.REMOVED_SECRET)
            continue
    else:
        # Translate Spanish to English
        if detected_lang == REMOVED_SECRETesREMOVED_SECRET:
            search_query_en = translate(corrected_input, REMOVED_SECRETes→enREMOVED_SECRET)
        else:
            search_query_en = corrected_input

        results = search_dataset(amazon_df, REMOVED_SECRETtitleREMOVED_SECRET, search_query_en)
        if results.empty:
            print(REMOVED_SECRET❌ No matching results found.REMOVED_SECRET)
            continue

    # Display results
    print(REMOVED_SECRET✅ Search Results:REMOVED_SECRET)
    print(results.head())

    # Prepare for evaluation
    candidate_titles = results[REMOVED_SECRETtitleREMOVED_SECRET].head(5).tolist()
    references = [search_query_en] * len(candidate_titles)

    # Compute BERTScore
    P, R, F1 = bert_score(candidate_titles, references, lang=REMOVED_SECRETenREMOVED_SECRET, verbose=False)

    print(REMOVED_SECRET\n📊 Evaluation: BERTScore + METEORREMOVED_SECRET)
    if detected_lang == REMOVED_SECRETesREMOVED_SECRET:
        translated_titles = [translate(title, REMOVED_SECRETen→esREMOVED_SECRET) for title in candidate_titles]
        for i, (trans_title, p, r, f1) in enumerate(zip(translated_titles, P, R, F1)):
            meteor = single_meteor_score(search_query_en.split(), candidate_titles[i].split())
            print(fREMOVED_SECRET{i+1}. Translated: {trans_title[:60]}...REMOVED_SECRET)
            print(fREMOVED_SECRET   → BERT Precision: {p.item():.4f}REMOVED_SECRET)
            print(fREMOVED_SECRET   → BERT Recall:    {r.item():.4f}REMOVED_SECRET)
            print(fREMOVED_SECRET   → BERT F1 Score:  {f1.item():.4f}REMOVED_SECRET)
            print(fREMOVED_SECRET   → METEOR Score:   {meteor:.4f}REMOVED_SECRET)
    else:
        for i, (title, p, r, f1) in enumerate(zip(candidate_titles, P, R, F1)):
            meteor = single_meteor_score(search_query_en.split(), title.split())
            print(fREMOVED_SECRET{i+1}. Title: {title[:60]}...REMOVED_SECRET)
            print(fREMOVED_SECRET   → BERT Precision: {p.item():.4f}REMOVED_SECRET)
            print(fREMOVED_SECRET   → BERT Recall:    {r.item():.4f}REMOVED_SECRET)
            print(fREMOVED_SECRET   → BERT F1 Score:  {f1.item():.4f}REMOVED_SECRET)
            print(fREMOVED_SECRET   → METEOR Score:   {meteor:.4f}REMOVED_SECRET)
