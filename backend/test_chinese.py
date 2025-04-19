from search_modules.chinese import search_chinese_backend

def print_results(results):
    if not results:
        print(REMOVED_SECRET❌ No matching results found in TinyDB.REMOVED_SECRET)
        return

    print(REMOVED_SECRET\n✅ Top Matching Results:\nREMOVED_SECRET)
    for i, item in enumerate(results, start=1):
        product = item[REMOVED_SECRETproductREMOVED_SECRET]
        score = item[REMOVED_SECRETscoreREMOVED_SECRET]
        name = product.get(REMOVED_SECRETnameREMOVED_SECRET, {}).get(REMOVED_SECRETzhREMOVED_SECRET, REMOVED_SECRETUnnamedREMOVED_SECRET)
        desc = product.get(REMOVED_SECRETdescriptionREMOVED_SECRET, {}).get(REMOVED_SECRETzhREMOVED_SECRET, REMOVED_SECRETNo descriptionREMOVED_SECRET)
        image = product.get(REMOVED_SECRETimageREMOVED_SECRET, REMOVED_SECRETN/AREMOVED_SECRET)

        print(fREMOVED_SECRET{i}. 🛍 {name}REMOVED_SECRET)
        print(fREMOVED_SECRET   📝 Description: {desc}REMOVED_SECRET)
        print(fREMOVED_SECRET   🖼 Image: {image}REMOVED_SECRET)
        print(fREMOVED_SECRET   📊 BERT Score: {score:.4f}\nREMOVED_SECRET)

if __name__ == REMOVED_SECRET__main__REMOVED_SECRET:
    print(REMOVED_SECRET💡 Example queries: 短袖, 裙子, 牛仔裤REMOVED_SECRET)
    query = input(REMOVED_SECRET🔍 Enter a Chinese product search query: REMOVED_SECRET)
    results = search_chinese_backend(query)
    print_results(results)
