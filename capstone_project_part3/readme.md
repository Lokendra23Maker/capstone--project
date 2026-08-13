# GenAI-Powered Text Analytics — Part 3

## Prompt Engineering & LLM API Integration

**Project:** Customer Feedback / E-commerce Review Analysis

**Dataset:** `womens clothing E-commerce Reviews.csv`

**LLM:** Google Gemini

**API environment variable:** `GEMINI_API_KEY`

---

## 📌 Project Overview

This project builds an end-to-end GenAI pipeline for analysing customer
feedback using prompt engineering and an LLM API.

The implementation compares three prompting strategies, adds
retry-on-failure handling, evaluates structured JSON outputs, extends
the best-performing approach for aspect-based sentiment analysis,
generates response drafts, and demonstrates multi-turn conversation
context.

### Main goals

- Classify customer feedback using structured JSON.
- Compare **Zero-shot**, **Few-shot**, and **Role-prompted**
strategies.
- Integrate Google Gemini through a reusable Python wrapper.
- Handle API failures without crashing the complete run.
- Extract aspect-level sentiment and actionable phrases.
- Generate professional, empathetic customer responses.
- Demonstrate multi-turn context.
- Keep the API key outside the source code.

---

# 🧩 Tasks Completed

## Task 1 — Prompt Engineering

Three separate prompt templates are defined:

### 1. Zero-shot

Uses a direct instruction without worked examples.

### 2. Few-shot

Uses the same classification instruction together with worked examples.

### 3. Role-prompted

Assigns the model a clear professional persona and follows the Three Cs:

- **Clarity**
- **Context**
- **Constraints**

All templates request the same locked JSON structure.

### Locked JSON schema

```json
{
  "label": "positive|negative|neutral",
  "confidence": "low|medium|high",
  "reason": "string"
}
```

---

# 🔌 Task 2 — Reusable LLM API Wrapper

A reusable function is used for model calls:

```python
call_llm(prompt, temperature, max_tokens)
```

The API key is loaded from the environment rather than being hardcoded.

Example:

```python
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
```

The wrapper accepts:

- `prompt`
- `temperature`
- `max_tokens`

and returns the model’s text response.

---

# 🔁 Task 3 — Retry-on-Failure

The LLM call is protected with retry logic.

If an API/network/rate-limit failure occurs, the code retries the
request before logging the failure and continuing with the remaining
records.

This prevents one failed request from terminating the complete analysis
pipeline.

---

# 📊 Task 4 — Three-Template Comparison

The three templates are applied to the same five real records:

| Template | Records | Calls |
| --- | --- | --- |
| Zero-shot | 5 | 5 |
| Few-shot | 5 | 5 |
| Role-prompted | 5 | 5 |
| **Total** | **15** | **15** |

Every response is attempted as JSON and marked as valid/invalid.

### Validation approach

```python
json.loads(response)
```

If parsing fails, the corresponding template/record is logged instead of
crashing the entire run.

> **Run note:** During development, the Gemini free-tier request quota
was exhausted. The code therefore records failed calls safely rather
than terminating the program. The final reliability statement should
be based on the successful 15-call run used for submission.
> 

---

# 🎯 Task 5 — Aspect-Based Sentiment Extension

The best-performing prompt is extended to analyse multiple relevant
aspects of each review.

For every selected record, the structured output contains:

1. Sentiment for at least two relevant aspects.
2. A short actionable phrase of approximately 3–6 words describing
what was liked or disliked.

### Example output structure

```json
{
  "aspects": [
    {
      "aspect": "fit",
      "sentiment": "positive",
      "actionable_phrase": "comfortable and flattering fit"
    },
    {
      "aspect": "quality",
      "sentiment": "negative",
      "actionable_phrase": "fabric feels too thin"
    }
  ]
}
```

The resulting 10-record analysis is intended to be presented in the
README as a compact table.

---

# 💬 Task 6 — Response-Drafting Chain

The structured output from Task 5 is passed into a second prompt.

The second prompt generates a short, professional and empathetic reply
that addresses the **specific issues mentioned in the source record**,
rather than producing a generic response.

### Pipeline

```
Customer Review
      ↓
Aspect-Based Sentiment JSON
      ↓
Response-Drafting Prompt
      ↓
Professional Customer Reply
```

At least three generated replies should be shown next to their source
records in the final results section.

---

# 🗣️ Task 7 — Multi-Turn Context

A two-turn conversation is demonstrated.

### Turn 1

The user provides personal information:

```
My name is Lucky and I like blue.
```

### Turn 2

The user asks:

```
What is my name and favorite color?
```

The conversation history is retained as a list of role/content messages
so that the second request can use information supplied in the first
turn.

### Conversation structure

```json
[
  {
    "role": "user",
    "content": "My name is Lucky and I like blue."
  },
  {
    "role": "assistant",
    "content": "Nice to meet you, Lucky!"
  },
  {
    "role": "user",
    "content": "What is my name and favorite color?"
  }
]
```

---

# 🔐 Task 8 — API Key Security

The Gemini API key is stored in a local `.env` file.

### `.env`

```
GEMINI_API_KEY=YOUR_API_KEY
```

The `.env` file is excluded from Git using `.gitignore`:

```
.env
```

The API key must **never** be committed to the repository or hardcoded
in `data.py`.

---

# 🧪 Validation & Error Handling

The pipeline is designed to:

- validate JSON responses,
- record failed template/record combinations,
- retry temporary API failures,
- continue after unsuccessful requests,
- keep credentials outside source code,
- preserve multi-turn message history.

This makes the pipeline more robust than a single direct LLM call.

---

# 📈 Results Summary

| Component | Status |
| --- | --- |
| Three prompt templates | Implemented |
| Reusable Gemini wrapper | Implemented |
| Environment-variable API key | Implemented |
| Retry handling | Implemented |
| 15-call template comparison | Implemented |
| JSON validation | Implemented |
| Aspect-based sentiment | Implemented |
| Response-drafting chain | Implemented |
| Multi-turn context | Demonstrated |
| `.env` excluded from Git | Implemented |

---

# 📁 Project Structure

```
capstone_project_part3/
│
├── data.py
├── README.md
├── .env
├── .gitignore
└── womens clothing E-commerce Reviews.csv
```

> `.env` contains the local API key and must remain untracked.
> 

---

# ▶️ How to Run

Install the required packages:

```bash
pip install -U google-genai python-dotenv pandas
```

Then make sure `.env` contains:

```
GEMINI_API_KEY=YOUR_API_KEY
```

Run:

```bash
python data.py
```

---

# 📝 Final Submission Checklist

- [x]  Three distinct prompting strategies.
- [x]  Locked JSON schema.
- [x]  Reusable `call_llm()` wrapper.
- [x]  Environment-variable API key.
- [x]  Retry-on-failure path.
- [x]  JSON validation and failure logging.
- [x]  Multi-turn conversation history.
- [x]  `.env` excluded through `.gitignore`.
- [ ]  Final 15-call reliability table populated from the successful
run.
- [ ]  Final 10-record aspect-sentiment table populated with real model
outputs.
- [ ]  At least 3 final auto-drafted replies shown with their source
records.

---

## ⭐ Conclusion

This project demonstrates a complete GenAI text-analysis workflow, from
raw customer feedback to structured insights and response generation.
The design emphasizes **prompt quality, reusable API integration,
structured outputs, error resilience, security, and conversational
context**.

The final results should be populated with the actual successful model
outputs produced during the submission run.