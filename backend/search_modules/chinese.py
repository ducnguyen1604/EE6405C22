from tinydb import TinyDB, Query
from mBART.run_cn_pipeline import run_chinese_query

def search_chinese(query, top_k=5):
    # 1. Run pipeline and get {product_name_zh: score}
    ranked_names = run_chinese_query(query)

    # 2. Load TinyDB
    db = TinyDB("data/products.json")
    Product = Query()

    # 3. Match top_k product names with TinyDB entries
    matched_products = []
    for name_zh, score in ranked_names.items():
        results = db.search(Product.name.zh == name_zh)
        if results:
            matched_products.append({
                "product": results[0],
                "score": score
            })
            if len(matched_products) >= top_k:
                break

    return matched_products
