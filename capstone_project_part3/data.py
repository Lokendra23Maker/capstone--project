
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

#load dataset 
df = pd.read_csv("womens clothing E-commerce Reviews.csv")
print("Rows and columns:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())

print("\nMissing Values:")
print(df.isnull().sum())

# promt Engineering
 # TASK 1 - Zero -shot promat
zero_shot_promt = """"
Analyze the following customer review and classify its overall sentiment

The sentiment must be one of:postive, negative, neutral.
Return the result onlyi in this JSON
fromat:
{ 
   "lebel": "postive/ negative/ neutral",
   "confidance": "low/medium/high",
   "reason": "string"
}
 customer Review:
 {review_text}
 """

 # Task 1 _ few shot promt
few_shot_promt = """
 Analyze the customer review and classify its  overall sentiment.
 The sentiment must be one of:
 postive, negative,neutral.

 Use the following examples as guidance.
  Example 1 :
  Review: " I absolutely love this dress. The quality is excellent,"
 output:
 { 
        "lebel": "postive",
        "confidance": "high",
        "reason": " the customer expresses strong satisfaction with the product quality."
}
 Example 2 :
 Review : " the product  arrived damaged and look  very cheap."
 output : 
{        
        "lebel" : "negative"
        "confidance": high",
        "reson": the customer is dissatisfied because the product arrived damged and had poor quality."

}

Example  3 :
 Review  : " THE DRESS IS  OKAY , NOTHING SPECAIL."
 Output : 
 {     "lebel": "neutral",
       "confidance": medium",
       "reason": the customer gives a neutral opanion without strong positive or negative emotion."
}

Return the result only in this JSON
fromat:
{ 
   "lebel": "postive/ negative/ neutral",
   "confidance": "low/medium/high",
   "reason": "string"
}
 customer Review:
 {review_text}

 """
# Task 1 - Role-Prompted Prompt

role_prompted_prompt = """
Role:
Act as a senior customer-insights analyst specializing in e-commerce reviews.

Instruction:
Analyze the following customer review and classify its overall sentiment.

Context:
The review is from a Women's Clothing E-Commerce customer.
Consider the customer's overall opinion about the product, quality, fit,
comfort, delivery, or shopping experience.

Constraints:
- The sentiment must be exactly one of: positive, negative, neutral.
- Assign confidence as exactly one of: low, medium, high.
- Give a short reason based only on the review.
- Do not invent information.
- Return only valid JSON.
- Do not add any text outside the JSON.

Output:
{
    "label": "positive/negative/neutral",
    "confidence": "low/medium/high",
    "reason": "string"
}

Customer Review:
{review_text}
print(role_prompt)
"""
# TASK 2 - Reusable LLM API Wrapper

import os
from google import genai
from google.genai import types

# Create Gemini client using environment variable
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def call_llm(prompt, temperature, max_tokens):
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_tokens
        )
    )

    return response.text

test_response = call_llm(
    "Say hello in one short sentence.",
    0.2,
    50
)

print("LLM Response:")
print(test_response)

# TASK 3 - Retry-on-Failure Handling

import logging
import time

logging.basicConfig(level=logging.INFO)

def call_llm_with_retry(prompt, temperature, max_tokens):
    max_retries = 3

    for attempt in range(max_retries + 1):
        try:
            return call_llm(prompt, temperature, max_tokens)

        except Exception as e:
            if attempt < max_retries:
                logging.warning(
                    f"LLM call failed (attempt {attempt + 1}). "
                    f"Retrying... Error: {e}"
                )
                time.sleep(1)
            else:
                logging.error(
                    f"LLM call failed after {max_retries} retries. "
                    f"Moving on. Error: {e}"
                )
                return None
test_retry = call_llm_with_retry(
    "Say hello in one short sentence.",
    0.2,
    50
)

print("Retry Test Response:")
print(test_retry)

# Task 4 — Three-Template Comparison
import json

records = df.head(5)

templates = {
    "zero_shot": zero_shot_promt,
    "few_shot": few_shot_promt,
    "role_prompted": role_prompted_prompt
}

results = []

for name, template in templates.items():
    for i, row in records.iterrows():

        prompt = template.replace(
            "{review}",
            str(row["Review Text"])
        )

        response = call_llm_with_retry(
            prompt,
            0.2,
            200
        )

        try:
            text = str(response).strip()

            if "" in text:
                text = text.replace("json", "").replace("```", "").strip()

            start = text.find("{")
            end = text.rfind("}") + 1

            data = json.loads(text[start:end])

            valid = all(
                k in data
                for k in ["label", "confidence", "reason"]
            )

        except Exception:
            valid = False

        results.append({
            "template": name,
            "record": i,
            "valid_json": valid
        })

        if not valid:
            logging.error(
                f"Failed: {name}, record {i}"
            )

print("Task 4 completed:", len(results), "calls")

for name in templates:
    valid_count = sum(
        r["valid_json"]
        for r in results
        if r["template"] == name
    )
    print(name, ":", valid_count, "/ 5 valid")


    # Task 5 — Aspect-Based Sentiment Extension

import json

records_10 = df.head(10)

best_template = role_prompted_prompt

task5_results = []

for i, row in records_10.iterrows():

    prompt = best_template.replace(
        "{review}",
        str(row["Review Text"])
    )

    prompt += """
    
Return ONLY valid JSON in this format:
{
  "aspects": [
    {
      "aspect": "string",
      "sentiment": "positive|negative|neutral",
      "actionable_phrase": "3-6 words"
    },
    {
      "aspect": "string",
      "sentiment": "positive|negative|neutral",
      "actionable_phrase": "3-6 words"
    }
  ]
}

Identify at least two relevant aspects from the review.
"""

    response = call_llm_with_retry(prompt, 0.2, 200)

    try:
        data = json.loads(response)
        valid = "aspects" in data and len(data["aspects"]) >= 2
    except Exception:
        data = None
        valid = False

    task5_results.append({
        "record": int(i),
        "result": data,
        "valid_json": valid
    })

    if not valid:
        logging.error(f"Task 5 failed: record {i}")

print("Task 5 completed:", len(task5_results), "records")

for r in task5_results:
    print(r)

    #  Task 6 — Response-Drafting Chain

autodrafted_replies = []

for r in task5_results[:3]:
    if not r["valid_json"]:
        continue

    prompt = f"""
You are a professional customer-support representative.

Based on this structured sentiment analysis:
{json.dumps(r["result"])}

Write a short, professional and empathetic reply that directly
addresses the specific issues raised in the review.

Return only the reply text.
"""

    reply = call_llm_with_retry(prompt, 0.2, 150)

    autodrafted_replies.append({
        "record": r["record"],
        "reply": reply
    })

print("Task 6 completed:", len(autodrafted_replies), "replies")

for r in autodrafted_replies:
    print("\nRecord:", r["record"])
    print("Reply:", r["reply"])

    #  Task 7 — Multi-Turn Context
history = [
    {"role": "user", "content": "My name is lucky and I like blue."},
    {"role": "assistant", "content": "Nice to meet you, lucky!"},
    {"role": "user", "content": "What is my name and favorite color?"}
]

prompt = f"""
Use this conversation history to answer the last question.

Conversation history:
{json.dumps(history)}

Answer using the information from the first turn.
"""

response = call_llm_with_retry(prompt, 0.2, 100)

print("Task 7 Response:")
print(response)

print("\nConversation History:")
print(json.dumps(history, indent=2))