# 🧠 Remindr

**Remindr** is a memory-augmented LLM system inspired by the [mem0](https://github.com/mem0ai/mem0) approach, designed to give AI applications a persistent, long-term memory layer.

It uses **Retrieval-Augmented Generation (RAG)** to store, retrieve, and compress user memories — enabling context-aware, personalized AI interactions that improve over time.

---

## Overview

Most LLM applications are stateless — they forget everything the moment a conversation ends. Remindr solves this by maintaining a semantic memory store that persists across sessions.

The memory pipeline:

1. Stores user interactions as vector embeddings in ChromaDB
2. Retrieves semantically relevant past memories during new queries
3. Periodically compresses recent memories into high-signal long-term summaries
4. Injects retrieved context into LLM prompts for personalized, aware responses

---

## Tech Stack

| Component       | Choice                                |
| --------------- | ------------------------------------- |
| LLM Access      | [OpenRouter](https://openrouter.ai)   |
| Model           | `nvidia/nemotron-super-49b-v1:free`   |
| Vector Database | [ChromaDB](https://www.trychroma.com) |
| Architecture    | RAG-based memory system               |

---

## Architecture

Remindr follows the mem0 memory architecture:

```
User Input
    │
    ▼
[Embedding Model]
    │
    ▼
[ChromaDB Vector Store] ◄──── Semantic Search
    │                               │
    ▼                               │
[Memory Retriever] ─────────────────┘
    │
    ▼
[LLM (via OpenRouter)] ◄── Compressed Long-term Memory
    │
    ▼
Response + Memory Update
```

> For a detailed explanation of the underlying approach, see the [mem0 architecture writeup](https://medium.com/@zeng.m.c22381/mem0-overall-architecture-and-principles-8edab6bc6dc4).

---

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd remindr
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

### 3. Add your OpenRouter API key

Open `.env` and set:

```env
OPENROUTER_API_KEY=your_api_key_here
```

Get a free API key at [openrouter.ai/keys](https://openrouter.ai/keys).

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run

```bash
python3 main.py
```

---

## Customization

`main.py` is the main entry point. You can modify it to:

- **Mock user inputs** — simulate conversations without a live UI
- **Test memory patterns** — vary input frequency and content to observe retrieval behavior
- **Tune summarization** — adjust prompts or thresholds for when memories get compressed
- **Connect a frontend** — wire up a chatbot UI or REST API on top of the memory pipeline

---

## Notes

- **API key**: Ensure your OpenRouter key is valid and has access to your chosen model
- **Free models**: May have rate limits or intermittent availability — consider switching to a paid model for production use
- **ChromaDB persistence**: Data is stored locally by default in a `./chroma_db` directory; configure the client for a remote instance if needed

---

## Roadmap

- [ ] Multi-agent shared memory
- [ ] Memory decay and priority scoring
- [ ] Real-time streaming responses
- [ ] React or CLI dashboard
- [ ] Fine-tuned summarization model

---

## Contributing

Forks, experiments, and PRs are welcome. If you build something interesting on top of Remindr, open an issue and share it.
