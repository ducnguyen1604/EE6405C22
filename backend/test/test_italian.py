from search_modules.italian import search_italian

if __name__ == REMOVED_SECRET__main__REMOVED_SECRET:
    query = input(REMOVED_SECRETEnter a product search query (e.g., 'shirt'): REMOVED_SECRET)
    results = search_italian(query)

    if not results:
        print(REMOVED_SECRET❌ No matching products found.REMOVED_SECRET)
    else:
        print(REMOVED_SECRET\n✅ Search Results:REMOVED_SECRET)
        for idx, r in enumerate(results, 1):
            name = r['product']['name'].get('it', 'N/A')
            desc = r['product']['description'].get('it', '')
            price = r['product'].get('price', 'N/A')
            print(fREMOVED_SECRET{idx}. {name} | €{price} | BERT F1: {r['bert_score_f1']}REMOVED_SECRET)
            if desc:
                print(fREMOVED_SECRET   → {desc}\nREMOVED_SECRET)
