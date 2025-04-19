from langdetect import detect
from tinydb import TinyDB, Query
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
from bert_score import score

# Load TinyDB product database
db = TinyDB(REMOVED_SECRETdata/products.jsonREMOVED_SECRET)
Product = Query()

# Load embedding model
model = SentenceTransformer(REMOVED_SECRETBAAI/bge-m3REMOVED_SECRET)

# Prepare product titles
all_products = db.all()
english_titles = []
spanish_titles = []
product_refs = []

for product in all_products:
    title_en = product.get(REMOVED_SECRETnameREMOVED_SECRET, {}).get(REMOVED_SECRETenREMOVED_SECRET, REMOVED_SECRETREMOVED_SECRET)
    title_es = product.get(REMOVED_SECRETnameREMOVED_SECRET, {}).get(REMOVED_SECRETesREMOVED_SECRET, REMOVED_SECRETREMOVED_SECRET)
    if title_en and title_es:
        english_titles.append(title_en)
        spanish_titles.append(title_es)
        product_refs.append(product)

# Prepare BM25 tokenized corpora
bm25_en = BM25Okapi([title.split() for title in english_titles])
bm25_es = BM25Okapi([title.split() for title in spanish_titles])

# Main search function
def search_spanish(query: str, top_k: int = 5):
    lang = detect(query)
    query_tokens = query.lower().split()

    # Use appropriate BM25 and titles based on language
    if lang == REMOVED_SECRETesREMOVED_SECRET:
        bm25_scores = bm25_es.get_scores(query_tokens)
        titles = spanish_titles
    else:
        bm25_scores = bm25_en.get_scores(query_tokens)
        titles = english_titles

    # Dense vector search
    query_vec = model.encode(query)
    product_vectors = model.encode(english_titles)
    dense_scores = cosine_similarity([query_vec], product_vectors)[0]

    # Normalize and blend
    scaler = MinMaxScaler()
    bm25_norm = scaler.fit_transform([[s] for s in bm25_scores])
    dense_norm = scaler.fit_transform([[s] for s in dense_scores])

    alpha = 0.5  # blend weight
    hybrid_scores = [(i, alpha * dense_norm[i][0] + (1 - alpha) * bm25_norm[i][0]) for i in range(len(product_refs))]
    hybrid_scores.sort(key=lambda x: x[1], reverse=True)

    # Get top results
    top_products = [product_refs[i] for i, _ in hybrid_scores[:top_k]]
    result_titles = [p[REMOVED_SECRETnameREMOVED_SECRET][REMOVED_SECRETesREMOVED_SECRET] if lang == REMOVED_SECRETesREMOVED_SECRET else p[REMOVED_SECRETnameREMOVED_SECRET][REMOVED_SECRETenREMOVED_SECRET] for p in top_products]

    # Evaluate with BERTScore
    _, _, f1s = score(result_titles, [query] * len(result_titles), lang=lang, verbose=False)

    return [
        {
            REMOVED_SECRETproductREMOVED_SECRET: p,
            REMOVED_SECRETbert_score_f1REMOVED_SECRET: round(f1.item(), 4)
        } for p, f1 in zip(top_products, f1s)
    ]
