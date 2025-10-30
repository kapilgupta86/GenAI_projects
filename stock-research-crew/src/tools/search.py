from typing import List, Dict
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup


def web_search(query: str, max_results: int = 10) -> List[Dict[str, str]]:
	"""Cheap meta-search via DuckDuckGo. Returns list of {title, href, body}."""
	with DDGS() as ddgs:
		results = ddgs.text(query, max_results=max_results)
	return [
		{"title": r.get("title", ""), "href": r.get("href", ""), "body": r.get("body", "")}
		for r in results
	]


def fetch_page_summary(url: str, max_chars: int = 800) -> str:
	"""Fetch page and return a short text summary (first paragraphs)."""
	try:
		resp = requests.get(url, timeout=10)
		resp.raise_for_status()
		soup = BeautifulSoup(resp.text, "html.parser")
		paras = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
		text = " ".join(paras)
		return text[:max_chars]
	except Exception:
		return ""
