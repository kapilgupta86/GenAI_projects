from typing import Dict, Any
import yfinance as yf


KEYS = [
	"marketCap",
	"forwardPE",
	"trailingPE",
	"priceToBook",
	"pegRatio",
	"profitMargins",
	"returnOnEquity",
	"revenueGrowth",
	"earningsGrowth",
]


def fetch_fundamentals(ticker: str) -> Dict[str, Any]:
	"""Fetch a subset of fundamentals and normalize types."""
	info = yf.Ticker(ticker).info or {}
	result: Dict[str, Any] = {k: info.get(k) for k in KEYS}
	# Normalize to python primitives
	for k, v in list(result.items()):
		if hasattr(v, "item"):
			try:
				result[k] = v.item()
			except Exception:
				pass
	return result
