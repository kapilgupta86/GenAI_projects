import os
from typing import Any

from crewai import LLM


def get_llm() -> Any:
	"""Return a CrewAI-compatible LLM based on environment.
	- If OPENAI_API_KEY is set, use OpenAI (gpt-4o-mini by default)
	- Else if OLLAMA_BASE_URL is set, use Ollama (llama3.1 by default)
	- Else raise a clear error
	"""
	openai_key = os.getenv("OPENAI_API_KEY")
	ollama_url = os.getenv("OLLAMA_BASE_URL")
	if openai_key:
		return LLM(model="gpt-4o-mini", api_key=openai_key)
	if ollama_url:
		# CrewAI 1.x infers provider from model prefix or base_url
		# Using an Ollama-compatible signature
		return LLM(model="ollama/llama3.1", base_url=ollama_url)
	raise RuntimeError(
		"No LLM configured. Set OPENAI_API_KEY for OpenAI or OLLAMA_BASE_URL for Ollama."
	)
