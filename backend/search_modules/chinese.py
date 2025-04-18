from langdetect import detect
from tinydb import TinyDB
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
from bert_score import score

# Load TinyDB product database
db = TinyDB(REMOVED_SECRETdata/products.jsonREMOVED_SECRET)
all_products = db.all()

# Initialize embedding model
model = SentenceTransformer(REMOVED_SECRETBAAI/bge-m3REMOVED_SECRET)

# Preprocess titles
english_titles = []
chinese_titles = []
product_refs = []

for product in all_products:
    title_en = product.get(REMOVED_SECRETnameREMOVED_SECRET, {}).get(REMOVED_SECRETenREMOVED_SECRET, REMOVED_SECRETREMOVED_SECRET)
    title_zh = product.get(REMOVED_SECRETnameREMOVED_SECRET, {}).get(REMOVED_SECRETzhREMOVED_SECRET, REMOVED_SECRETREMOVED_SECRET)
    if title_en and title_zh:
        english_titles.append(title_en)
        chinese_titles.append(title_zh)
        product_refs.append(product)

# BM25 tokenization
bm25_en = BM25Okapi([title.split() for title in english_titles])
bm25_zh = BM25Okapi([title.split() for title in chinese_titles])


def search_chinese(query: str, top_k: int = 5):
    lang = detect(query)
    query_tokens = query.lower().split()

    if lang.startswith(REMOVED_SECRETzhREMOVED_SECRET) or any(ord(c) > 127 for c in query):
        bm25_scores = bm25_zh.get_scores(query_tokens)
        titles = chinese_titles
    else:
        bm25_scores = bm25_en.get_scores(query_tokens)
        titles = english_titles

    query_vec = model.encode(query)
    product_vectors = model.encode(english_titles)
    dense_scores = cosine_similarity([query_vec], product_vectors)[0]

    scaler = MinMaxScaler()
    bm25_norm = scaler.fit_transform([[s] for s in bm25_scores])
    dense_norm = scaler.fit_transform([[s] for s in dense_scores])

    alpha = 0.5
    hybrid_scores = [
        (i, alpha * dense_norm[i][0] + (1 - alpha) * bm25_norm[i][0])
        for i in range(len(product_refs))
    ]
    hybrid_scores.sort(key=lambda x: x[1], reverse=True)

    top_products = [product_refs[i] for i, _ in hybrid_scores[:top_k]]
    titles_zh = [p[REMOVED_SECRETnameREMOVED_SECRET][REMOVED_SECRETzhREMOVED_SECRET] for p in top_products]
    _, _, f1s = score(titles_zh, [query] * len(titles_zh), lang=REMOVED_SECRETzhREMOVED_SECRET, verbose=False)

    return [
        {
            REMOVED_SECRETproductREMOVED_SECRET: p,
            REMOVED_SECRETbert_score_f1REMOVED_SECRET: round(f1.item(), 4)
        }
        for p, f1 in zip(top_products, f1s)
    ]
