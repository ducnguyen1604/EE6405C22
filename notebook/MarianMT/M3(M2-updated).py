import pandas as pd
from transformers import MarianMTModel, MarianTokenizer
from langdetect import detect

# Load datasets
amazon_df = pd.read_csv("C:\\Users\\65988\\Documents\\GitHub\\EE6405C22\\NLP\\dataset\\Amazon_en_to_es.csv")
shopee_df = pd.read_csv("C:\\Users\\65988\\Documents\\GitHub\\EE6405C22\\NLP\\dataset\\Shopee_CN_to_EN.csv")
italian_df = pd.read_csv("C:\\Users\\65988\\Documents\\GitHub\\EE6405C22\\NLP\\dataset\\target_en_to_it.csv")


# Define translation models
#You specify 7 translation directions using Helsinki-NLP MarianMT models from HuggingFace.
#These are transformer-based models for multilingual translation.

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

# User input
user_input = input("Enter your product search query: ")
detected_lang = detect(user_input)
print(f"🔍 Detected language: {detected_lang}")

# Only support languages you've loaded models for
supported_langs = ["zh", "it", "es", "fr"]
if detected_lang not in supported_langs:
    print(f"⚠️ Detected unsupported language '{detected_lang}', defaulting to English.")
    detected_lang = "en"

# Translate to English if needed
if detected_lang == "zh":
    search_query_en = translate(user_input, "zh→en")
elif detected_lang == "it":
    search_query_en = translate(user_input, "it→en")
elif detected_lang == "es":
    search_query_en = translate(user_input, "es→en")
else:
    search_query_en = user_input

print(f"🔎 Searching for: {search_query_en}")

# Search all datasets
def search_dataset(df, column):
    return df[df[column].str.contains(search_query_en, case=False, na=False)]

results = []
results.append(search_dataset(amazon_df, "title"))
results.append(search_dataset(shopee_df, "translation_output"))
results.append(search_dataset(italian_df, "title"))

# Combine
combined = pd.concat(results)
print("✅ Search Results:")
print(combined.head())

# Translate back only if language was not English
if detected_lang != "en":
    # Handle missing 'title' in Shopee by falling back to 'translation_output'
    def get_display_title(row):
        return row["title"] if "title" in row and pd.notna(row["title"]) else row.get("translation_output", "")

    display_titles = [get_display_title(row) for _, row in combined.head().iterrows()]
    translated_titles = [translate(title, f"en→{detected_lang}") for title in display_titles]

    print("\n🌍 Translated Results:")
    for original, translated in zip(display_titles, translated_titles):
        print(f"- {original} → {translated}")
else:
    print("\n🌍 All results already in English.")
