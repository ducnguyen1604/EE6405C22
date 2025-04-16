import numpy as np
import time
import os
import json
import re
from dotenv import load_dotenv
from langdetect import detect
from sklearn.preprocessing import MinMaxScaler
from retrieval.prompt_utils import get_dynamic_alpha  # LLM-based alpha computation
from rank_bm25 import BM25Okapi
import pandas as pd
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

# Load API key from .env file
load_dotenv(dotenv_path='../.env')
API_key = os.getenv(REMOVED_SECRETdeepseek_API_KEYREMOVED_SECRET)

# Initialize Pinecone
pc = Pinecone(api_key=API_key)
index = pc.Index('italian-db')

# Load sentence embedding model
model = SentenceTransformer(REMOVED_SECRETBAAI/bge-m3REMOVED_SECRET)

# Load embeddings and titles
df_embeddings = pd.read_pickle(REMOVED_SECRETen_to_it_embeddings.pklREMOVED_SECRET)
english_titles = df_embeddings['title']
italian_titles = df_embeddings['title_italian']

# Tokenize for BM25
tokenized_en = [title.split() for title in english_titles]
tokenized_it = [title.split() for title in italian_titles]

# Initialize BM25 indexes
bm25_en = BM25Okapi(tokenized_en)
bm25_it = BM25Okapi(tokenized_it)

def hybrid_search_dat(query, top_k=5):
    lang = detect(query)
    tokens = query.lower().split()

    # --- BM25 Search ---
    bm25_scores = bm25_it.get_scores(tokens) if lang == 'it' else bm25_en.get_scores(tokens)

    # --- Semantic Search (Pinecone) ---
    query_vec = model.encode(query).tolist()
    pinecone_results = index.query(vector=query_vec, top_k=top_k, include_metadata=False)
    pinecone_ids = [int(match['id'].split('-')[1]) for match in pinecone_results['matches']]
    pinecone_scores = [match['score'] for match in pinecone_results['matches']]

    # --- Top-1 retrievals for alpha decision ---
    bm25_top_idx = int(np.argmax(bm25_scores))
    dense_top_idx = pinecone_ids[0]
    bm25_text = df_embeddings['title'][bm25_top_idx]
    dense_text = df_embeddings['title'][dense_top_idx]

    start = time.time()
    alpha = get_dynamic_alpha(query, dense_text, bm25_text)
    #print(fREMOVED_SECRETAlpha fetched: {alpha} in {time.time() - start:.2f}sREMOVED_SECRET)

    # --- Normalize Scores ---
    scaler = MinMaxScaler()
    bm25_norm = scaler.fit_transform(np.array(bm25_scores).reshape(-1, 1)).flatten()
    pinecone_norm = scaler.fit_transform(np.array(pinecone_scores).reshape(-1, 1)).flatten()

    # --- Score fusion ---
    hybrid_results = []
    for idx, semantic_score in zip(pinecone_ids, pinecone_norm):
        final_score = alpha * semantic_score + (1 - alpha) * bm25_norm[idx]
        hybrid_results.append((idx, final_score))

    hybrid_results.sort(key=lambda x: x[1], reverse=True)

    # --- Final detailed output ---
    detailed_results = []
    for idx, hybrid_score in hybrid_results[:top_k]:
        bm25_score = round(bm25_norm[idx], 4)
        semantic_score = round(pinecone_norm[pinecone_ids.index(idx)], 4)
        product_id = df_embeddings.iloc[idx]['id'] if 'id' in df_embeddings.columns else idx
        detailed_results.append((product_id, idx, round(hybrid_score, 4), bm25_score, semantic_score))

        output = []
    for product_id, idx, hybrid_score, bm25_score, semantic_score in detailed_results:
        output.append({
            REMOVED_SECRETproduct_idREMOVED_SECRET: product_id,
            REMOVED_SECRETtitle_italianREMOVED_SECRET: df_embeddings['title_italian'][idx],
            REMOVED_SECREThybrid_scoreREMOVED_SECRET: hybrid_score,
            REMOVED_SECRETbm25_scoreREMOVED_SECRET: bm25_score,
            REMOVED_SECRETsemantic_scoreREMOVED_SECRET: semantic_score
        })

    return output
