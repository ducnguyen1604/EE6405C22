from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from tinydb import Query as TinyQuery
from models.product import Product
from db.tinydb_conn import db

from search_modules.chinese import search_chinese
from search_modules.italian import search_italian
from search_modules.spanish import search_spanish

# Optional: fallback translation API
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[REMOVED_SECRET*REMOVED_SECRET],
    allow_methods=[REMOVED_SECRET*REMOVED_SECRET],
    allow_headers=[REMOVED_SECRET*REMOVED_SECRET],
)

# Unified translate function using LibreTranslate
def translate(query: str, target_lang: str) -> str:
    lang_map = {
        REMOVED_SECRETchineseREMOVED_SECRET: REMOVED_SECRETzhREMOVED_SECRET,
        REMOVED_SECRETitalianREMOVED_SECRET: REMOVED_SECRETitREMOVED_SECRET,
        REMOVED_SECRETspanishREMOVED_SECRET: REMOVED_SECRETesREMOVED_SECRET
    }
    if target_lang.lower() not in lang_map:
        return query

    '''
    target_code = lang_map[target_lang.lower()]
    response = requests.post(
        REMOVED_SECREThttps://libretranslate.de/translateREMOVED_SECRET,
        headers={REMOVED_SECRETContent-TypeREMOVED_SECRET: REMOVED_SECRETapplication/jsonREMOVED_SECRET},
        json={
            REMOVED_SECRETqREMOVED_SECRET: query,
            REMOVED_SECRETsourceREMOVED_SECRET: REMOVED_SECRETenREMOVED_SECRET,  # assuming user inputs in English
            REMOVED_SECRETtargetREMOVED_SECRET: target_code,
            REMOVED_SECRETformatREMOVED_SECRET: REMOVED_SECRETtextREMOVED_SECRET
        }
    )
    return response.json().get(REMOVED_SECRETtranslatedTextREMOVED_SECRET, query)
    '''

@app.get(REMOVED_SECRET/searchREMOVED_SECRET)
def search_products(q: str = Query(...), langs: str = Query(REMOVED_SECRETREMOVED_SECRET)):
    language_list = [lang.strip().lower() for lang in langs.split(REMOVED_SECRET,REMOVED_SECRET) if lang.strip()]
    translations = {}
    matched = []

    if not language_list:
        # Simple English keyword search if no language specified
        all_products = db.all()
        for product in all_products:
            title_en = product.get(REMOVED_SECRETnameREMOVED_SECRET, {}).get(REMOVED_SECRETenREMOVED_SECRET, REMOVED_SECRETREMOVED_SECRET).lower()
            desc_en = product.get(REMOVED_SECRETdescriptionREMOVED_SECRET, {}).get(REMOVED_SECRETenREMOVED_SECRET, REMOVED_SECRETREMOVED_SECRET).lower()
            if q.lower() in title_en or q.lower() in desc_en:
                matched.append(product)

        translations[REMOVED_SECRETenglishREMOVED_SECRET] = q  # just echo the query
        return {
            REMOVED_SECRETtranslationsREMOVED_SECRET: translations,
            REMOVED_SECRETproductsREMOVED_SECRET: matched
        }

    # Multilingual search (when language is specified)
    for lang in language_list:
        translated = translate(q, lang)
        translations[lang] = translated

        if lang == REMOVED_SECRETchineseREMOVED_SECRET:
            results = search_chinese(q)
        elif lang == REMOVED_SECRETspanishREMOVED_SECRET:
            results = search_spanish(q)
        elif lang == REMOVED_SECRETitalianREMOVED_SECRET:
            results = search_italian(q)
        elif lang == REMOVED_SECRETenglishREMOVED_SECRET:
            # optionally reuse basic search logic
            all_products = db.all()
            for product in all_products:
                title_en = product.get(REMOVED_SECRETnameREMOVED_SECRET, {}).get(REMOVED_SECRETenREMOVED_SECRET, REMOVED_SECRETREMOVED_SECRET).lower()
                desc_en = product.get(REMOVED_SECRETdescriptionREMOVED_SECRET, {}).get(REMOVED_SECRETenREMOVED_SECRET, REMOVED_SECRETREMOVED_SECRET).lower()
                if q.lower() in title_en or q.lower() in desc_en:
                    matched.append(product)
            continue
        else:
            continue

        for r in results:
            matched.append(r)

    return {
        REMOVED_SECRETtranslationsREMOVED_SECRET: translations,
        REMOVED_SECRETproductsREMOVED_SECRET: matched
    }


@app.get(REMOVED_SECRET/product/{id}REMOVED_SECRET, response_model=Product)
def get_product(id: int):
    ProductQuery = TinyQuery()
    result = db.get(ProductQuery.id == id)
    if not result:
        raise HTTPException(status_code=404, detail=REMOVED_SECRETProduct not foundREMOVED_SECRET)
    return result
