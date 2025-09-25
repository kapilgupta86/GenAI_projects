import requests
import json

def test_ollama():
    base_url = "http://ollama-service.ollama.svc.cluster.local:11434"
    
    # Test streaming vs non-streaming
    response = requests.post(f"{base_url}/api/chat", json={
        "model": "mistral",
        "messages": [{"role": "user", "content": "What are my interests based on: AI, DevOps, Kubernetes"}],
        "stream": False,  # Disable streaming
        "options": {"temperature": 0.2, "num_predict": 200}
    }, timeout=30)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        answer = data.get("message", {}).get("content", "")
        print(f"Parsed answer: {answer}")

if __name__ == "__main__":
    test_ollama()
