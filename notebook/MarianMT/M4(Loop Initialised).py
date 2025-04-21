import pandas as pd
from transformers import MarianMTModel, MarianTokenizer
from langdetect import detect

# Load datasets
amazon_df = pd.read_csv("C:\\Users\\65988\\Documents\\GitHub\\EE6405C22\\NLP\\dataset\\Amazon_en_to_es.csv")
shopee_df = pd.read_csv("C:\\Users\\65988\\Documents\\GitHub\\EE6405C22\\NLP\\dataset\\Shopee_CN_to_EN.csv")
italian_df = pd.read_csv("C:\\Users\\65988\\Documents\\GitHub\\EE6405C22\\NLP\\dataset\\target_en_to_it.csv")

# Define translation models
models = {
    "en→zh": "Helsinki-NLP/opus-mt-en-zh",
    "zh→en": "Helsinki-NLP/opus-mt-zh-en",
    "en→it": "Helsinki-NLP/opus-mt-en-it",
    "it→en": "Helsinki-NLP/opus-mt-mul-en",
    "en→fr": "Helsinki-NLP/opus-mt-en-fr",
    "es→en": "Helsinki-NLP/opus-mt-es-en",
    "en→es": "Helsinki-NLP/opus-mt-en-es"
}

# Load translation pipelines
translation_pipelines = {}
for key, model_name in models.items():
    print(f"🔄 Loading model: {key}")
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    translation_pipelines[key] = (tokenizer, model)

# Translation function
def translate(text, direction):
    tokenizer, model = translation_pipelines[direction]
    inputs = tokenizer(text, return_tensors="pt", padding=True)
    outputs = model.generate(**inputs)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Search all datasets
def search_dataset(df, column, query):
    return df[df[column].str.contains(query, case=False, na=False)]

# Main search loop
while True:
    user_input = input("\nEnter your product search query (or type 'exit' to quit): ")
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Exiting search. Goodbye!")
        break

    detected_lang = detect(user_input)
    print(f"🔍 Detected language: {detected_lang}")

    supported_langs = ["zh", "it", "es", "fr"]
    if detected_lang not in supported_langs:
        print(f"⚠️ Detected unsupported language '{detected_lang}', defaulting to English.")
        detected_lang = "en"

    if detected_lang == "zh":
        search_query_en = translate(user_input, "zh→en")
    elif detected_lang == "it":
        search_query_en = translate(user_input, "it→en")
    elif detected_lang == "es":
        search_query_en = translate(user_input, "es→en")
    else:
        search_query_en = user_input

    print(f"🔎 Searching for: {search_query_en}")

    results = []
    results.append(search_dataset(amazon_df, "title", search_query_en))
    results.append(search_dataset(shopee_df, "translation_output", search_query_en))
    results.append(search_dataset(italian_df, "title", search_query_en))

    combined = pd.concat(results)
    if combined.empty:
        print("❌ No matching results found.")
        continue

    print("✅ Search Results:")
    print(combined.head())

    if detected_lang != "en":
        def get_display_title(row):
            return row["title"] if "title" in row and pd.notna(row["title"]) else row.get("translation_output", "")

        display_titles = [get_display_title(row) for _, row in combined.head().iterrows()]
        translated_titles = [translate(title, f"en→{detected_lang}") for title in display_titles]

        print("\n🌍 Translated Results:")
        for original, translated in zip(display_titles, translated_titles):
            print(f"- {original} → {translated}")
    else:
        print("\n🌍 All results already in English.")
