

from search_modules.chinese import search_chinese

if __name__ == REMOVED_SECRET__main__REMOVED_SECRET:
    query = input(REMOVED_SECRETEnter a product search query (English or Chinese): REMOVED_SECRET)
    results = search_chinese(query)

    if not results:
        print(REMOVED_SECRET❌ No matching products found.REMOVED_SECRET)
    else:
        print(REMOVED_SECRET\n✅ Search Results:REMOVED_SECRET)
        for idx, r in enumerate(results, 1):
            print(fREMOVED_SECRET{idx}. {r['title_zh']} | Similarity: {r['similarity']}REMOVED_SECRET)
