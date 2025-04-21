from langdetect import detect
from tinydb import TinyDB, Query
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
from bert_score import score

import os
import re

# Load TinyDB product database
db = TinyDB("data/products.json")
Product = Query()

# Load embedding model
model = SentenceTransformer("BAAI/bge-m3")

# Load Italian product titles and English originals
all_products = db.all()
english_titles = []
italian_titles = []
product_refs = []

for product in all_products:
    title_en = product.get("name", {}).get("en", "")
    title_it = product.get("name", {}).get("it", "")
    if title_en and title_it:
        english_titles.append(title_en)
        italian_titles.append(title_it)
        product_refs.append(product)

# Tokenized versions for BM25
bm25_en = BM25Okapi([title.split() for title in english_titles])
bm25_it = BM25Okapi([title.split() for title in italian_titles])

# --- Hybrid search ---
def search_italian(query: str, top_k: int = 5):
    lang = detect(query)
    query_tokens = query.lower().split()

    # BM25
    bm25_scores = bm25_it.get_scores(query_tokens) if lang == "it" else bm25_en.get_scores(query_tokens)

    # Dense vector
    query_vec = model.encode(query)
    product_vectors = model.encode(english_titles)
    dense_scores = cosine_similarity([query_vec], product_vectors)[0]

    scaler = MinMaxScaler()
    bm25_norm = scaler.fit_transform([[s] for s in bm25_scores])
    dense_norm = scaler.fit_transform([[s] for s in dense_scores])

    # Combine
    alpha = 0.5
    hybrid_scores = [(i, alpha * dense_norm[i][0] + (1 - alpha) * bm25_norm[i][0]) for i in range(len(product_refs))]
    hybrid_scores.sort(key=lambda x: x[1], reverse=True)

    top_products = [product_refs[i] for i, _ in hybrid_scores[:top_k]]
    titles = [p["name"]["it"] for p in top_products]
    _, _, f1s = score(titles, [query] * len(titles), lang="it", verbose=False)

    return [
        {
            "product": p,
            "bert_score_f1": round(f1.item(), 4)
        } for p, f1 in zip(top_products, f1s)
    ]