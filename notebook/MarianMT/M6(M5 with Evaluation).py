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
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyspellchecker"])
    from spellchecker import SpellChecker

spell = SpellChecker()

# Load dataset
amazon_df = pd.read_csv("C:\\Users\\65988\\Documents\\GitHub\\EE6405C22\\NLP\\dataset\\Amazon_en_to_es.csv")

# Load MarianMT models
models = {
    "en→es": "Helsinki-NLP/opus-mt-en-es",
    "es→en": "Helsinki-NLP/opus-mt-es-en"
}
translation_pipelines = {}
for direction, model_name in models.items():
    print(f"🔄 Loading model: {direction}")
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    translation_pipelines[direction] = (tokenizer, model)

# Translation function
def translate(text, direction):
    tokenizer, model = translation_pipelines[direction]
    inputs = tokenizer(text, return_tensors="pt", padding=True)
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
    user_input = input("\nEnter your product search query (English/Spanish, or type 'exit' to quit): ")
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Exiting search. Goodbye!")
        break

    corrected_input = " ".join([spell.correction(w) or w for w in user_input.split()])
    if corrected_input.lower() != user_input.lower():
        print(f"📝 Corrected input: {corrected_input}")
    else:
        corrected_input = user_input

    detected_lang = detect(corrected_input)
    print(f"🔍 Detected language: {detected_lang}")

    # Non-English/Spanish fallback
    if detected_lang not in ["en", "es"]:
        if all(c.isascii() and (c.isalpha() or c.isspace()) for c in corrected_input):
            print(f"⚠️ Detected '{detected_lang}', trying both English and Spanish due to input format.")
            en_results = search_dataset(amazon_df, "title", corrected_input)
            es_to_en_query = translate(corrected_input, "es→en")
            es_results = search_dataset(amazon_df, "title", es_to_en_query)

            if not en_results.empty:
                print("✅ Interpreted as English.")
                search_query_en = corrected_input
                detected_lang = "en"
                results = en_results
            elif not es_results.empty:
                print("✅ Interpreted as Spanish.")
                search_query_en = es_to_en_query
                detected_lang = "es"
                results = es_results
            else:
                print("❌ No matching results found in either English or Spanish.")
                continue
        else:
            print("⚠️ Only English or Spanish are supported. Try again.")
            continue
    else:
        # Translate Spanish to English
        if detected_lang == "es":
            search_query_en = translate(corrected_input, "es→en")
        else:
            search_query_en = corrected_input

        results = search_dataset(amazon_df, "title", search_query_en)
        if results.empty:
            print("❌ No matching results found.")
            continue

    # Display results
    print("✅ Search Results:")
    print(results.head())

    # Prepare for evaluation
    candidate_titles = results["title"].head(5).tolist()
    references = [search_query_en] * len(candidate_titles)

    # Compute BERTScore
    P, R, F1 = bert_score(candidate_titles, references, lang="en", verbose=False)

    print("\n📊 Evaluation: BERTScore + METEOR")
    if detected_lang == "es":
        translated_titles = [translate(title, "en→es") for title in candidate_titles]
        for i, (trans_title, p, r, f1) in enumerate(zip(translated_titles, P, R, F1)):
            meteor = single_meteor_score(search_query_en.split(), candidate_titles[i].split())
            print(f"{i+1}. Translated: {trans_title[:60]}...")
            print(f"   → BERT Precision: {p.item():.4f}")
            print(f"   → BERT Recall:    {r.item():.4f}")
            print(f"   → BERT F1 Score:  {f1.item():.4f}")
            print(f"   → METEOR Score:   {meteor:.4f}")
    else:
        for i, (title, p, r, f1) in enumerate(zip(candidate_titles, P, R, F1)):
            meteor = single_meteor_score(search_query_en.split(), title.split())
            print(f"{i+1}. Title: {title[:60]}...")
            print(f"   → BERT Precision: {p.item():.4f}")
            print(f"   → BERT Recall:    {r.item():.4f}")
            print(f"   → BERT F1 Score:  {f1.item():.4f}")
            print(f"   → METEOR Score:   {meteor:.4f}")
