from langdetect import detect
from tinydb import TinyDB, Query
from rapidfuzz import fuzz
from bert_score import score
import requests

# Load TinyDB
db = TinyDB(REMOVED_SECRETdata/products.jsonREMOVED_SECRET)
Product = Query()

# Try MarianMT first
try:
    from transformers import MarianMTModel, MarianTokenizer
    models = {
        REMOVED_SECRETen→esREMOVED_SECRET: REMOVED_SECRETHelsinki-NLP/opus-mt-en-esREMOVED_SECRET,
        REMOVED_SECRETes→enREMOVED_SECRET: REMOVED_SECRETHelsinki-NLP/opus-mt-es-enREMOVED_SECRET
    }
    translation_pipelines = {}
    for direction, model_name in models.items():
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        translation_pipelines[direction] = (tokenizer, model)

    def translate(text, direction):
        tokenizer, model = translation_pipelines[direction]
        inputs = tokenizer(text, return_tensors=REMOVED_SECRETptREMOVED_SECRET, padding=True)
        outputs = model.generate(**inputs)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)

except Exception as e:
    #marianMT and sentencepiece cant be installed in macOS, thus librestanslate api is used instead 
    print(REMOVED_SECRET⚠️ MarianMT not available. Falling back to LibreTranslate API.REMOVED_SECRET)

    def translate(text, direction):
        try:
            source, target = direction.split(REMOVED_SECRET→REMOVED_SECRET)
            response = requests.post(
                REMOVED_SECREThttps://libretranslate.de/translateREMOVED_SECRET,
                headers={REMOVED_SECRETContent-TypeREMOVED_SECRET: REMOVED_SECRETapplication/jsonREMOVED_SECRET},
                json={
                    REMOVED_SECRETqREMOVED_SECRET: text,
                    REMOVED_SECRETsourceREMOVED_SECRET: source,
                    REMOVED_SECRETtargetREMOVED_SECRET: target,
                    REMOVED_SECRETformatREMOVED_SECRET: REMOVED_SECRETtextREMOVED_SECRET
                }
            )
            return response.json().get(REMOVED_SECRETtranslatedTextREMOVED_SECRET, text)
        except:
            return text

def search_spanish(query: str, top_k: int = 5):
    detected_lang = detect(query)

    if detected_lang == REMOVED_SECRETesREMOVED_SECRET:
        query_en = translate(query, REMOVED_SECRETes→enREMOVED_SECRET)
    else:
        query_en = query

    products = db.all()
    matches = []

    for product in products:
        title = product.get(REMOVED_SECRETnameREMOVED_SECRET, {}).get(REMOVED_SECRETenREMOVED_SECRET, REMOVED_SECRETREMOVED_SECRET)
        if not title:
            continue

        token_match = all(token in title.lower() for token in query_en.lower().split())
        fuzzy_score = fuzz.partial_ratio(query_en.lower(), title.lower())

        if token_match or fuzzy_score >= 70:
            matches.append((product, fuzzy_score))

    if not matches:
        return []

    matches.sort(key=lambda x: x[1], reverse=True)
    top_products = [m[0] for m in matches[:top_k]]
    titles = [p[REMOVED_SECRETnameREMOVED_SECRET][REMOVED_SECRETenREMOVED_SECRET] for p in top_products]

    _, _, f1s = score(titles, [query_en] * len(titles), lang=REMOVED_SECRETenREMOVED_SECRET, verbose=False)

    return [
        {
            REMOVED_SECRETproductREMOVED_SECRET: p,
            REMOVED_SECRETbert_score_f1REMOVED_SECRET: round(f1.item(), 4)
        } for p, f1 in zip(top_products, f1s)
    ]