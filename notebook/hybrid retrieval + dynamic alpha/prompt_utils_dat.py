from dotenv import load_dotenv
import os
import json
import re
from openai import OpenAI

# Load API key from .env file
load_dotenv(dotenv_path='../.env')
api_key = os.getenv('deepseek_API_KEY')

# Initialize OpenAI client with loaded key
client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")

def get_dynamic_alpha(question, dense_result, bm25_result):
    system_prompt = """You are a multilingual evaluator in an Italian e-commerce site assessing the retrieval effectiveness of dense
retrieval (Cosine Distance) and BM25 retrieval for finding the correct Italian product title given an English-language query.

## Task:
Given a query and two top-1 search results (one from dense retrieval, one from BM25 retrieval), score each method from **0 to 5** based on how likely the correct result is retrieved or nearby.

### Scoring Criteria:
1. **Direct hit → 5 points**
   - If the retrieved result directly answers the question.
2. **Good wrong result → 3-4 points**
   - Answer is not exact, but closely related; likely the correct one is nearby.
3. **Bad wrong result → 1-2 points**
   - Loosely related or general, unlikely correct answer is nearby.
4. **Completely off-track → 0 points**
   - Retrieval is unrelated.

### Output Format:
Return two integers separated by a space:
- First number: dense retrieval score.
- Second number: BM25 retrieval score.
"""

    user_prompt = f"""### Given Data:
- Question: "{question}"
- dense retrieval Top1 Result: "{dense_result}"
- BM25 retrieval Top1 Result: "{bm25_result}"
"""

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324:free",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0
    )

    output = response.choices[0].message.content.strip()

    try:
        dense_score, bm25_score = map(int, output.split())
    except:
        dense_score = bm25_score = 3  # fallback if parsing fails

    if dense_score == 5 and bm25_score != 5:
        return 1.0
    elif bm25_score == 5 and dense_score != 5:
        return 0.0
    elif dense_score == 0 and bm25_score == 0:
        return 0.5
    else:
        return dense_score / (dense_score + bm25_score)


