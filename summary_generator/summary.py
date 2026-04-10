
from dotenv import load_dotenv
from prompts.system_prompts import SUMMARY_GENERATOR_PROMPT
import requests
import json
import os

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def summary_generator(retrieved_memories):
    messages = [
        {"role": "system", "content": SUMMARY_GENERATOR_PROMPT}
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

        reply = data["choices"][0]["message"]["content"]

        return reply

    except Exception as e:
        print("Error:", str(e))
        return "Something went wrong. Please try again."
