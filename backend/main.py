from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from tinydb import Query as TinyQuery
from models.product import Product
from db.tinydb_conn import db

from search_modules.chinese import search_chinese
from search_modules.italian import search_italian
from search_modules.spanish import search_spanish

from translation_module.cn_trans import translate_to_chinese
from translation_module.es_trans import translate_to_spanish
from translation_module.it_trans import translate_to_italian

# Optional: fallback translation API
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

#translation part
def translate(query: str, target_langs_str: str) -> Dict[str, str]:
    lang_map = {
        "chinese": translate_to_chinese,
        "italian": translate_to_italian,
        "spanish": translate_to_spanish,
        "english": lambda x: x
    }

    target_langs = [lang.strip().lower() for lang in target_langs_str.split(",") if lang.strip()]
    translations = {}

    for lang in target_langs:
        if lang in lang_map:
            translations[lang] = lang_map[lang](query)

    return translations




@app.get("/search")
def search_products(q: str = Query(...), langs: str = Query("")):
    language_list = [lang.strip().lower() for lang in langs.split(",") if lang.strip()]
    translations = translate(q, langs)
    matched = []

    if not language_list:
        # Simple English keyword search
        all_products = db.all()
        for product in all_products:
            title_en = product.get("name", {}).get("en", "").lower()
            desc_en = product.get("description", {}).get("en", "").lower()
            if q.lower() in title_en or q.lower() in desc_en:
                matched.append(product)

        translations["english"] = q
        return {
            "translations": translations,
            "products": matched
        }

    for lang in language_list:
        translated = translate(q, lang)
        translations[lang] = translated

        if lang == "chinese":
            results = search_chinese(q)
        elif lang == "spanish":
            results = search_spanish(q)
        elif lang == "italian":
            results = search_italian(q)
        elif lang == "english":
            all_products = db.all()
            for product in all_products:
                title_en = product.get("name", {}).get("en", "").lower()
                desc_en = product.get("description", {}).get("en", "").lower()
                if q.lower() in title_en or q.lower() in desc_en:
                    matched.append(product)
            continue
        else:
            continue

        # 🧼 Unwrap { "product": ..., "score": ... } structure
        for r in results:
            product = r["product"]
            product["score"] = r.get("score", 0.0)  # Optional: attach score
            matched.append(product)

    return {
        "translations": translations,
        "products": matched
    }



@app.get("/product/{id}", response_model=Product)
def get_product(id: int):
    ProductQuery = TinyQuery()
    result = db.get(ProductQuery.id == id)
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")
    return result
