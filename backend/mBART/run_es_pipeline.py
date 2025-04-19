import os
from .mtpipeline import init_mt_environment, mt_pipeline_search

def run_spanish_query(query):
    # Dynamically construct paths relative to this file's location
    base_path = os.path.dirname(__file__)
    data_paths = {
        'cn': os.path.join(base_path, 'en_to_cn_embeddings.pkl'),
        'es': os.path.join(base_path, 'en_to_sp_embeddings.pkl'),
        'it': os.path.join(base_path, 'en_to_it_embeddings.pkl')
    }

    mBART_model_path = os.path.join(base_path, REMOVED_SECRETfinalREMOVED_SECRET)
    embed_model = REMOVED_SECRETBAAI/bge-m3REMOVED_SECRET
    env_path = os.path.join(base_path, REMOVED_SECRET.envREMOVED_SECRET)

    # Initialize environment
    mBART_model, mBART_tokenizer, data, bm25_corpus, dense_embed_model, pinecone_indices = init_mt_environment(
        mBART_model_path, data_paths, embed_model, env_path
    )

    # Run pipeline for Chinese (tgt_lang='cn')
    final_output = mt_pipeline_search(
        query=query,
        tgt_lang='es',
        env_path=env_path,
        mBART_model=mBART_model,
        mBART_tokenizer=mBART_tokenizer,
        data=data,
        bm25_corpus=bm25_corpus,
        dense_embed_model=dense_embed_model,
        pinecone_indices=pinecone_indices
    )

    return final_output  # Dictionary: {product_name_zh: bert_score}


# CLI testing
if __name__ == REMOVED_SECRET__main__REMOVED_SECRET:
    query = input(REMOVED_SECRET🔍 Enter a Spanish query to test the pipeline: REMOVED_SECRET)
    result = run_spanish_query(query)

    print(REMOVED_SECRET\n📦 Type of result:REMOVED_SECRET, type(result))
    print(REMOVED_SECRET🧪 Is dictionary?REMOVED_SECRET, isinstance(result, dict))
    print(REMOVED_SECRET\n✅ Sample Output:\nREMOVED_SECRET)
    for i, (product, score) in enumerate(result.items()):
        print(fREMOVED_SECRET{i+1}. {product[:50]} → BERTScore: {score:.4f}REMOVED_SECRET)
        if i == 4: break
