import pandas as pd
from transformers import MarianMTModel, MarianTokenizer
from langdetect import detect

# Load datasets
amazon_df = pd.read_csv(REMOVED_SECRETC:\\Users\\65988\\Documents\\GitHub\\EE6405C22\\NLP\\dataset\\Amazon_en_to_es.csvREMOVED_SECRET)
shopee_df = pd.read_csv(REMOVED_SECRETC:\\Users\\65988\\Documents\\GitHub\\EE6405C22\\NLP\\dataset\\Shopee_CN_to_EN.csvREMOVED_SECRET)
italian_df = pd.read_csv(REMOVED_SECRETC:\\Users\\65988\\Documents\\GitHub\\EE6405C22\\NLP\\dataset\\target_en_to_it.csvREMOVED_SECRET)

# Define translation models
models = {
    REMOVED_SECRETen→zhREMOVED_SECRET: REMOVED_SECRETHelsinki-NLP/opus-mt-en-zhREMOVED_SECRET,
    REMOVED_SECRETzh→enREMOVED_SECRET: REMOVED_SECRETHelsinki-NLP/opus-mt-zh-enREMOVED_SECRET,
    REMOVED_SECRETen→itREMOVED_SECRET: REMOVED_SECRETHelsinki-NLP/opus-mt-en-itREMOVED_SECRET,
    REMOVED_SECRETit→enREMOVED_SECRET: REMOVED_SECRETHelsinki-NLP/opus-mt-mul-enREMOVED_SECRET,
    REMOVED_SECRETen→frREMOVED_SECRET: REMOVED_SECRETHelsinki-NLP/opus-mt-en-frREMOVED_SECRET,
    REMOVED_SECRETes→enREMOVED_SECRET: REMOVED_SECRETHelsinki-NLP/opus-mt-es-enREMOVED_SECRET,
    REMOVED_SECRETen→esREMOVED_SECRET: REMOVED_SECRETHelsinki-NLP/opus-mt-en-esREMOVED_SECRET
}

# Load translation pipelines
translation_pipelines = {}
for key, model_name in models.items():
    print(fREMOVED_SECRET🔄 Loading model: {key}REMOVED_SECRET)
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    translation_pipelines[key] = (tokenizer, model)

# Translation function
def translate(text, direction):
    tokenizer, model = translation_pipelines[direction]
    inputs = tokenizer(text, return_tensors=REMOVED_SECRETptREMOVED_SECRET, padding=True)
    outputs = model.generate(**inputs)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Search all datasets
def search_dataset(df, column, query):
    return df[df[column].str.contains(query, case=False, na=False)]

# Main search loop
while True:
    user_input = input(REMOVED_SECRET\nEnter your product search query (or type 'exit' to quit): REMOVED_SECRET)
    if user_input.lower() in [REMOVED_SECRETexitREMOVED_SECRET, REMOVED_SECRETquitREMOVED_SECRET]:
        print(REMOVED_SECRET👋 Exiting search. Goodbye!REMOVED_SECRET)
        break

    detected_lang = detect(user_input)
    print(fREMOVED_SECRET🔍 Detected language: {detected_lang}REMOVED_SECRET)

    supported_langs = [REMOVED_SECRETzhREMOVED_SECRET, REMOVED_SECRETitREMOVED_SECRET, REMOVED_SECRETesREMOVED_SECRET, REMOVED_SECRETfrREMOVED_SECRET]
    if detected_lang not in supported_langs:
        print(fREMOVED_SECRET⚠️ Detected unsupported language '{detected_lang}', defaulting to English.REMOVED_SECRET)
        detected_lang = REMOVED_SECRETenREMOVED_SECRET

    if detected_lang == REMOVED_SECRETzhREMOVED_SECRET:
        search_query_en = translate(user_input, REMOVED_SECRETzh→enREMOVED_SECRET)
    elif detected_lang == REMOVED_SECRETitREMOVED_SECRET:
        search_query_en = translate(user_input, REMOVED_SECRETit→enREMOVED_SECRET)
    elif detected_lang == REMOVED_SECRETesREMOVED_SECRET:
        search_query_en = translate(user_input, REMOVED_SECRETes→enREMOVED_SECRET)
    else:
        search_query_en = user_input

    print(fREMOVED_SECRET🔎 Searching for: {search_query_en}REMOVED_SECRET)

    results = []
    results.append(search_dataset(amazon_df, REMOVED_SECRETtitleREMOVED_SECRET, search_query_en))
    results.append(search_dataset(shopee_df, REMOVED_SECRETtranslation_outputREMOVED_SECRET, search_query_en))
    results.append(search_dataset(italian_df, REMOVED_SECRETtitleREMOVED_SECRET, search_query_en))

    combined = pd.concat(results)
    if combined.empty:
        print(REMOVED_SECRET❌ No matching results found.REMOVED_SECRET)
        continue

    print(REMOVED_SECRET✅ Search Results:REMOVED_SECRET)
    print(combined.head())

    if detected_lang != REMOVED_SECRETenREMOVED_SECRET:
        def get_display_title(row):
            return row[REMOVED_SECRETtitleREMOVED_SECRET] if REMOVED_SECRETtitleREMOVED_SECRET in row and pd.notna(row[REMOVED_SECRETtitleREMOVED_SECRET]) else row.get(REMOVED_SECRETtranslation_outputREMOVED_SECRET, REMOVED_SECRETREMOVED_SECRET)

        display_titles = [get_display_title(row) for _, row in combined.head().iterrows()]
        translated_titles = [translate(title, fREMOVED_SECRETen→{detected_lang}REMOVED_SECRET) for title in display_titles]

        print(REMOVED_SECRET\n🌍 Translated Results:REMOVED_SECRET)
        for original, translated in zip(display_titles, translated_titles):
            print(fREMOVED_SECRET- {original} → {translated}REMOVED_SECRET)
    else:
        print(REMOVED_SECRET\n🌍 All results already in English.REMOVED_SECRET)
