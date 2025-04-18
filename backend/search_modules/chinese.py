from langdetect import detect
from mBART.mtpipeline import init_mt_environment, mt_pipeline_search

# Initialize models once (assumed already downloaded)
mBART_model_path = REMOVED_SECRET../mBART/finalREMOVED_SECRET
data_paths = {
    'cn': 'mBART/en_to_cn_embeddings.pkl',
    'es': 'mBART/en_to_sp_embeddings.pkl',
    'it': 'mBART/en_to_it_embeddings.pkl'
}
embed_model = REMOVED_SECRETBAAI/bge-m3REMOVED_SECRET
env_path = REMOVED_SECRET../.envREMOVED_SECRET

# Only run once
mBART_model, mBART_tokenizer, data, bm25_corpus, dense_embed_model, pinecone_indices = init_mt_environment(
    mBART_model_path, data_paths, embed_model, env_path
)

def search_chinese(query: str, top_k: int = 5):
    lang = detect(query)
    if lang == REMOVED_SECRETzh-cnREMOVED_SECRET or lang == REMOVED_SECRETzhREMOVED_SECRET or any(ord(c) > 127 for c in query):
        # Query is already in Chinese, skip translation
        query_lang = REMOVED_SECRETcnREMOVED_SECRET
    else:
        # Assume English, translate internally inside mt_pipeline
        query_lang = REMOVED_SECRETcnREMOVED_SECRET

    results = mt_pipeline_search(
        query=query,
        env_path=env_path,
        mBART_model=mBART_model,
        mBART_tokenizer=mBART_tokenizer,
        data=data,
        bm25_corpus=bm25_corpus,
        pinecone_indices=pinecone_indices,
        dense_embed_model=dense_embed_model,
        tgt_lang=query_lang,
        top_k=top_k
    )

    output = []
    for title, score in results.items():
        output.append({
            REMOVED_SECRETtitle_zhREMOVED_SECRET: title,
            REMOVED_SECRETsimilarityREMOVED_SECRET: round(score, 4)
        })
    return output
