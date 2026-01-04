# src/knowledge_bot/crew.py
from typing import Any, Dict, List
import hashlib
import os
from dataclasses import dataclass
from pathlib import Path

import requests
import chromadb
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from .tools.custom_tool import LocalFileReader, GitHubRepoCloner, GoogleDriveReader
from .agents.file_agent import build_file_agent
from .agents.github_agent import build_github_agent
from .agents.drive_agent import build_drive_agent
from .agents.embed_agent import build_embed_agent
from .agents.query_agent import build_query_agent

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
AGENTS_YAML = (BASE_DIR / "config" / "agents.yaml").as_posix()
TASKS_YAML  = (BASE_DIR / "config" / "tasks.yaml").as_posix()

def _chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> List[str]:
    if not text:
        return []
    n = len(text)
    chunks: List[str] = []
    start = 0
    while start < n:
        end = min(n, start + chunk_size)
        chunks.append(text[start:end])
        start = start + chunk_size - overlap
        if start <= 0 or start >= n:
            break
    return chunks

def _doc_id(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()

def _ollama_embed_batch(base_url: str, model: str, texts: List[str]) -> List[List[float]]:
    try:
        resp = requests.post(f"{base_url}/api/embed", json={"model": model, "input": texts}, timeout=180)
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, dict) and "embeddings" in data:
                return data["embeddings"]
            if isinstance(data, dict) and "data" in data:
                return [item.get("embedding", []) for item in data["data"]]
            if isinstance(data, dict) and "embedding" in data:
                return [data["embedding"]] * len(texts)
    except Exception:
        pass
    vectors: List[List[float]] = []
    for t in texts:
        r = requests.post(f"{base_url}/api/embeddings", json={"model": model, "prompt": t}, timeout=180)
        r.raise_for_status()
        jd = r.json()
        vectors.append(jd.get("embedding", []))
    return vectors

@dataclass
class RAGStore:
    client: chromadb.PersistentClient
    collection_name: str
    def get_or_create(self):
        return self.client.get_or_create_collection(self.collection_name)

