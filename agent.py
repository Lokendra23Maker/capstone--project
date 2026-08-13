import os
import json
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableLambda,
    RunnableBranch,
)

# --- import fallback: some environments ship AgentExecutor / create_tool_calling_agent
# --- / ConversationBufferMemory under langchain_classic, others under classic langchain.
try:
    from langchain_classic.agents import create_tool_calling_agent
    from langchain_classic.agents.agent import AgentExecutor
    from langchain_classic.memory import ConversationBufferMemory
except ImportError:
    from langchain.agents import create_tool_calling_agent, AgentExecutor
    from langchain.memory import ConversationBufferMemory


load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise EnvironmentError(
        "GOOGLE_API_KEY is not set. Add it to your .env file "
        "(GOOGLE_API_KEY=your_key_here) before running this script."
    )


# ---------- TOOLS ----------

@tool
def get_random_advice() -> str:
    """Fetch one random piece of advice from the public api.adviceslip.com API.
    Read-only tool: makes a GET request, returns a short string of advice.
    Takes no arguments."""
    try:
        req = Request(
            "https://api.adviceslip.com/advice",
            headers={"User-Agent": "masai-agent-assignment"},
        )
        with urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
        return data["slip"]["advice"]
    except (URLError, HTTPError, TimeoutError) as e:
        # Safe: return the error as data instead of raising/crashing the agent.
        return f"API error while fetching advice: {e}"
    except (KeyError, json.JSONDecodeError) as e:
        return f"Unexpected advice API response format: {e}"


@tool
def get_order_count(status: str = "all") -> str:
    """Return a count of mock orders, optionally filtered by status
    ('all', 'completed', 'pending', or 'cancelled'). Read-only tool
    operating on local in-memory mock data, no external calls."""
    orders = [
        {"id": 1, "status": "completed"},
        {"id": 2, "status": "completed"},
        {"id": 3, "status": "pending"},
        {"id": 4, "status": "completed"},
        {"id": 5, "status": "cancelled"},
    ]

    valid_statuses = {"all", "completed", "pending", "cancelled"}
    status_norm = status.lower().strip()
    if status_norm not in valid_statuses:
        # Safe: known-bad input returns a data-shaped error, not an exception.
        return f"Unknown status '{status}'. Valid options: {sorted(valid_statuses)}"

    if status_norm == "all":
        return f"Total orders: {len(orders)}"

    count = sum(1 for order in orders if order["status"] == status_norm)
    return f"{status_norm.title()} orders: {count}"


tools = [get_random_advice, get_order_count]


# ---------- MODEL ----------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0,
)


# ---------- AGENT PROMPT ----------

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful assistant. Use the available tools when needed.",
    ),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])


# ---------- AGENT ----------

agent = create_tool_calling_agent(llm, tools, prompt)


# ---------- MEMORY ----------

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
)


# ---------- EXECUTOR ----------

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    max_iterations=5,
    verbose=True,
    return_intermediate_steps=True,
)


# ---------- TOOL-CALL LOGGER (requirement: structured {tool, arguments} log) ----------

def run_query(query):
    print("\n" + "=" * 60)
    print("USER:", query)

    result = agent_executor.invoke({"input": query})

    print("\nTOOL CALLS (structured, extracted from AgentExecutor.intermediate_steps):")
    logged_calls = []
    for action, observation in result["intermediate_steps"]:
        call_record = {
            "tool": action.tool,
            "arguments": action.tool_input,  # native structured dict, not regex-parsed
        }
        logged_calls.append(call_record)
        # Print as real JSON so it can be copy-pasted straight into the README.
        print(json.dumps(call_record, indent=2, default=str))
        print(f"  -> observation: {observation}")

    print("\nFINAL ANSWER:")
    print(result["output"])

    return {
        "query": query,
        "tool_calls": logged_calls,
        "final_answer": result["output"],
    }


# ---------- 2-TURN MEMORY DEMO ----------

print("\n\nMEMORY DEMO")

run_query("My preferred language is Hindi.")
run_query("What is my preferred language?")


# ---------- 3+ DISTINCT TOOL QUERIES (acceptance criteria requires >= 3) ----------

print("\n\nTOOL DEMONSTRATION")

run_query("Give me one random piece of advice.")
run_query("How many orders are there in total?")
run_query("How many completed orders are there?")


# ---------- CONDITIONAL WORKFLOW (RunnablePassthrough + RunnableBranch) ----------

def add_word_count(data):
    return len(data["input"].split())


def classify(data):
    return "long" if data["word_count"] >= 6 else "short"


state_step_1 = RunnablePassthrough.assign(
    word_count=RunnableLambda(add_word_count)
)

state_step_2 = state_step_1.assign(
    category=RunnableLambda(classify)
)

short_chain = RunnableLambda(
    lambda x: {"route": "SHORT", "message": "Short query route selected."}
)

long_chain = RunnableLambda(
    lambda x: {"route": "LONG", "message": "Long query route selected."}
)

conditional_workflow = state_step_2 | RunnableBranch(
    (lambda x: x["category"] == "long", long_chain),
    short_chain,
)


print("\n\nCONDITIONAL WORKFLOW")

# Invoke twice with inputs designed to trigger each branch, per acceptance criteria.
short_result = conditional_workflow.invoke({"input": "Give advice"})
print("SHORT branch input -> ", short_result)

long_result = conditional_workflow.invoke(
    {"input": "Please give me some useful advice for learning Python"}
)
print("LONG branch input -> ", long_result)