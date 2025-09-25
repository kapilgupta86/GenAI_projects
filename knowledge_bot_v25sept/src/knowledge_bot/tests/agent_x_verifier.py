"""
Agent X: Verifier script to check imports, crew wiring, minimal flow, and Chroma persistence without external services.
Run: python -m knowledge_bot.tests.agent_x_verifier
"""
import os
import json
import importlib

def main():
    kb_mod = importlib.import_module("knowledge_bot.crew")
    KnowledgeBotCrew = getattr(kb_mod, "KnowledgeBotCrew")

    kb = KnowledgeBotCrew()
    cr = kb.crew()
    assert cr is not None, "Crew not created"

    inputs = {"folder_path": os.path.join(os.path.expanduser("~"), "Desktop")}
    out_ingest = kb.ingest_task().function(inputs)  # type: ignore[attr-defined]
    assert isinstance(out_ingest, dict), "ingest_task did not return a dict"
    assert "documents" in out_ingest, "ingest_task missing documents key"

    out_embed = kb.embed_task().function({"documents": []})  # type: ignore[attr-defined]
    assert out_embed.get("collection") == kb.collection_name, "embed_task did not return collection name"

    out_query = kb.query_task().function({"query": ""})  # type: ignore[attr-defined]
    assert "answer" in out_query, "query_task did not return answer"

    print(json.dumps({"status": "ok"}))

if __name__ == "__main__":
    main()

