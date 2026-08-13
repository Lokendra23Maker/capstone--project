# LangChain Single Autonomous Agent — Option A

A tool-calling LangChain agent (Gemini 3.1-Flash-lite) with bounded iterations, 2-turn
conversation memory, and a separate RunnablePassthrough / RunnableBranch
conditional workflow.

Run with:

bash
pip install -r requirements.txt   # langchain, langchain-core, langchain-google-genai, python-dotenv
# add GOOGLE_API_KEY=... to a .env file
python agent_option_a.py


---

## 1. Tool contract table

| Name | Description | Parameters | Read / Write |
|---|---|---|---|
| get_random_advice | Fetches one random piece of advice from the public, keyless api.adviceslip.com API. Returns the advice as a string, or an error string if the API call fails or returns an unexpected shape. | none | *Read* — GET request only, no state changed |
| get_order_count | Counts orders in a local, in-memory mock order list, optionally filtered by status. Returns an error string (not an exception) for an unrecognized status. | status: str — one of all, completed, pending, cancelled (default all) | *Read* — reads a hardcoded local list, no external calls, no state changed |

No write tools are used in this submission, so no write-safeguard is needed.

---

## 2. How tool-selection is communicated as a {tool, arguments} contract

This agent is built with create_tool_calling_agent + AgentExecutor from
LangChain, *not* a hand-rolled text parser. When the model decides to call a
tool, LangChain's own tool-calling machinery resolves that decision into a
structured AgentAction object with a .tool (string name) and
.tool_input (parsed dict of arguments) attribute — this is native to the
framework, generated from the model's function-calling output, not scraped
from raw text.

AgentExecutor is run with return_intermediate_steps=True, so every
(action, observation) pair is available on result["intermediate_steps"]
after each .invoke() call. run_query() extracts each action.tool /
action.tool_input pair, builds it into a real JSON object

json
{"tool": "...", "arguments": {...}}


via json.dumps(...), and prints/returns it. That is the structured,
inspectable log referenced below — it comes directly from LangChain's
internal representation of the routing decision, not from parsing the
agent's natural-language output.

---

## 3. Memory demo (2 turns)

*Turn 1*

- Query: "My preferred language is Hindi."
- Tool calls: none expected (no tool is needed to store a stated preference in
  conversation memory).
- Final answer:
  
  <PASTE the actual printed "FINAL ANSWER" text from your run here>
  

*Turn 2*

- Query: "What is my preferred language?"
- Tool calls: none expected.
- Final answer:
  
  <PASTE the actual printed "FINAL ANSWER" text from your run here>
  
  This should state "Hindi" *without the user repeating it*, because
  ConversationBufferMemory (memory_key="chat_history") carried turn 1's
  human/AI messages into turn 2's prompt via the {chat_history} placeholder.

---

## 4. Tool-use demonstration (3 distinct queries)

### Query 1 — "Give me one random piece of advice."

Logged tool call (captured from intermediate_steps):

json
<PASTE the printed {"tool": "get_random_advice", "arguments": {}} block here>


Final answer:

<PASTE final answer text here>


### Query 2 — "How many orders are there in total?"

Logged tool call:

json
<PASTE the printed {"tool": "get_order_count", "arguments": {"status": "all"}} block here>


Final answer:

<PASTE final answer text here>


### Query 3 — "How many completed orders are there?"

Logged tool call:

json
<PASTE the printed {"tool": "get_order_count", "arguments": {"status": "completed"}} block here>


Final answer:

<PASTE final answer text here>


---

## 5. Conditional workflow (RunnablePassthrough + RunnableBranch)

A workflow separate from the main agent loop:

- state_step_1 = RunnablePassthrough.assign(word_count=...) — accumulates a
  word_count field onto the input dict.
- state_step_2 = state_step_1.assign(category=...) — chains a second step
  that classifies word_count >= 6 as "long", else "short".
- RunnableBranch routes to long_chain or short_chain based on
  category.

*Run 1 — triggers the SHORT branch*

- Input: {"input": "Give advice"}  (2 words → word_count=2 → category="short")
- Output:
  
  <PASTE the printed short_result dict here, e.g. {'route': 'SHORT', 'message': 'Short query route selected.'}>
  

*Run 2 — triggers the LONG branch*

- Input: {"input": "Please give me some useful advice for learning Python"}
  (8 words → word_count=8 → category="long")
- Output:
  
  <PASTE the printed long_result dict here, e.g. {'route': 'LONG', 'message': 'Long query route selected.'}>
  

Both branches are demonstrated by invoking the same conditional_workflow
twice with inputs chosen to cross the 6-word threshold in opposite
directions.

---

## 6. Design notes / good-tool properties

- *Clear name* — get_random_advice, get_order_count describe exactly
  what each does.
- *Honest/accurate description* — docstrings state read-only behavior and
  parameters; these docstrings are what the model reads to decide when to
  call each tool.
- *Atomic* — each tool does exactly one job (fetch one piece of advice;
  count orders).
- *Safe* — network/parsing failures in get_random_advice and an
  unrecognized status in get_order_count are caught and returned as
  plain-string data, never raised as exceptions that would crash the agent
  loop.
- *Bounded loop* — AgentExecutor(max_iterations=5) prevents runaway
  tool-calling.

## 7. Environment variables

| Variable | Purpose |
|---|---|
| GOOGLE_API_KEY | Required by langchain_google_genai.ChatGoogleGenerativeAI to call the Gemini API. Set it in a local .env file — never commit it. |

No API key appears anywhere in this repository.