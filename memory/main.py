import json
import requests
from typing import TypedDict, List, Optional
from difflib import SequenceMatcher

from langgraph.graph import StateGraph, END


# ---------------------------
# 🔐 CONFIG
# ---------------------------
OPENROUTER_API_KEY = "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"


# ---------------------------
# 🧠 STATE
# ---------------------------
class MemoryState(TypedDict):
    new_input: str
    existing_memory: List[str]
    matched_memory: Optional[str]
    similarity: float
    decision: str


# ---------------------------
# 🤖 OPENROUTER LLM FUNCTION
# ---------------------------
def call_llm(messages):
    url = "https://openrouter.ai/api/v1/chat/completions"

    response = requests.post(
        url=url,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        data=json.dumps({
            "model": "nvidia/nemotron-3-super-120b-a12b:free",
            "messages": messages
        })
    )

    result = response.json()

    return result["choices"][0]["message"]["content"]


# ---------------------------
# 🔍 FIND BEST MATCH
# ---------------------------
def find_best_match(state: MemoryState):
    new_input = state["new_input"]
    memories = state["existing_memory"]

    best_score = 0
    best_match = None

    for mem in memories:
        score = SequenceMatcher(None, new_input, mem).ratio()
        if score > best_score:
            best_score = score
            best_match = mem

    state["matched_memory"] = best_match
    state["similarity"] = best_score

    print("\n[COMPARE]")
    print("New Input:", new_input)
    print("Best Match:", best_match)
    print("Similarity:", round(best_score, 2))

    return state


# ---------------------------
# 🤖 DECISION NODE (LLM)
# ---------------------------
def decide_action(state: MemoryState):
    messages = [
        {
            "role": "system",
            "content": "You are a strict memory management agent."
        },
        {
            "role": "user",
            "content": f"""
New Input:
{state['new_input']}

Closest Existing Memory:
{state['matched_memory']}

Similarity Score:
{state['similarity']}

Rules:
- If completely new → ADD
- If similar but improved → UPDATE
- If contradicts → DELETE
- If same → NOOP

Respond ONLY with one word:
ADD / UPDATE / DELETE / NOOP
"""
        }
    ]

    response = call_llm(messages)

    decision = response.strip().lower()

    # Safety fallback
    if decision not in ["add", "update", "delete", "noop"]:
        decision = "noop"

    state["decision"] = decision

    print("\n[DECISION] →", decision.upper())

    return state


# ---------------------------
# 🔀 ROUTER
# ---------------------------
def route_decision(state: MemoryState):
    return state["decision"]


# ---------------------------
# 🛠 ACTIONS
# ---------------------------
def add_memory(state: MemoryState):
    print("[ACTION] ADD")
    state["existing_memory"].append(state["new_input"])
    return state


def update_memory(state: MemoryState):
    print("[ACTION] UPDATE")

    updated = []
    for mem in state["existing_memory"]:
        if mem == state["matched_memory"]:
            updated.append(state["new_input"])
        else:
            updated.append(mem)

    state["existing_memory"] = updated
    return state


def delete_memory(state: MemoryState):
    print("[ACTION] DELETE")

    state["existing_memory"] = [
        m for m in state["existing_memory"]
        if m != state["matched_memory"]
    ]

    return state


def noop(state: MemoryState):
    print("[ACTION] NOOP")
    return state


# ---------------------------
# 🧱 BUILD GRAPH
# ---------------------------
builder = StateGraph(MemoryState)

builder.add_node("compare", find_best_match)
builder.add_node("decide", decide_action)

builder.add_node("add", add_memory)
builder.add_node("update", update_memory)
builder.add_node("delete", delete_memory)
builder.add_node("noop", noop)

builder.set_entry_point("compare")

builder.add_edge("compare", "decide")

builder.add_conditional_edges(
    "decide",
    route_decision,
    {
        "add": "add",
        "update": "update",
        "delete": "delete",
        "noop": "noop"
    }
)

builder.add_edge("add", END)
builder.add_edge("update", END)
builder.add_edge("delete", END)
builder.add_edge("noop", END)

graph = builder.compile()


# ---------------------------
# ▶️ RUN TEST
# ---------------------------
if __name__ == "__main__":
    state = {
        "new_input": "User likes cold coffee",
        "existing_memory": [
            "User likes coffee",
            "User is a student"
        ],
        "matched_memory": None,
        "similarity": 0.0,
        "decision": ""
    }

    result = graph.invoke(state)

    print("\n[FINAL MEMORY]")
    print(result["existing_memory"])