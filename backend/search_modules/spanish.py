from tinydb import TinyDB, Query
from mBART.run_es_pipeline import run_spanish_query

def search_spanish(query, top_k=5):
    # 1. Run pipeline and get {product_name_zh: score}
    ranked_names = run_spanish_query(query)

    # 2. Load TinyDB
    db = TinyDB("data/products.json")
    Product = Query()

    # 3. Match top_k product names with TinyDB entries
    matched_products = []
    for name_es, score in ranked_names.items():
        results = db.search(Product.name.es == name_es)
        if results:
            matched_products.append({
                "product": results[0],
                "score": score
            })
            if len(matched_products) >= top_k:
                break

    return matched_products