@CrewBase
class KnowledgeBotCrew:
    """Ingest → embed to Chroma → retrieve and answer via Ollama (with optional OpenAI fallback)."""
    agents_config = AGENTS_YAML
    tasks_config  = TASKS_YAML

    def __init__(self):
        self.persist_dir = os.path.abspath("./kb_chroma")
        os.makedirs(self.persist_dir, exist_ok=True)
        self.chroma = chromadb.PersistentClient(path=self.persist_dir)
        self.collection_name = "knowledgebot_collection"
        self.rag_store = RAGStore(client=self.chroma, collection_name=self.collection_name)

    @agent
    def file_agent(self) -> Agent:
        return build_file_agent(self.agents_config["file_agent"])  # type: ignore[index]

    @agent
    def github_agent(self) -> Agent:
        return build_github_agent(self.agents_config["github_agent"])  # type: ignore[index]

    @agent
    def drive_agent(self) -> Agent:
        return build_drive_agent(self.agents_config["drive_agent"])  # type: ignore[index]

    @agent
    def embed_agent(self) -> Agent:
        return build_embed_agent(self.agents_config["embed_agent"])  # type: ignore[index]

    @agent
    def query_agent(self) -> Agent:
        return build_query_agent(self.agents_config["query_agent"])  # type: ignore[index]

    @task
    def ingest_task(self) -> Task:
        def run(inputs: Dict[str, Any]) -> Dict[str, Any]:
            folder = inputs.get("folder_path") or os.path.join(os.path.expanduser("~"), "Desktop")
            gh_url = inputs.get("github_url") or ""
            use_drive = bool(inputs.get("use_drive"))
            drive_folder_id = inputs.get("drive_folder_id") or None

            local_docs = LocalFileReader(folder)
            _, gh_docs = GitHubRepoCloner(gh_url) if gh_url else ("", [])
            drive_docs = GoogleDriveReader(drive_folder_id) if use_drive else []

            all_docs: List[Dict[str, Any]] = []
            for d in (local_docs + gh_docs + drive_docs):
                if d.get("content"):
                    all_docs.append(d)
            return {"documents": all_docs, "count": len(all_docs)}
        return Task(config=self.tasks_config["ingest_task"], agent=self.file_agent(), function=run)  # type: ignore[index]

    @task
    def embed_task(self) -> Task:
        def run(inputs: Dict[str, Any]) -> Dict[str, Any]:
            documents = inputs.get("documents", [])
            if not documents:
                return {"embedded": 0, "collection": self.collection_name}
            base_url = os.getenv("OLLAMA_BASE_URL", "http://ollama-service.ollama.svc.cluster.local:11434")
            embed_model = inputs.get("embed_model") or "nomic-embed-text"
            collection = self.rag_store.get_or_create()
            ids: List[str] = []
            metadatas: List[Dict[str, Any]] = []
            texts: List[str] = []
            for d in documents:
                meta = d.get("metadata", {})
                chunks = _chunk_text(d["content"], chunk_size=800, overlap=100)
                for ch in chunks:
                    ids.append(_doc_id(ch + str(meta)))
                    metadatas.append(meta)
                    texts.append(ch)
            vectors = _ollama_embed_batch(base_url, embed_model, texts)
            collection.upsert(ids=ids, embeddings=vectors, metadatas=metadatas, documents=texts)
            return {"embedded": len(ids), "collection": self.collection_name}
        return Task(config=self.tasks_config["embed_task"], agent=self.embed_agent(), function=run)  # type: ignore[index]

    @task
    def query_task(self) -> Task:
        def run(inputs: Dict[str, Any]) -> Dict[str, Any]:
            question = inputs.get("query") or ""
            if not question.strip():
                return {"answer": "Please provide a query.", "sources": []}
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            embed_model = inputs.get("embed_model") or "nomic-embed-text"
            top_k = int(inputs.get("top_k") or 5)
            model = inputs.get("model") or "llama3"
            save_md = inputs.get("save_markdown")
            collection = self.rag_store.get_or_create()
            qvec = _ollama_embed_batch(base_url, embed_model, [question])[0]
            results = collection.query(query_embeddings=[qvec], n_results=top_k)
            contexts: List[str] = results.get("documents", [[]])[0]
            metas: List[Dict[str, Any]] = results.get("metadatas", [[]])[0]
            prompt = (
                "Answer the question using only the provided context; "
                "cite file paths or sources when helpful.\n\n"
                f"Context:\n{os.linesep.join(contexts)}\n\nQuestion: {question}\n"
            )
            answer = ""
            try:
                resp = requests.post(
                    f"{base_url}/api/chat",
                    json={
                        "model": model,
                        "messages": [
                            {"role": "system", "content": "You are a helpful assistant that is concise and strictly grounded in the given context."},
                            {"role": "user", "content": prompt},
                        ],
                        "options": {"temperature": 0.2}
                    },
                    timeout=180
                )
                if resp.status_code == 200:
                    data = resp.json()
                    answer = data.get("message", {}).get("content") or data.get("response") or ""
            except Exception:
                answer = ""
            if not answer.strip():
                api_key = os.getenv("OPENAI_API_KEY")
                if api_key:
                    try:
                        from openai import OpenAI
                        client = OpenAI(api_key=api_key)
                        oai = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": "You are a helpful assistant that is concise and strictly grounded in the provided context."},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.2
                        )
                        answer = oai.choices[0].message.content or ""
                    except Exception as e:
                        answer = f"Both Ollama and OpenAI fallback failed: {e}"
            if save_md:
                out_path = os.path.abspath(save_md if isinstance(save_md, str) else "./knowledgebot_answer.md")
                try:
                    with open(out_path, "w", encoding="utf-8") as f:
                        f.write(f"# Answer\n\n{answer}\n\n## Sources\n")
                        for m in metas:
                            f.write(f"- {m}\n")
                except Exception:
                    pass
            return {"answer": answer, "sources": metas}
        return Task(config=self.tasks_config["query_task"], agent=self.query_agent(), function=run)  # type: ignore[index]

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential, verbose=True)

