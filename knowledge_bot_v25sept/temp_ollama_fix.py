def _generate_answer_with_ollama(query: str, contexts: List[str], base_url: str = None, model: str = "mistral") -> str:
    """Generate answer using Ollama with provided context."""
    if not base_url:
        base_url = os.getenv("OLLAMA_BASE_URL", "http://ollama-service.ollama.svc.cluster.local:11434")
    
    if not contexts:
        return "I couldn't find relevant information in your documents to answer this question."
    
    # Prepare context - limit to avoid token limits
    context_text = "\n\n".join(contexts[:2])[:1500]
    
    # Create prompt
    prompt = f"""Answer the question based on the provided context. Be direct and concise.

Context:
{context_text}

Question: {query}

Answer:"""

    try:
        print(f"[OLLAMA] Querying {base_url} with model {model}")
        response = requests.post(f"{base_url}/api/chat", json={
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant. Answer questions based on the provided context. Be concise."},
                {"role": "user", "content": prompt}
            ],
            "stream": False,  # Disable streaming to avoid JSON parsing issues
            "options": {
                "temperature": 0.2,
                "num_predict": 500,
                "num_ctx": 2048
            }
        }, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get("message", {}).get("content", "")
            if answer:
                print(f"[OLLAMA] Got response: {answer[:100]}...")
                return answer.strip()
        else:
            print(f"[OLLAMA] Error: {response.status_code} - {response.text}")
    except requests.exceptions.JSONDecodeError as e:
        print(f"[OLLAMA] JSON decode error: {e}")
        print(f"[OLLAMA] Raw response: {response.text[:200]}...")
    except Exception as e:
        print(f"[OLLAMA] Error: {e}")
    
    # Fallback to simple answer
    print("[OLLAMA] Falling back to simple answer")
    return _generate_simple_answer(query, contexts)
