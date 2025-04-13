from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import re

def get_openai_client():
    REMOVED_SECRETREMOVED_SECRETREMOVED_SECRETInitialize and return an OpenAI client with the appropriate configuration.REMOVED_SECRETREMOVED_SECRETREMOVED_SECRET
    # Load API key from environment
    load_dotenv(dotenv_path='../.env')
    api_key = os.getenv('deepseek_API_KEY')
    
    # Initialize and return client
    return OpenAI(api_key=api_key, base_url=REMOVED_SECREThttps://openrouter.ai/api/v1REMOVED_SECRET)

def get_expanded_queries(user_query):
    # Initialize client
    client = get_openai_client()
    
    prompt=f'''You are an expert search query optimizer. Your task is to expand the following e-commerce search query to improve retrieval of relevant products. Generate a list of semantically related terms, synonyms, and common user variations while preserving the original intent.

**Rules:**
1. Prioritize **contextual relevance** (e.g., REMOVED_SECRETrunning shoesREMOVED_SECRET → REMOVED_SECRETjogging sneakersREMOVED_SECRET).
2. Include **common misspellings** (e.g., REMOVED_SECRETearbudsREMOVED_SECRET → REMOVED_SECRETairbudsREMOVED_SECRET).
3. Add **technical/layman variants** (e.g., REMOVED_SECRET4K TVREMOVED_SECRET → REMOVED_SECRETultra HD televisionREMOVED_SECRET).
4. For non-English queries, provide **translations/transliterations** if applicable (e.g., REMOVED_SECRETスマホREMOVED_SECRET → REMOVED_SECRETsmartphoneREMOVED_SECRET).
5. Output in JSON format for easy parsing.

**Input Query:** REMOVED_SECRET{user_query}REMOVED_SECRET

**Output Format:**  
{{
  REMOVED_SECREToriginal_queryREMOVED_SECRET: REMOVED_SECRET...REMOVED_SECRET,
  REMOVED_SECRETexpanded_termsREMOVED_SECRET: [
    {{REMOVED_SECRETtermREMOVED_SECRET: REMOVED_SECRET...REMOVED_SECRET, REMOVED_SECRETtypeREMOVED_SECRET: REMOVED_SECRETsynonymREMOVED_SECRET}},
    {{REMOVED_SECRETtermREMOVED_SECRET: REMOVED_SECRET...REMOVED_SECRET, REMOVED_SECRETtypeREMOVED_SECRET: REMOVED_SECRETmisspellingREMOVED_SECRET}},
    {{REMOVED_SECRETtermREMOVED_SECRET: REMOVED_SECRET...REMOVED_SECRET, REMOVED_SECRETtypeREMOVED_SECRET: REMOVED_SECRETtechnicalREMOVED_SECRET}}
  ]
}}

**Example Output for REMOVED_SECRETwireless headphonesREMOVED_SECRET:**
{{
  REMOVED_SECREToriginal_queryREMOVED_SECRET: REMOVED_SECRETwireless headphonesREMOVED_SECRET,
  REMOVED_SECRETexpanded_termsREMOVED_SECRET: [
    {{REMOVED_SECRETtermREMOVED_SECRET: REMOVED_SECRETBluetooth headphonesREMOVED_SECRET, REMOVED_SECRETtypeREMOVED_SECRET: REMOVED_SECRETsynonymREMOVED_SECRET}},
    {{REMOVED_SECRETtermREMOVED_SECRET: REMOVED_SECRETcordless earphonesREMOVED_SECRET, REMOVED_SECRETtypeREMOVED_SECRET: REMOVED_SECRETsynonymREMOVED_SECRET}},
    {{REMOVED_SECRETtermREMOVED_SECRET: REMOVED_SECRETwireless headsetsREMOVED_SECRET, REMOVED_SECRETtypeREMOVED_SECRET: REMOVED_SECRETsynonymREMOVED_SECRET}},
    {{REMOVED_SECRETtermREMOVED_SECRET: REMOVED_SECRETairbudsREMOVED_SECRET, REMOVED_SECRETtypeREMOVED_SECRET: REMOVED_SECRETmisspellingREMOVED_SECRET}},
    {{REMOVED_SECRETtermREMOVED_SECRET: REMOVED_SECRETnoise-cancelling headphonesREMOVED_SECRET, REMOVED_SECRETtypeREMOVED_SECRET: REMOVED_SECRETtechnicalREMOVED_SECRET}}
  ]
}}

**Now process this query:** REMOVED_SECRET{user_query}REMOVED_SECRET'''
    response = client.chat.completions.create(
        model=REMOVED_SECRETdeepseek/deepseek-chat-v3-0324:freeREMOVED_SECRET,
        messages=[
            {REMOVED_SECRETroleREMOVED_SECRET: REMOVED_SECRETuserREMOVED_SECRET, REMOVED_SECRETcontentREMOVED_SECRET: prompt},
        ],
        temperature=0.3,
    )
    
    expanded_queries_raw=response.choices[0].message.content
    if not expanded_queries_raw or expanded_queries_raw.strip() == REMOVED_SECRETREMOVED_SECRET:
      raise ValueError(REMOVED_SECRETAPI returned an empty responseREMOVED_SECRET)
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
        REMOVED_SECRETsynonymREMOVED_SECRET: 0.8,
        REMOVED_SECRETmisspellingREMOVED_SECRET: 0.3,
        REMOVED_SECRETtechnicalREMOVED_SECRET: 0.7,
        REMOVED_SECRETtranslationREMOVED_SECRET: 0.6
    }
    return weights.get(term_type, 0.5)  #default weight

def return_weighted_dict(expanded_queries):
    weighted_terms = [
    {REMOVED_SECRETtermREMOVED_SECRET: expanded_queries[REMOVED_SECREToriginal_queryREMOVED_SECRET], REMOVED_SECRETweightREMOVED_SECRET: 1.0}  # Original query (highest priority)
    ]

    for item in expanded_queries[REMOVED_SECRETexpanded_termsREMOVED_SECRET]:
        weighted_terms.append({
            REMOVED_SECRETtermREMOVED_SECRET: item[REMOVED_SECRETtermREMOVED_SECRET],
            REMOVED_SECRETweightREMOVED_SECRET: assign_weights(item[REMOVED_SECRETtypeREMOVED_SECRET])
        })
    return weighted_terms


#full pipeline to be called by other fns
def expand(input_query):
   expanded_list=get_expanded_queries(input_query)
   expanded_queries=return_weighted_dict(expanded_list)
   return expanded_queries
