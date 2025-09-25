# src/knowledge_bot/crew_simple.py
from typing import Any, Dict, List, Tuple
import os, re, json, requests

# Optional BM25 scorer
try:
    from rank_bm25 import BM25Okapi
    HAS_BM25 = True
except Exception:
    HAS_BM25 = False

def _detect_intent(q: str) -> str:
    ql = (q or "").lower().strip()
    if any(x in ql for x in ["who am i", "what is my name", "who i am"]) and "interest" not in ql:
        return "personal_info"
    if "list" in ql and (".py" in ql or ".md" in ql):
        return "list_files"
    if ("project" in ql or "projects" in ql) and any(y in ql for y in ["list", "show", "folder", "path", "directory"]):
        return "list_projects"
    return "rag_query"

def _extract_versions(q: str) -> List[str]:
    versions = set(re.findall(r"\bv?\d+(?:[._]\d+){1,3}\b", (q or "").lower()))
    normalized = {v.replace("_", ".") for v in versions}
    return list(versions | normalized)

def _expand_query_terms(q: str) -> List[str]:
    ql = (q or "").lower()
    tokens = set(re.findall(r"\w+", ql))
    mapping = {
        "install": {"installation", "setup", "configure", "deploy", "deployment", "install"},
        "procedure": {"procedure", "steps", "runbook", "guide", "howto"},
        "pod": {"pod", "pods"},
        "max": {"max", "m.a.x", "m_a_x"},
        "release": {"release", "version"},
        "ecp": {"ecp"},
    }
    for t in list(tokens):
        if t in mapping:
            tokens |= mapping[t]
    for v in _extract_versions(q):
        tokens.add(v)
        tokens.add(v.lstrip("v"))
        tokens.add(v.replace("_", "."))
        tokens.add(v.replace(".", "_"))
    return list(tokens)

def _chunk_text(text: str, chunk_size: int = 700, overlap: int = 120) -> List[str]:
    if not text:
        return []
    out, n, start = [], len(text), 0
    while start < n:
        end = min(n, start + chunk_size)
        out.append(text[start:end])
        if end >= n:
            break
        start = max(0, end - overlap)
    return out

def _load_documents_from_folder(folder_path: str) -> List[Dict[str, Any]]:
    try:
        import sys
        sys.path.append("./src")
        from knowledge_bot.tools.custom_tool import LocalFileReader

        raw_docs = LocalFileReader(folder_path)
        print(f"[RAG] Loaded {len(raw_docs)} documents from {folder_path}")

        chunked: List[Dict[str, Any]] = []
        for d in raw_docs:
            content = (d.get("content") or "").strip()
            meta = d.get("metadata", {})
            if not content or len(content) < 50:
                continue
            chunks = _chunk_text(content, 700, 120)
            for i, ch in enumerate(chunks):
                md = meta.copy()
                md["chunk_id"] = i
                md["total_chunks"] = len(chunks)
                md["name"] = md.get("name") or os.path.basename(md.get("path", "") or "") or "unknown"
                chunked.append({"content": ch, "metadata": md})

        print(f"[RAG] Created {len(chunked)} chunks")
        for c in chunked[:2]:
            md = c["metadata"]
            print(f"[RAG] Example chunk from {md.get('name', 'unknown')} page={md.get('page')}, len={len(c['content'])}")
        return chunked
    except Exception as e:
        print(f"[RAG] Error loading documents: {e}")
        import traceback; traceback.print_exc()
        return []

def _bm25_search(query: str, docs: List[Dict[str, Any]], top_k: int = 7) -> List[Tuple[float, Dict[str, Any]]]:
    if not HAS_BM25 or not docs:
        return []
    tokenized_corpus = [re.findall(r"\w+", (d["content"] or "").lower()) for d in docs]
    bm25 = BM25Okapi(tokenized_corpus)
    expanded = _expand_query_terms(query)
    scores = [bm25.get_scores(re.findall(r"\w+", t)) for t in expanded]
    avg_score = [sum(vals) / max(1, len(vals)) for vals in zip(*scores)]

    versions = _extract_versions(query)
    phrase = (query or "").lower()
    scored: List[Tuple[float, Dict[str, Any]]] = []
    for idx, d in enumerate(docs):
        s = avg_score[idx]
        text = (d["content"] or "").lower()

        # Version boosts
        for v in versions:
            if v in text or v.lstrip("v") in text or v.replace(".", "_") in text:
                s += 2.0

        # Procedure/install bias
        if any(k in phrase for k in ["install", "installation", "steps", "procedure", "runbook", "setup"]):
            if any(k in text for k in ["install", "installation", "steps", "procedure", "runbook", "setup", "deploy"]):
                s += 1.5

        # Section hint
        if any(k in text for k in ["prerequisites", "requirements", "overview", "installation steps"]):
            s += 0.5

        scored.append((s, d))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]

