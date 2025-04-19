from tinydb import TinyDB, Query
from mBART.run_cn_pipeline import run_chinese_query

def search_chinese_backend(query, top_k=5):
    # 1. Run pipeline and get {product_name_zh: score}
    ranked_names = run_chinese_query(query)

    # 2. Load TinyDB
    db = TinyDB(REMOVED_SECRETdata/products.jsonREMOVED_SECRET)
    Product = Query()

    # 3. Match top_k product names with TinyDB entries
    matched_products = []
    for name_zh, score in ranked_names.items():
        results = db.search(Product.name.zh == name_zh)
        if results:
            matched_products.append({
                REMOVED_SECRETproductREMOVED_SECRET: results[0],
                REMOVED_SECRETscoreREMOVED_SECRET: score
            })
            if len(matched_products) >= top_k:
                break

    return matched_products
