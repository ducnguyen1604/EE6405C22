from search_modules.chinese import search_chinese

def print_results(results):
    print("\n🧪 Raw Output Structure:")
    print(f"Type: {type(results)}")
    if isinstance(results, list):
        print(f"Length: {len(results)}")
        if results:
            print("First item keys:", results[0].keys())
            print("First item sample:", results[0])
        else:
            print("List is empty.")
    
    print("\n✅ Top Matching Results:\n")
    if not results:
        print("❌ No matching results found in TinyDB.")
        return

    for i, item in enumerate(results, start=1):
        product = item["product"]
        score = item["score"]
        name = product.get("name", {}).get("zh", "Unnamed")
        desc = product.get("description", {}).get("zh", "No description")
        image = product.get("image", "N/A")

        print(f"{i}. 🛍 {name}")
        print(f"   📝 Description: {desc}")
        print(f"   🖼 Image: {image}")
        print(f"   📊 BERT Score: {score:.4f}\n")

if __name__ == "__main__":
    print("💡 Example queries: 短袖, 裙子, 牛仔裤")
    query = input("🔍 Enter a Chinese product search query: ")
    results = search_chinese(query)
    print_results(results)
