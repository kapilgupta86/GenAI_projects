import json
import pandas as pd

from .prices import fetch_price_history as _fetch_price_history, compute_trend_metrics as _compute_trend_metrics, simple_technical_flags as _simple_technical_flags
from .fundamentals import fetch_fundamentals as _fetch_fundamentals
from .search import web_search as _web_search, fetch_page_summary as _fetch_page_summary


def tool_web_search(query: str) -> str:
	results = _web_search(query, max_results=10)
	return json.dumps(results)


def tool_fetch_page_summary(url: str) -> str:
	text = _fetch_page_summary(url, max_chars=800)
	return text


def tool_fetch_price_history(ticker: str) -> str:
	df = _fetch_price_history(ticker, period="5y", interval="1d").tail(500)
	return df.to_json()


def tool_compute_trend_metrics(prices_json: str) -> str:
	df = pd.read_json(prices_json)
	metrics = _compute_trend_metrics(df)
	return json.dumps(metrics)


def tool_simple_technical_flags(prices_json: str) -> str:
	df = pd.read_json(prices_json)
	flags = _simple_technical_flags(df)
	return json.dumps(flags)


def tool_fetch_fundamentals(ticker: str) -> str:
	data = _fetch_fundamentals(ticker)
	return json.dumps(data)
