import os
from .mtpipeline import init_mt_environment, mt_pipeline_search

def run_chinese_query(query):
    # Dynamically construct paths relative to this file's location
    base_path = os.path.dirname(__file__)
    data_paths = {
        'cn': os.path.join(base_path, 'en_to_cn_embeddings.pkl'),
        'es': os.path.join(base_path, 'en_to_sp_embeddings.pkl'),
        'it': os.path.join(base_path, 'en_to_it_embeddings.pkl')
    }

    mBART_model_path = os.path.join(base_path, "final")
    embed_model = "BAAI/bge-m3"
    env_path = os.path.join(base_path, ".env")

    # Initialize environment
    mBART_model, mBART_tokenizer, data, bm25_corpus, dense_embed_model, pinecone_indices = init_mt_environment(
        mBART_model_path, data_paths, embed_model, env_path
    )

    # Run pipeline for Chinese (tgt_lang='cn')
    final_output = mt_pipeline_search(
        query=query,
        tgt_lang='it',
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
if __name__ == "__main__":
    query = input("🔍 Enter a Chinese query to test the pipeline: ")
    result = run_chinese_query(query)

    print("\n📦 Type of result:", type(result))
    print("🧪 Is dictionary?", isinstance(result, dict))
    print("\n✅ Sample Output:\n")
    for i, (product, score) in enumerate(result.items()):
        print(f"{i+1}. {product[:50]} → BERTScore: {score:.4f}")
        if i == 4: break
