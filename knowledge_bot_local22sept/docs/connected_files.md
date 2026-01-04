# Connected Files Manifest

This document lists the files that are actually connected and used by this project (KnowledgeBot) and describes how they reference each other.

## Entry point / orchestrator
- `src/knowledge_bot/crew.py` (CORE)
  - Defines the `KnowledgeBotCrew` class (Crew, agents, tasks).
  - Creates Chroma persistent client: `chromadb.PersistentClient(path="./kb_chroma")`.
  - Tasks implemented: `ingest_task`, `embed_task`, `query_task` (see code in file).

## Agents (builders)
- `src/knowledge_bot/agents/embed_agent.py` — provides the embed Agent used by `embed_task`.
- `src/knowledge_bot/agents/query_agent.py` — provides the query Agent used by `query_task`.
- `src/knowledge_bot/agents/file_agent.py` — provides the file Agent used by `ingest_task`.

## Tools & Readers
- `src/knowledge_bot/tools/custom_tool.py`
  - `LocalFileReader(folder)` — reads `.pdf`, `.docx`, `.txt`, `.csv`, `.xlsx` from a folder and returns a list of `{"content": str, "metadata": {...}}`.
  - `GitHubRepoCloner(repo_url)` — clones repo and returns files from repo.
  - `GoogleDriveReader(folder_id)` — reads Google Drive files.

## Config & Metadata
- `src/knowledge_bot/config/tasks.yaml` — describes tasks and expected outputs.
- `src/knowledge_bot/config/agents.yaml` — agent descriptions and default goals.
- `src/knowledge_bot/README.md` & top-level `README.md` — project docs and usage.

## Tests
- `src/knowledge_bot/tests/agent_x_verifier.py` — rudimentary verifier that checks crew wiring, `ingest_task`, `embed_task`, and `query_task` return expected shapes.

## Persistent Store
- `kb_chroma/` (directory) — ChromaDB persistence path used by `chromadb.PersistentClient`.

---

## How these files connect (call graph)
- `ingest_task` (in `crew.py`) → uses `LocalFileReader` / `GitHubRepoCloner` / `GoogleDriveReader` to produce `documents: List[dict]`.
- `embed_task` (in `crew.py`) → chunks each doc via `_chunk_text`, builds deterministic IDs with `_doc_id`, calls `_ollama_embed_batch` to get embeddings, then `collection.upsert(ids, embeddings, metadatas, documents)` into Chroma.
- `query_task` (in `crew.py`) → embeds the query with `_ollama_embed_batch(...)[0]`, calls `collection.query(query_embeddings=[qvec], n_results=top_k)`, then sends the combined contexts to Ollama chat (POST `/api/chat`) to generate answer; if Ollama fails for answering, falls back to OpenAI chat.

---

## Not in use in this repo
- No `crew_simple.py` file is present in this workspace. The `crew_simple.py` you referenced exists in a different repo and implements an **optional BM25** lexical retrieval (via `rank_bm25.BM25Okapi`) and a different flow (lexical retrieval + Ollama for answering). That file is NOT used by the running project in this workspace.


