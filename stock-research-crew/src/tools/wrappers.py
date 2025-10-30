import json
import pandas as pd
from crewai.tools import tool

from .prices import (
	fetch_price_history as _fetch_price_history,
	compute_trend_metrics as _compute_trend_metrics,
	simple_technical_flags as _simple_technical_flags,
)
from .fundamentals import fetch_fundamentals as _fetch_fundamentals
from .search import (
	web_search as _web_search,
	fetch_page_summary as _fetch_page_summary,
)


@tool("web_search")
def WEB_SEARCH(query: str) -> str:
	"""DuckDuckGo web search returning a JSON list of results (title, href, body)."""
	results = _web_search(query, max_results=10)
	return json.dumps(results)


@tool("fetch_page_summary")
def FETCH_PAGE_SUMMARY(url: str) -> str:
	"""Fetch and summarize a webpage into a short text snippet."""
	text = _fetch_page_summary(url, max_chars=800)
	return text


@tool("fetch_price_history")
def FETCH_PRICE_HISTORY(ticker: str) -> str:
	"""Download historical OHLCV price data for a ticker via yfinance; returns JSON DataFrame tail."""
	df = _fetch_price_history(ticker, period="5y", interval="1d").tail(500)
	return df.to_json()


@tool("compute_trend_metrics")
def COMPUTE_TREND_METRICS(prices_json: str) -> str:
	"""Compute trend metrics from a price history DataFrame JSON; returns JSON dict."""
	df = pd.read_json(prices_json)
	metrics = _compute_trend_metrics(df)
	return json.dumps(metrics)


@tool("simple_technical_flags")
def SIMPLE_TECH_FLAGS(prices_json: str) -> str:
	"""Return simple bullish flags from a price history DataFrame JSON; returns JSON list."""
	df = pd.read_json(prices_json)
	flags = _simple_technical_flags(df)
	return json.dumps(flags)


@tool("fetch_fundamentals")
def FETCH_FUNDAMENTALS(ticker: str) -> str:
	"""Fetch a subset of fundamentals for a ticker via yfinance; returns JSON dict."""
	data = _fetch_fundamentals(ticker)
	return json.dumps(data)