def _simple_search(query: str, docs: List[Dict[str, Any]], top_k: int = 7) -> List[Tuple[float, Dict[str, Any]]]:
    q_terms = set(re.findall(r"\w+", (query or "").lower()))
    out: List[Tuple[float, Dict[str, Any]]] = []
    for d in docs:
        text = (d["content"] or "").lower()
        if not text:
            continue
        c_terms = set(re.findall(r"\w+", text))
        overlap = len(q_terms & c_terms)
        if overlap <= 0:
            continue
        phrase_bonus = 0.2 * sum(text.count(t) for t in q_terms if t in text)
        out.append((overlap + phrase_bonus, d))
    out.sort(key=lambda x: x[0], reverse=True)
    return out[:top_k]

def _compose_contexts(chosen: List[Dict[str, Any]]) -> List[str]:
    contexts: List[str] = []
    for d in chosen:
        md = d.get("metadata", {})
        name = md.get("name", "unknown")
        page = md.get("page")
        header = f"Source: {name}" + (f" (page {page})" if page else "")
        contexts.append(f"{header}\n\n{d['content']}")
    return contexts

def _ollama_chat_stream_or_json(base_url: str, payload: Dict[str, Any], timeout_connect: int = 20, timeout_read: int = 120) -> str:
    url = f"{base_url.rstrip('/')}/api/chat"
    payload = dict(payload)
    payload.setdefault("stream", True)
    try:
        with requests.post(url, json=payload, stream=True, timeout=(timeout_connect, timeout_read)) as r:
            r.raise_for_status()
            ctype = (r.headers.get("Content-Type") or "").lower()

            # Non-stream JSON
            if "application/json" in ctype and not r.headers.get("Transfer-Encoding") == "chunked":
                jd = r.json()
                return (jd.get("message", {}) or {}).get("content", "") or jd.get("response", "") or ""

            # Streaming JSONL
            parts: List[str] = []
            for line in r.iter_lines(decode_unicode=True):
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                msg = obj.get("message") or {}
                content = msg.get("content") or ""
                if content:
                    parts.append(content)
                if obj.get("done"):
                    break
            return "".join(parts).strip()
    except Exception as e:
        print(f"[OLLAMA] Error: {e}")
        return ""

def _generate_simple_answer(query: str, contexts: List[str]) -> str:
    if not contexts:
        return "No relevant context was found to answer this question."
    ql = (query or "").lower()
    if any(k in ql for k in ["install", "installation", "steps", "procedure", "runbook", "setup"]):
        lines = []
        for ctx in contexts:
            for line in ctx.splitlines():
                if re.search(r"^\s*\d+[\.\)]\s+", line) or any(k in line.lower() for k in ["install", "step", "prerequisite", "verify"]):
                    lines.append(line.strip())
        if lines:
            return "Installation steps derived from context:\n- " + "\n- ".join(lines[:20])
    return f"Based on the context:\n\n{contexts[0][:900]}"

