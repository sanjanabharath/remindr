from vector_db.vector_db import fetch_last_memories
from summary_generator.summary import summary_generator

def extraction_phase(recent_messages, collection):
    # Get the summary of recent messages
    prev_memories = fetch_last_memories(collection, k=5)
    prev_summary = summary_generator(prev_memories)

    extracted_memory = summary_generator(f"{prev_summary}\n\n[NEW MEMORY]\n\n{recent_messages}")

    return extracted_memory