

from prompts.system_prompts import SUMMARY_GENERATOR_PROMPT
import requests
import json
OPENROUTER_API_KEY = "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"
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
