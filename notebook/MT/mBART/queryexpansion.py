from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import re

def get_openai_client(env_path):
    """Initialize and return an OpenAI client with the appropriate configuration."""
    # Load API key from environment
    load_dotenv(dotenv_path=env_path)
    api_key = os.getenv('deepseek_API_KEY')
    
    # Initialize and return client
    return OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")

def get_expanded_queries(user_query, env_path):
    # Initialize client
    client = get_openai_client(env_path)
    
    prompt=f'''You are an expert search query optimizer. Your task is to expand the following e-commerce search query to improve retrieval of relevant products. Generate a list of semantically related terms, synonyms, and common user variations while preserving the original intent.

**Rules:**
1. Prioritize **contextual relevance** (e.g., "running shoes" → "jogging sneakers").
2. Include **common misspellings** (e.g., "earbuds" → "airbuds").
3. Add **technical/layman variants** (e.g., "4K TV" → "ultra HD television").
4. For non-English queries, provide **translations/transliterations** if applicable (e.g., "スマホ" → "smartphone").
5. Output in JSON format for easy parsing.

**Input Query:** "{user_query}"

**Output Format:**  
{{
  "original_query": "...",
  "expanded_terms": [
    {{"term": "...", "type": "synonym"}},
    {{"term": "...", "type": "misspelling"}},
    {{"term": "...", "type": "technical"}}
  ]
}}

**Example Output for "wireless headphones":**
{{
  "original_query": "wireless headphones",
  "expanded_terms": [
    {{"term": "Bluetooth headphones", "type": "synonym"}},
    {{"term": "cordless earphones", "type": "synonym"}},
    {{"term": "wireless headsets", "type": "synonym"}},
    {{"term": "airbuds", "type": "misspelling"}},
    {{"term": "noise-cancelling headphones", "type": "technical"}}
  ]
}}

**Now process this query:** "{user_query}"'''
    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324:free",
        messages=[
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )
    
    expanded_queries_raw=response.choices[0].message.content
    if not expanded_queries_raw or expanded_queries_raw.strip() == "":
      raise ValueError("API returned an empty response")
    expanded_queries_raw = re.search(r'```json\n({.*?})\n```', expanded_queries_raw, re.DOTALL)
    if expanded_queries_raw:
      expanded_queries_raw = expanded_queries_raw.group(1)
    else:
      expanded_queries_raw = expanded_queries_raw.strip()  # fallback to raw response
      
    #print(expanded_queries_raw)
    expanded_queries=json.loads(expanded_queries_raw)
    return expanded_queries


#weight the different output types
def assign_weights(term_type):
    weights = {
        "synonym": 0.8,
        "misspelling": 0.3,
        "technical": 0.7,
        "translation": 0.6
    }
    return weights.get(term_type, 0.5)  #default weight

def return_weighted_dict(expanded_queries, include_translations):
    weighted_terms = [
    {"term": expanded_queries["original_query"], "weight": 1.0}  # Original query (highest priority)
    ]

    if include_translations:
      for item in expanded_queries["expanded_terms"]:
          weighted_terms.append({
              "term": item["term"],
              "weight": assign_weights(item["type"])
          })
    else:
       for item in expanded_queries["expanded_terms"]:
          if item["type"]!="translation":
            weighted_terms.append({
                "term": item["term"],
                "weight": assign_weights(item["type"])
            })
    return weighted_terms


#full pipeline to be called by other fns
def expand(input_query, env_path, include_translations=True):
   expanded_list=get_expanded_queries(input_query, env_path)
   expanded_queries=return_weighted_dict(expanded_list, include_translations)

   return expanded_queries

