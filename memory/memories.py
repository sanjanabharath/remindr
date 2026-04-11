import json
import requests
from vector_db.vector_db import add_to_memory, delete_memory, relevant_memories, update_memory
from dotenv import load_dotenv
import os

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def brain(new_memeory, relevant_memory):
    messages = [
        {"role": "system", "content": "You are an AI brain that decides whether a new memory needs an addition or updation or deletion to the existing memory. Decide based on the relevance and importance of the new memory compared to the existing memory. Answer with 'add', 'update', or 'delete' or 'none'. Here are the details of the new memory and the relevant memory: {new_memory} and {relevant_memory}".format(new_memory=new_memeory, relevant_memory=relevant_memory)},
    ]

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "model": "nvidia/nemotron-3-super-120b-a12b:free",
                "messages": messages
            })
        )

        data = response.json()

        decision = data["choices"][0]["message"]["content"]

        return decision
    except Exception as e:
        print(f"Error while decoding response: {e}")
        return None

def update_phase(new_memory, collection):
    # Get relevant memories based on the new memory
    relevant = relevant_memories(collection, new_memory, s=5)

    for mem in relevant_memories:
        decision = brain(new_memory, mem)

        if decision == "add":
            add_to_memory(collection, new_memory)
        elif decision == "update":
            update_memory(collection, mem["id"], new_memory)
        elif decision == "delete":
            delete_memory(collection, mem["id"])
        elif decision == "none":
            continue
        else:
            print(f"Unexpected decision: {decision}")

