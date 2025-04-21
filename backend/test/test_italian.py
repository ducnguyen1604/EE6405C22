from search_modules.italian import search_italian

if __name__ == "__main__":
    query = input("Enter a product search query (e.g., 'shirt'): ")
    results = search_italian(query)

    if not results:
        print("❌ No matching products found.")
    else:
        print("\n✅ Search Results:")
        for idx, r in enumerate(results, 1):
            name = r['product']['name'].get('it', 'N/A')
            desc = r['product']['description'].get('it', '')
            price = r['product'].get('price', 'N/A')
            print(f"{idx}. {name} | €{price} | BERT F1: {r['bert_score_f1']}")
            if desc:
                print(f"   → {desc}\n")
