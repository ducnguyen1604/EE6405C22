import numpy as np
import pandas as pd
from rank_bm25 import BM25Okapi
import jieba
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from pinecone import ServerlessSpec
from dotenv import load_dotenv
import os
from bert_score import score
import warnings

#returns dictionary of dfs of our db
def get_data(data_paths):
    data = {} 
    for lang, path in data_paths.items():
        data[lang]=pd.read_pickle(path)
    return data

#Build BM_25 corpus
def build_BM25(data):
    #cn
    entocn_chinese_titles = data['cn']['chinese translation']
    entocn_tokenized_cn = [list(jieba.cut_for_search(title.lower())) for title in entocn_chinese_titles]
    bm25_cn = BM25Okapi(entocn_tokenized_cn)

    #es
    entoes_spanish_titles = data['es']['title_spanish']
    entoes_tokenized_es = [title.split() for title in entoes_spanish_titles]
    bm25_es = BM25Okapi(entoes_tokenized_es)

    #it
    entoit_italian_titles = data['it']['title_italian']
    entoit_tokenized_it = [title.split() for title in entoit_italian_titles]
    bm25_it = BM25Okapi(entoit_tokenized_it)

    bm25_corpus={'cn':bm25_cn, 'es':bm25_es, 'it':bm25_it}


    return bm25_corpus

#Search BM25
def search_bm25_expanded(query_list, corpus, tgt_lang='cn', top_k=5):
    #init scores as zeros

    scores = [0.0] * len(corpus[tgt_lang].doc_len)

    for query_dict in query_list:
        term=query_dict['term']
        weight=query_dict['weight']
        if tgt_lang=='cn':
            tokens=jieba.cut_for_search(term.lower())
            term_scores = corpus[tgt_lang].get_scores(tokens)        
        else:
            tokens = term.lower().split()
            term_scores = corpus[tgt_lang].get_scores(tokens)

        scores = [s + weight * ts for s, ts in zip(scores, term_scores)]

    # Get top-k ranked indices
    top_k_ids = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    return top_k_ids, [scores[i] for i in top_k_ids]

#Embeds a dense embedding representing the weighted mean of the expanded queries
def embed_expanded(query_list, model):
    query_embeddings= []
    #embed expanded queries
    for query_dict in query_list:
        embedding=model.encode(query_dict['term'],  convert_to_tensor=True).cpu().numpy() #size1024
        query_embeddings.append(embedding * query_dict["weight"])

    query_embedding = sum(query_embeddings) / len(query_embeddings)  # Weighted mean
    return query_embedding


def init_index(pc, index_name, data, embedding_col, eng_col, tgt_col, tgt_lang):
    index_name = index_name
    dimension = 1024

    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",  # by cosine similarity
            spec=ServerlessSpec(
                cloud="aws",  # or "gcp"
                region="us-east-1" 
            )
        )

        index = pc.Index(index_name)
        print("Upserting vectors...")
        vectors_to_upsert = []
        for _, row in data.iterrows():
            vectors_to_upsert.append({
                "id": str(_),  # Use index or generate unique IDs
                "values": row[embedding_col],  # Using Chinese embeddings
                "metadata": {
                    "title": row[eng_col],
                    "chinese_title": row[tgt_col],
                    "embedding_type": tgt_lang  # Track which embedding was used
                }
            })

        for i in range(0, len(vectors_to_upsert), 100):
            index.upsert(vectors=vectors_to_upsert[i:i+100])

    else:
        index = pc.Index(index_name)

def setup_pinecone(data, env_path):
    load_dotenv(dotenv_path=env_path)
    pinecone_api_key = os.getenv('pinecone_API_KEY')
    pc = Pinecone(api_key=pinecone_api_key, environment='nlp-proj')

    data = data
    
    indexes={'cn':'cn-search', 'it':'it-search', 'es':'es-search'}

    
    #setup cn
    init_index(pc, index_name=indexes['cn'], data=data['cn'],
     embedding_col='chinese_embedding',
     eng_col='title',
     tgt_col='chinese translation',
     tgt_lang='chinese')

    #setup it
    init_index(pc, index_name=indexes['it'], data=data['it'],
     embedding_col='italian_embedding',
     eng_col='title',
     tgt_col='title_italian',
     tgt_lang='italian')

    #setup es
    init_index(pc, index_name=indexes['es'], data=data['es'],
     embedding_col='spanish_embedding',
     eng_col='title',
     tgt_col='title_spanish',
     tgt_lang='spanish')
    
     
    return indexes

