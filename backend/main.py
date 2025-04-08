from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from db.tinydb_conn import db
from models.product import Product
from fuzzywuzzy import fuzz
from tinydb import Query as TinyQuery

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[REMOVED_SECRET*REMOVED_SECRET],
    allow_methods=[REMOVED_SECRET*REMOVED_SECRET],
    allow_headers=[REMOVED_SECRET*REMOVED_SECRET],
)

# Dummy translator
def dummy_translate(query: str, lang: str) -> str:
    translations = {
        (REMOVED_SECRETmouth sprayREMOVED_SECRET, REMOVED_SECRETChineseREMOVED_SECRET): REMOVED_SECRET口腔喷雾REMOVED_SECRET,
        (REMOVED_SECRETmouth sprayREMOVED_SECRET, REMOVED_SECRETSpanishREMOVED_SECRET): REMOVED_SECRETspray oralREMOVED_SECRET,
        (REMOVED_SECRETmouth sprayREMOVED_SECRET, REMOVED_SECRETItalianREMOVED_SECRET): REMOVED_SECRETspray oraleREMOVED_SECRET,

        (REMOVED_SECRETbreadREMOVED_SECRET, REMOVED_SECRETChineseREMOVED_SECRET): REMOVED_SECRET面包REMOVED_SECRET,
        (REMOVED_SECRETbreadREMOVED_SECRET, REMOVED_SECRETSpanishREMOVED_SECRET): REMOVED_SECRETpanREMOVED_SECRET,
        (REMOVED_SECRETbreadREMOVED_SECRET, REMOVED_SECRETItalianREMOVED_SECRET): REMOVED_SECRETpaneREMOVED_SECRET,

        (REMOVED_SECRETshirtREMOVED_SECRET, REMOVED_SECRETChineseREMOVED_SECRET): REMOVED_SECRET衬衫REMOVED_SECRET,
        (REMOVED_SECRETshirtREMOVED_SECRET, REMOVED_SECRETSpanishREMOVED_SECRET): REMOVED_SECRETcamisaREMOVED_SECRET,
        (REMOVED_SECRETshirtREMOVED_SECRET, REMOVED_SECRETItalianREMOVED_SECRET): REMOVED_SECRETcamiciaREMOVED_SECRET,
    }
    return translations.get((query.lower(), lang), query)

# --- /search endpoint ---
@app.get(REMOVED_SECRET/searchREMOVED_SECRET)
def search_products(q: str = Query(...), langs: str = Query(REMOVED_SECRETREMOVED_SECRET)):
    ProductQuery = TinyQuery()
    languages = [lang.strip() for lang in langs.split(REMOVED_SECRET,REMOVED_SECRET) if lang.strip()]
    translations = {}

    translated_queries = []
    for lang in languages:
        translated = dummy_translate(q, lang)
        translations[lang] = translated
        translated_queries.append(translated.lower().strip())

    translated_queries.append(q.lower().strip())

    (REMOVED_SECRETTranslated Queries:REMOVED_SECRET, translated_queries)

    matched = []
    all_products = db.all()
    print(fREMOVED_SECRETLoaded {len(all_products)} productsREMOVED_SECRET)

    for product in all_products:
        print(REMOVED_SECRETChecking product:REMOVED_SECRET, product[REMOVED_SECRETidREMOVED_SECRET])
        for lang in [REMOVED_SECRETenREMOVED_SECRET, REMOVED_SECRETesREMOVED_SECRET, REMOVED_SECRETitREMOVED_SECRET, REMOVED_SECRETzhREMOVED_SECRET]:
            name = product[REMOVED_SECRETnameREMOVED_SECRET].get(lang, REMOVED_SECRETREMOVED_SECRET).lower().strip()
            desc = product[REMOVED_SECRETdescriptionREMOVED_SECRET].get(lang, REMOVED_SECRETREMOVED_SECRET).lower().strip()

            for query in translated_queries:
                if query in name or query in desc:
                    print(fREMOVED_SECRETMatched on {lang} for query '{query}' → {name}REMOVED_SECRET)
                    matched.append(product)
                    break
            else:
                continue
            break

    return {
        REMOVED_SECRETtranslationsREMOVED_SECRET: translations,
        REMOVED_SECRETproductsREMOVED_SECRET: matched
    }



# --- /product/{id} endpoint ---
@app.get(REMOVED_SECRET/product/{id}REMOVED_SECRET, response_model=Product)
def get_product(id: int):
    ProductQuery = TinyQuery()
    result = db.get(ProductQuery.id == id)
    if not result:
        raise HTTPException(status_code=404, detail=REMOVED_SECRETProduct not foundREMOVED_SECRET)
    return result
