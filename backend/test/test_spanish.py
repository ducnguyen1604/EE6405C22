from search_modules.spanish import search_spanish

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
        name = product.get("name", {}).get("es", "Unnamed")
        desc = product.get("description", {}).get("es", "No description")
        image = product.get("image", "N/A")

        print(f"{i}. 🛍 {name}")
        print(f"   📝 Description: {desc}")
        print(f"   🖼 Image: {image}")
        print(f"   📊 BERT Score: {score:.4f}\n")

if __name__ == "__main__":
    query = input("🔍 Enter a Spanish product search query: ")
    results = search_spanish(query)
    print_results(results)
