from dotenv import load_dotenv
import os
import json
import re
from openai import OpenAI

# Load API key from .env file
load_dotenv(dotenv_path='../.env')
api_key = os.getenv('deepseek_API_KEY')

# Initialize OpenAI client with loaded key
client = OpenAI(api_key=api_key, base_url=REMOVED_SECREThttps://openrouter.ai/api/v1REMOVED_SECRET)

def get_dynamic_alpha(question, dense_result, bm25_result):
    prompt = fREMOVED_SECRETREMOVED_SECRETREMOVED_SECRETYou are a multilingual evaluator in a italian ecommerce site assessing the retrieval effectiveness of dense
retrieval (Cosine Distance) and BM25 retrieval for finding the correct italian product title with respect to the english query.

## Task:
Given a question and two top1 search results (one from dense retrieval,
one from BM25 retrieval), score each retrieval method from **0 to 5** based on whether the correct answer is likely to appear in top2, top3, etc.

### **Scoring Criteria:**
1. **Direct hit --> 5 points**
- If the retrieved document directly answers the question, assign **5 points**.
2. **Good wrong result (High likelihood correct answer is nearby) --> 3-4 points**
3. **Bad wrong result (Low likelihood correct answer is nearby) --> 1-2 points**
4. **Completely off-track --> 0 points**

### **Given Data:**
- **Question:** REMOVED_SECRET{question}REMOVED_SECRET

- **dense retrieval Top1 Result:** REMOVED_SECRET{dense_result}REMOVED_SECRET
- **BM25 retrieval Top1 Result:** REMOVED_SECRET{bm25_result}REMOVED_SECRET

### **Output Format:**
Return two integers separated by a space:
- **First number:** dense retrieval score.
- **Second number:** BM25 retrieval score.
REMOVED_SECRETREMOVED_SECRETREMOVED_SECRET

    response = client.chat.completions.create(
        model=REMOVED_SECRETdeepseek/deepseek-chat-v3-0324:freeREMOVED_SECRET,  
        messages=[{REMOVED_SECRETroleREMOVED_SECRET: REMOVED_SECRETuserREMOVED_SECRET, REMOVED_SECRETcontentREMOVED_SECRET: prompt}],
        temperature=0
    )

    output = response.choices[0].message.content.strip()

    try:
        dense_score, bm25_score = map(int, output.split())
    except:
        dense_score = bm25_score = 3  # default fallback

    if dense_score == 5 and bm25_score != 5:
        return 1.0
    elif bm25_score == 5 and dense_score != 5:
        return 0.0
    elif dense_score == 0 and bm25_score == 0:
        return 0.5
    else:
        return dense_score / (dense_score + bm25_score)

