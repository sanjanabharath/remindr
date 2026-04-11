
from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def summary_generator(retrieved_memories):
    messages = [
        {"role": "system", "content": """You are a memory compression and summarization agent designed for long-term AI memory systems.

Your job is to transform the latest user memories into a compact, structured, and reusable summary that can be stored as long-term memory.

GOAL:
Convert the given memories into a high-signal summary that preserves only meaningful, durable, and evolving information about the user.

INPUT:
{retrieved_memories}

WHAT TO EXTRACT:
- Stable preferences (likes, dislikes, habits)
- Emotional patterns (stress, improvement, recurring feelings)
- Behavioral changes over time
- Important personal context (goals, routines, lifestyle)

WHAT TO REMOVE:
- Redundant or repeated information
- Temporary or low-value details
- One-off statements unless significant

CONFLICT HANDLING:
If memories conflict:
- Capture the transition clearly
- Example: "Previously X, but now Y"

INSTRUCTIONS:
1. Merge related memories into a coherent understanding.
2. Prioritize recent changes over older information.
3. Compress aggressively — keep only high-value insights.
4. Do NOT repeat similar points.
5. Do NOT hallucinate or invent new facts.
6. Keep it concise but information-dense.

STYLE:
- Neutral, factual, slightly empathetic
- Avoid fluff or storytelling
- Focus on clarity and usefulness for future AI reasoning

OUTPUT FORMAT (STRICT):

Return ONLY a structured summary in this format:

Summary:
<2–4 sentence compressed summary>

Key Insights:
- <insight 1>
- <insight 2>
- <insight 3 (optional)>

Do NOT include anything else.""".format(retrieved_memories=retrieved_memories)}
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
