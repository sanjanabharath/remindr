from extraction.extractor import extraction_phase
from memory.memories import update_phase
from vector_db.vector_db import fetch_all_memories, init_chromadb

if __name__ == "__main__":
    # Simulate a conversation
    recent_messages = input("User: ")
    collection = init_chromadb()

    # Perform the extraction phase
    extracted_memory = extraction_phase(recent_messages, collection)

    # print("Extracted Memory:", extracted_memory)

    update_phase(extracted_memory, collection)

    print("Memory updated in the vector database.")

    print("All memories in the vector database:")
    
    for doc, metadata in fetch_all_memories(collection):
        print(f"Document: {doc}")