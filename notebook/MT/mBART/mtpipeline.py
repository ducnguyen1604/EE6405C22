from queryexpansion import expand
from translate import load_model_and_tokenizer, translate_expanded
from search import *
from sentence_transformers import SentenceTransformer

def init_mt_environment(mBART_model_path, data_paths, embed_model, env_path):
    mBART_model,mBART_tokenizer=load_model_and_tokenizer(mBART_model_path)
    data=get_data(data_paths)
    bm25_corpus=build_BM25(data) #From search.py, builds the bm25 corpus
    dense_embed_model=SentenceTransformer(embed_model)
    pinecone_indices=setup_pinecone(data, env_path) #From search.py, sets up vector db

    return mBART_model, mBART_tokenizer, data, bm25_corpus, dense_embed_model, pinecone_indices

#wrapper for easy calling

def mt_pipeline_search(query, env_path, mBART_model, mBART_tokenizer, data, bm25_corpus, pinecone_indices, dense_embed_model, tgt_lang='cn' , top_k=5):

    print('Expanding queries...')
    expanded_queries=expand(query, env_path, include_translations=False)
    print('Queries Expanded')

    print('Translating Queries...')
    weighted_queries = translate_expanded(mBART_model, mBART_tokenizer, expanded_queries, 'en', tgt_lang)
    print('Searching...')
    hybrid_top_id, hybrid_top_scores=hybrid_expanded_search(weighted_queries, bm25_corpus, pinecone_indices, dense_embed_model, env_path, tgt_lang=tgt_lang, top_k=top_k )
    print('Processing Output...')
    final_output = get_final_output(query, hybrid_top_id, data, tgt_lang=tgt_lang)

    return final_output