def _generate_answer_with_ollama(query: str, contexts: List[str], base_url: str = None, model: str = "mistral") -> str:
    base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://ollama-service.ollama.svc.cluster.local:11434")
    if not contexts:
        return "No relevant context was found to answer this question."

    context_text = "\n\n---\n\n".join(contexts[:3])[:3500]
    wants_steps = any(k in (query or "").lower() for k in ["install", "installation", "steps", "procedure", "runbook", "setup"])
    style_instr = (
        "Return numbered, actionable steps with prerequisites and post-checks. Cite the page next to each key item when available. "
        if wants_steps else
        "Return a concise, factual answer grounded only in the context. "
    )
    prompt = (
        f"{style_instr}"
        "If the context does not contain the answer, say exactly 'Not found in the provided context.'\n\n"
        f"Context:\n{context_text}\n\nQuestion: {query}\nAnswer:"
    )
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You answer only from the provided context and never invent details."},
            {"role": "user", "content": prompt},
        ],
        "stream": True,
        "options": {"temperature": 0.2, "num_predict": 700, "num_ctx": 4096},
    }
    print(f"[OLLAMA] Querying {base_url} with model {model}")
    answer = _ollama_chat_stream_or_json(base_url, payload)
    if answer:
        return answer.strip()
    print("[OLLAMA] Falling back to simple answer")
    return _generate_simple_answer(query, [c.split("\n\n", 1)[-1] for c in contexts])

def process_query_direct(query: str, folder_path: str = "./knowledge") -> Dict[str, Any]:
    folder_path = os.path.abspath(folder_path)
    intent = _detect_intent(query)

    print(f"[DIRECT] Processing: '{query}'")
    print(f"[DIRECT] Intent: {intent}")
    print(f"[DIRECT] Folder: {folder_path}")

    if intent == "personal_info":
        try:
            pref = os.path.join(folder_path, "user_preference.txt")
            if os.path.exists(pref):
                with open(pref, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip().lower().startswith("name:"):
                            return {"answer": line.split(":", 1)[1].strip(),
                                    "sources": [{"intent": "personal_info", "file": "user_preference.txt"}]}
        except Exception as e:
            print(f"[DIRECT] Profile read error: {e}")
        return {"answer": "Kapil", "sources": [{"intent": "personal_info", "source": "fallback"}]}

    if intent == "list_files":
        base = folder_path
        m = re.search(r"\{([^}]+)\}", query or "")
        if m:
            base = m.group(1).strip()
        files: List[str] = []
        try:
            for root, _, fns in os.walk(base):
                for name in fns:
                    if name.lower().endswith((".py", ".md")):
                        files.append(os.path.join(root, name))
        except Exception:
            pass
        return {"answer": "\n".join(files) if files else f"No .py or .md files found in {base}",
                "sources": [{"intent": "list_files", "base_path": base, "count": len(files)}]}

    if intent == "list_projects":
        base = folder_path
        m = re.search(r"\{([^}]+)\}", query or "")
        if m:
            base = m.group(1).strip()
        projects: List[str] = []
        try:
            for root, dirs, files in os.walk(base):
                if any(x in files for x in ["README.md", ".git", "requirements.txt", "package.json", "pyproject.toml"]):
                    projects.append(root)
                    dirs[:] = []
                if root.count(os.sep) - base.count(os.sep) >= 3:
                    dirs[:] = []
        except Exception:
            pass
        return {"answer": "\n".join(projects) if projects else f"No projects found in {base}",
                "sources": [{"intent": "list_projects", "base_path": base, "count": len(projects)}]}

    # RAG path
    print("[RAG] Processing document search query...")
    docs = _load_documents_from_folder(folder_path)
    if not docs:
        return {"answer": "No documents found to search. Please add files to your knowledge directory.",
                "sources": [{"intent": "rag_no_docs"}]}

    chosen_scored: List[Tuple[float, Dict[str, Any]]] = []
    if HAS_BM25:
        chosen_scored = _bm25_search(query, docs, top_k=7)
    if not chosen_scored:
        chosen_scored = _simple_search(query, docs, top_k=7)

    if not chosen_scored:
        return {"answer": f"I couldn't find information about '{query}' in your documents.",
                "sources": [{"intent": "rag_no_results"}]}

    chosen_docs = [d for _, d in chosen_scored[:5]]
    contexts = _compose_contexts(chosen_docs)
    base_url = os.getenv("OLLAMA_BASE_URL", "").strip() or None
    answer = _generate_answer_with_ollama(query, contexts, base_url=base_url, model=os.getenv("KB_MODEL", "mistral"))

    sources = []
    for d in chosen_docs:
        md = d.get("metadata", {})
        sources.append({
            "name": md.get("name") or os.path.basename(md.get("path", "") or ""),
            "page": md.get("page"),
            "path": md.get("path"),
        })
    return {"answer": answer, "sources": sources + [{"intent": "rag_query", "chunks_used": len(contexts)}]}

