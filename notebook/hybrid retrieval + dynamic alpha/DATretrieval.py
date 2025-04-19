import numpy as np
import time
import os
import json
import re
from dotenv import load_dotenv
from langdetect import detect
from sklearn.preprocessing import MinMaxScaler
from rank_bm25 import BM25Okapi
import pandas as pd
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from bert_score import score
from openai import OpenAI

# Load API key from .env file
load_dotenv(dotenv_path='../.env')
CHARRAN_API = os.getenv('CHARRAN_API')
CHERYL_API = os.getenv('CHERYL_API')
deepseek_API_KEY = os.getenv('deepseek_API_KEY')

# Initialize Pinecone
pc = Pinecone(api_key=CHARRAN_API)
index = pc.Index('italian-db')

# Load sentence embedding model
model = SentenceTransformer(REMOVED_SECRETBAAI/bge-m3REMOVED_SECRET)

# Load embeddings and titles
italian_embeddings = pd.read_pickle(REMOVED_SECRETen_to_it_embeddings.pklREMOVED_SECRET)
english_titles = italian_embeddings['title']
italian_titles = italian_embeddings['title_italian']

# Tokenize for BM25
tokenized_en = [title.split() for title in english_titles]
tokenized_it = [title.split() for title in italian_titles]

# Initialize BM25 indexes
bm25_en = BM25Okapi(tokenized_en)
bm25_it = BM25Okapi(tokenized_it)

#Improved prompt for dynamic alpha calculation using LLM

# Set your OpenAI API key
client = OpenAI(api_key= deepseek_API_KEY, base_url=REMOVED_SECREThttps://openrouter.ai/api/v1REMOVED_SECRET)
# prompting for dynamic alpha calculation
def get_dynamic_alpha(question, dense_result, bm25_result):
    system_prompt = REMOVED_SECRETREMOVED_SECRETREMOVED_SECRETYou are a multilingual evaluator in an Italian e-commerce site assessing the retrieval effectiveness of dense
retrieval (Cosine Distance) and BM25 retrieval for finding the correct Italian product title given an English-language query.

## Task:
Given a query and two top-1 search results (one from dense retrieval, one from BM25 retrieval), score each method from **0 to 5** based on how likely the correct result is retrieved or nearby.

### Scoring Criteria:
1. **Direct hit → 5 points**
   - If the retrieved result directly answers the question.
2. **Good wrong result → 3-4 points**
   - Answer is not exact, but closely related; likely the correct one is nearby.
3. **Bad wrong result → 1-2 points**
   - Loosely related or general, unlikely correct answer is nearby.
4. **Completely off-track → 0 points**
   - Retrieval is unrelated.

### Output Format:
Return two integers separated by a space:
- First number: dense retrieval score.
- Second number: BM25 retrieval score.
REMOVED_SECRETREMOVED_SECRETREMOVED_SECRET

    user_prompt = fREMOVED_SECRETREMOVED_SECRETREMOVED_SECRET### Given Data:
- Question: REMOVED_SECRET{question}REMOVED_SECRET
- dense retrieval Top1 Result: REMOVED_SECRET{dense_result}REMOVED_SECRET
- BM25 retrieval Top1 Result: REMOVED_SECRET{bm25_result}REMOVED_SECRET
REMOVED_SECRETREMOVED_SECRETREMOVED_SECRET

    response = client.chat.completions.create(
        model=REMOVED_SECRETdeepseek/deepseek-chat-v3-0324:freeREMOVED_SECRET,
        messages=[
            {REMOVED_SECRETroleREMOVED_SECRET: REMOVED_SECRETsystemREMOVED_SECRET, REMOVED_SECRETcontentREMOVED_SECRET: system_prompt},
            {REMOVED_SECRETroleREMOVED_SECRET: REMOVED_SECRETuserREMOVED_SECRET, REMOVED_SECRETcontentREMOVED_SECRET: user_prompt}
        ],
        temperature=0
    )

    output = response.choices[0].message.content.strip()

    try:
        dense_score, bm25_score = map(int, output.split())
    except:
        dense_score = bm25_score = 3  # fallback if parsing fails

    if dense_score == 5 and bm25_score != 5:
        return 1.0
    elif bm25_score == 5 and dense_score != 5:
        return 0.0
    elif dense_score == 0 and bm25_score == 0:
        return 0.5
    else:
        return dense_score / (dense_score + bm25_score)

# Step 2: Main hybrid retrieval with dynamic alpha and BERTScore evaluation

def hybrid_search_dat(query, top_k=5):
    lang = detect(query)
    tokens = query.lower().split()

    # --- BM25 Search ---
    if lang == 'it':
        bm25_scores = bm25_it.get_scores(tokens)
    else:
        bm25_scores = bm25_en.get_scores(tokens)

    # --- Semantic Search (Pinecone) ---
    query_vec = model.encode(query).tolist()
    pinecone_results = index.query(vector=query_vec, top_k=top_k, include_metadata=False)

    # Parse Pinecone results
    pinecone_ids = [int(match['id'].split('-')[1]) for match in pinecone_results['matches']]
    pinecone_scores = [match['score'] for match in pinecone_results['matches']]

    # Get top-1 text from both for alpha calculation
    bm25_top_idx = int(np.argmax(bm25_scores))
    dense_top_idx = pinecone_ids[0]
    bm25_text = italian_embeddings['title'][bm25_top_idx]
    dense_text = italian_embeddings['title'][dense_top_idx]

    # --- Get dynamic alpha from GPT ---
    start = time.time()
    alpha = get_dynamic_alpha(query, dense_text, bm25_text)
    #print(fREMOVED_SECRETAlpha fetched: {alpha} in {time.time() - start:.2f}sREMOVED_SECRET)

    # --- Normalize Scores ---
    scaler = MinMaxScaler()
    bm25_norm = scaler.fit_transform(np.array(bm25_scores).reshape(-1, 1)).flatten()
    pinecone_norm = scaler.fit_transform(np.array(pinecone_scores).reshape(-1, 1)).flatten()

    # --- Combine scores using dynamic alpha ---
    hybrid_results = []
    for idx, semantic_score in zip(pinecone_ids, pinecone_norm):
        final_score = alpha * semantic_score + (1 - alpha) * bm25_norm[idx]
        hybrid_results.append((idx, final_score))

    # Sort by hybrid score
    hybrid_results.sort(key=lambda x: x[1], reverse=True)

    # --- Prepare and return top-k titles with BERTScores ---
    titles = [italian_embeddings['title_italian'][idx] for idx, _ in hybrid_results[:top_k]]
    reference_query = query
    _, _, F1 = score(titles, [reference_query] * len(titles), lang=REMOVED_SECRETmultilingualREMOVED_SECRET, verbose=False)

    output = [
        {
            REMOVED_SECRETtitle_italianREMOVED_SECRET: title,
            REMOVED_SECRETbert_score_f1REMOVED_SECRET: round(f1.item(), 4)
        }
        for title, f1 in zip(titles, F1)
    ]

    return output

#example to run the code

if __name__ == REMOVED_SECRET__main__REMOVED_SECRET:
    query = REMOVED_SECRETMen's white shirtREMOVED_SECRET
    results = hybrid_search_dat(query, top_k=5)
    for result in results:
        print(result)
