from extraction.extractor import extraction_phase
from vector_db.vector_db import init_chromadb

if __name__ == "__main__":
    # Simulate a conversation
    recent_messages = "User: I had a great day! I went to the park and enjoyed the sunshine."
    collection = init_chromadb()

    # Perform the extraction phase
    extracted_memory = extraction_phase(recent_messages, collection)

    print("Extracted Memory:")
    print(extracted_memory)

    