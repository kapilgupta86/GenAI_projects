# KnowledgeBot — Project Documentation (Corrected & Verified)

## TL;DR ✅
- Active retrieval pipeline in this workspace: **Ollama embeddings → ChromaDB vector search → Ollama (chat) for answer**.
- **No BM25 or lexical/BM25 hybrid retrieval is used in this project repo** (`knowledge_bot_local22sept`). (A `crew_simple.py` in a different repo uses BM25, but it is external and not imported here.)

---

## Design & Flow (step-by-step)
1. **Ingest**
   - Implemented in `crew.py` → `ingest_task()`
   - Sources: local files (`LocalFileReader`), GitHub (`GitHubRepoCloner`), Google Drive (`GoogleDriveReader`).
   - Output: `List[dict]` with `{"content": str, "metadata": {...}}`.

2. **Chunking & IDs**
   - `_chunk_text(text, chunk_size=800, overlap=100)` (character-based chunking).
   - `_doc_id(chunk + str(meta))` → deterministic SHA1 id used as `id` for upsert.

3. **Embedding**
   - `_ollama_embed_batch(base_url, model, texts)` calls Ollama embed endpoints and returns `List[List[float]]`.
   - Default embed model comes from UI / `KB_EMBED_MODEL` / args (e.g., `nomic-embed-text`, `mistral`).

4. **Persist to ChromaDB**
   - `collection.upsert(ids=ids, embeddings=vectors, metadatas=metadatas, documents=texts)`
   - Chroma persistence: `chromadb.PersistentClient(path="./kb_chroma")` and collection `knowledgebot_collection`.

5. **Query & Retrieval**
   - `query_task()` embeds the question: `qvec = _ollama_embed_batch(...)[0]`
   - `results = collection.query(query_embeddings=[qvec], n_results=top_k)` → returns `documents` and `metadatas`.

6. **Answer Generation**
   - Prompt built from retrieved contexts + question.
   - Primary: POST to Ollama `/api/chat` (model specified in UI). If Ollama chat fails to produce an answer, **OpenAI chat** is used as fallback (if `OPENAI_API_KEY` is set).

7. **Optional saving**
   - If `save_md` provided, writes `knowledgebot_answer.md` containing answer and sources (metadatas).

---

## Environment & Config
- `OLLAMA_BASE_URL` — endpoint for Ollama (embeddings & chat); defaults in code to local service address.
- `KB_EMBED_MODEL` or UI selection — choose embedding model.
- `OPENAI_API_KEY` — used only as fallback for answering; not used for retrieval.
- Persistence dir: `./kb_chroma`

---

## Verification (what I checked)
- Confirmed `crew.py` **calls** `_ollama_embed_batch`, `collection.upsert(...)`, and `collection.query(...)`.
- Verified presence of `tools/custom_tool.py` readers used by `ingest_task`.
- Ran static search across the workspace — found **no** `rank_bm25` / `BM25Okapi` / `_bm25_search` function in the local repo.
- Found `crew_simple.py` with BM25 logic only on the remote repo (`kanilgupta86/GenAI_projects`) you referenced — not in this workspace.

---

## Tests & Checks to add (recommended)
- Add unit tests for `_chunk_text` (boundary conditions) and `_doc_id`.
- Add tests mocking `_ollama_embed_batch` to ensure correct `collection.upsert` parameter formation (ids, embeddings, metadata, documents).
- Add an integration test that ingests a small corpus with a unique phrase, queries it, and asserts returned `metadatas` contain the document.
- Add a debug mode / logging in `query_task` to expose the retrieved `document_id`s and their similarity (Chroma may not return explicit similarity; add a function to compute similarities if needed).

---

## Observability & Improvements
- Switch chunking to token-based chunking (tokenizer) to improve semantic boundaries.
- Add retrieval logging: returned chunk `id`, source `metadata`, and computed cosine similarity.
- If a hybrid retrieval is desired, implement BM25 or SQLite FTS as a lexical fallback and combine scores with vector similarity (configurable weight).

---

## Quick answers to your doubts
- "Are we using BM25?" — **No** in this workspace.
- "Are we using intent-based routing?" — Not in the running code; `crew_simple.py` contains intent detection but it is **not** used in this repo.
- "Are we using Ollama embedding + ChromaDB?" — **Yes** (embeddings are created via Ollama calls and persisted into ChromaDB; retrieval uses the Chroma vector query API).

---

## Where to look in code (exact references)
- `src/knowledge_bot/crew.py` → ingest, embed (upsert), query (query_embeddings), chat answer, fallback to OpenAI.
- `src/knowledge_bot/tools/custom_tool.py` → readers used by `ingest_task`.
- `src/knowledge_bot/config/tasks.yaml` & `agents.yaml` → provides task descriptions and default agents.
- `src/knowledge_bot/tests/agent_x_verifier.py` → quick verifier script.

---

If you'd like, I can:
- Add a `docs/architecture_diagram.md` with an ASCII swimlane or mermaid diagram, or
- Implement the hybrid BM25 proof-of-concept in this repo and add tests that demonstrate lex+vector ranking, or
- Add logging and a small test that verifies retrieval uses embeddings (mocking Ollama + Chroma).  

Which follow-up should I implement next? 🔧