def search_pinecone(query_list, embedding_model, index_name, env_path, top_k=5):
    load_dotenv(dotenv_path=env_path)
    pinecone_api_key = os.getenv('pinecone_API_KEY')
    pc = Pinecone(api_key=pinecone_api_key, environment='nlp-proj')
    index = pc.Index(index_name)
    query_embedding=embed_expanded(query_list, embedding_model)
    results = index.query(
            vector=query_embedding.tolist(),
            top_k=top_k,
            include_metadata=False
        )
    id_list = []
    score_list = []
    for dict in results.matches:
        id_list.append(int(dict['id']))
        score_list.append(float(dict['score']))

    return id_list, score_list

def scores_to_ranking(scores: list[float]) -> list[int]:
    """Convert float scores into int rankings (1 = best)."""
    return np.argsort(scores)[::-1] + 1  # ranks start at 1

def rrf(keyword_rank: int, semantic_rank: int, k: int = 60) -> float:
    """Combine keyword rank and semantic rank into a hybrid score using RRF."""
    return 1 / (k + keyword_rank) + 1 / (k + semantic_rank)

def hybrid_expanded_search(query_list, bm25_corpus, pinecone_indices, embedding_model, env_path, tgt_lang='cn', top_k=5 ):
    bm25_top_ids, bm25_top_scores = search_bm25_expanded(query_list, bm25_corpus, top_k=top_k)
    pc_top_ids, pc_top_scores =search_pinecone(query_list, embedding_model, pinecone_indices[tgt_lang], env_path, top_k=top_k)
    bm25_ranks = scores_to_ranking(bm25_top_scores)
    pc_ranks = scores_to_ranking(pc_top_scores)

    # Create dictionaries for quick rank lookup
    bm25_rank_dict = {doc_id: rank for doc_id, rank in zip(bm25_top_ids, bm25_ranks)}
    pc_rank_dict = {doc_id: rank for doc_id, rank in zip(pc_top_ids, pc_ranks)}
    
    # Combine all unique document IDs from both methods
    all_doc_ids = list(set(bm25_top_ids) | set(pc_top_ids))
    
    # Calculate RRF scores for each document
    rrf_scores = []
    for doc_id in all_doc_ids:
        # Get ranks from each method (use a high rank if document not found)
        bm25_rank = bm25_rank_dict.get(doc_id, top_k * 2)  # Penalize missing documents
        pc_rank = pc_rank_dict.get(doc_id, top_k * 2)
        
        # Calculate combined RRF score
        score = rrf(bm25_rank, pc_rank)
        rrf_scores.append((doc_id, score))
    
    # Sort documents by RRF score (descending)
    rrf_scores.sort(key=lambda x: -x[1])
    
    # Extract the top_k document IDs
    #hybrid_top_ids = [doc_id for doc_id, score in rrf_scores[:top_k]]
    hybrid_top_ids = [doc_id for doc_id, score in rrf_scores]

    #hybrid_top_scores = [score for doc_id, score in rrf_scores[:top_k]]
    hybrid_top_scores = [score for doc_id, score in rrf_scores]
    
    return hybrid_top_ids, hybrid_top_scores

def calculate_bertscore(candidate, reference, lang = "en"):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # Compute scores
        P, R, F1 = score(
            [candidate], 
            [reference], 
            lang=lang,
            model_type="bert-base-multilingual-cased",  # Multilingual BERT
            verbose=False  # Disable progress messages
        )
    return P.item(), R.item(), F1.item()


def get_final_output(query, hybrid_top_id, data, tgt_lang='cn',debug=False):
    if debug:
        tgt_results = []
        english_results = []
        for ids in hybrid_top_id:
            if tgt_lang=='cn':
                tgt_results.append(data[tgt_lang]['chinese translation'][ids])
                english_results.append(data[tgt_lang]['title'][ids])
            elif tgt_lang=='es':
                tgt_results.append(data[tgt_lang]['title_spanish'][ids])
                english_results.append(data[tgt_lang]['title'][ids])
            elif tgt_lang=='it':
                tgt_results.append(data[tgt_lang]['title_italian'][ids])
                english_results.append(data[tgt_lang]['title'][ids])
        result_df=pd.DataFrame({'en':english_results, 'tgt':tgt_results})
        return result_df

    else:
        final_output={}
        for ids in hybrid_top_id:
            if tgt_lang=='cn':
                txt=data[tgt_lang]['chinese translation'][ids]
            elif tgt_lang=='es':
                txt=data[tgt_lang]['title_spanish'][ids]
            elif tgt_lang=='it':
                txt=data[tgt_lang]['title_italian'][ids]

            acc, precision, f1 = calculate_bertscore(txt, query)
            final_output[txt]=f1
        return final_output