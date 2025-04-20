This README is created to assist in navigating the hybid retreival and dynamic alpha folder.

1. NLP Capstone Files:
The NLP Capstone Files consists of the main work in this folder:
1.1 NLP Capstone_v1.ipynb: Focuses on dataset exploration as well as sentence versus word embeddings (BGE against FastText) using cosine similarity as metrics.
1.2 NLP Capstone_v2_hybrid_retrieval_search.ipynb: Focuses on Hybrid Retrieval Search. This phase focuses on comparing the performances in search retrieval models between sparse retrieval techniques using term weighting schemes such as BM25 and TF-IDF against hybrid search retrieval methods which incorporates dense retrieval from embeddings generated using BAAI BGE-M3 sentence transformer combined with the sparse retrieval methods. The models explored are BM25 Alone, TF-IDF Alone, BM25 + BGE, and TFIDF + BGE.
1.3 NLP Capstone_v4_LLMbasedquery.ipynb: Focuses on deploying the Dynamic Alpha Tuning, which is the Novel Framework that adaptively adjusts the retrieval weighting coefficient based on the query-specific characteristics. Focus on Italian dataset
1.4 NLP Capstone_Dataprep.ipynb: Focuses on Data Preparation

2. Function .py Files:
2.1 DATretrieval.py: This file contain important functions:
2.1.1 get_dynamic_alpha:
This defines the Dynamic Alpha Tuning (DAT) function which receives both dense and bm25 top-1 result and assigns scores from 0 to 5. The scores are used to compute dynamic alpha which determines the validity of the result from BM25 vs. semantic retrieval for that specific query.
2.1.2 hybrid_search_dat:
This function executes the BM25 and Dense Retrieval. Get top-1 text from both and combine scores for alpha calculation then return top-k titles with BERTScores.

3. Dataset Folder
The Dataset Folder consists of the csv file of the three datasets used:
3.1 Amazon_en_to_es.csv: English and Spanish dataset
3.2 Shopee_CN_to_EN.csv: English and Chinese dataset
3.3 target_en_to_it.csv: English and Italian dataset
as well as the split folder which consists of test, train, and validation of the three datasets.

4. Pickle Files:
These are embedded pickle files to be used in NLP_Capstone_v2 and NLP_Capstone_v4
4.1 en_to_sp_embeddings.pkl: Embeddings pickle file for English and Spanish dataset
4.2 en_to_it_embeddings.pkl: Embeddings pickle file for English and Italian dataset
4.3 en_to_cn_embeddings.pkl. Embeddings pickle file for English and Chinese dataset

