import chromadb
from chromadb.config import Settings
import uuid
from datetime import datetime
# 1. Init ChromaDB client and collection

def init_chromadb():
    client = chromadb.Client(
    Settings(persist_directory="./chroma_db")
)
    collection = client.get_or_create_collection(name="my_memory")
    return collection

def add_to_memory(collection, value):

    key = str(uuid.uuid4())

    collection.add(
        documents=[value],
        metadatas={"timestamp": datetime.now().timestamp()},
        ids=[key]
    )

def delete_memory(collection, key):
    collection.delete(ids=[key])

def update_memory(collection, key, new_value):
    collection.update(
        ids=[key],
        documents=[new_value],
        metadatas={"timestamp": datetime.now().timestamp()}
    )

def relevant_memories(collection, summary, s=5):
    res = collection.query(
        query_texts=[summary],
        n_results=s,
        include=["documents", "metadatas"]
    )
    return res

def fetch_last_memories(collection, k=10):
    res = collection.get(include=["documents", "metadatas"])
    
    sorted_docs = sorted(
        zip(res["documents"], res["metadatas"]),
        key=lambda x: x[1].get("timestamp", 0),
        reverse=True
    )
    
    return sorted_docs[:k]