from typing import List
from crewai import Agent

from .tools.wrappers import (
	tool_web_search,
	tool_fetch_page_summary,
	tool_fetch_price_history,
	tool_compute_trend_metrics,
	tool_simple_technical_flags,
	tool_fetch_fundamentals,
)
from .llm import get_llm


def _tools_for_researcher():
	return [
		{"name": "web_search", "description": "DuckDuckGo web search", "function": tool_web_search},
		{"name": "fetch_page_summary", "description": "Fetch and summarize webpage", "function": tool_fetch_page_summary},
		{"name": "fetch_price_history", "description": "OHLCV for ticker as JSON", "function": tool_fetch_price_history},
		{"name": "compute_trend_metrics", "description": "Trend metrics from prices JSON", "function": tool_compute_trend_metrics},
		{"name": "simple_technical_flags", "description": "Bullish flags from prices JSON", "function": tool_simple_technical_flags},
		{"name": "fetch_fundamentals", "description": "Subset fundamentals via yfinance", "function": tool_fetch_fundamentals},
	]


def _tools_for_analyst():
	return [
		{"name": "fetch_price_history", "description": "OHLCV for ticker as JSON", "function": tool_fetch_price_history},
		{"name": "compute_trend_metrics", "description": "Trend metrics from prices JSON", "function": tool_compute_trend_metrics},
		{"name": "simple_technical_flags", "description": "Bullish flags from prices JSON", "function": tool_simple_technical_flags},
		{"name": "fetch_fundamentals", "description": "Subset fundamentals via yfinance", "function": tool_fetch_fundamentals},
	]


def _tools_for_reviewer():
	return [
		{"name": "fetch_price_history", "description": "OHLCV for ticker as JSON", "function": tool_fetch_price_history},
		{"name": "compute_trend_metrics", "description": "Trend metrics from prices JSON", "function": tool_compute_trend_metrics},
		{"name": "simple_technical_flags", "description": "Bullish flags from prices JSON", "function": tool_simple_technical_flags},
		{"name": "fetch_fundamentals", "description": "Subset fundamentals via yfinance", "function": tool_fetch_fundamentals},
		{"name": "web_search", "description": "DuckDuckGo web search", "function": tool_web_search},
		{"name": "fetch_page_summary", "description": "Fetch and summarize webpage", "function": tool_fetch_page_summary},
	]


def create_researcher() -> Agent:
	return Agent(
		role="Agent2 - Researcher",
		goal=(
			"Discover promising stocks and ETFs aligned with the user's horizon (1-2 years) "
			"and theme, and collect key signals: earnings, buybacks, demergers, IPOs, and "
			"basic technical parameters."
		),
		backstory=(
			"Financial research specialist who scouts high-probability opportunities using "
			"cheap/free public sources. Aggregates concise, factual briefs for analysis."
		),
		allow_delegation=False,
		allow_code_execution=False,
		tools=_tools_for_researcher(),
		llm=get_llm(),
	)


def create_analyst() -> Agent:
	return Agent(
		role="Agent1 - Analyst",
		goal=(
			"Evaluate the researcher's candidates using fundamental and technical factors to "
			"identify positional uptrend opportunities suitable for holding 1-2 years."
		),
		backstory=(
			"Seasoned stock market analyst with deep fundamental and technical understanding. "
			"Focus on risk-managed entries within sustained uptrends."
		),
		allow_delegation=False,
		allow_code_execution=False,
		tools=_tools_for_analyst(),
		llm=get_llm(),
	)


def create_reviewer() -> Agent:
	return Agent(
		role="Agent3 - Reviewer",
		goal=(
			"Critically review the analyst and researcher outputs, highlight gaps, and either "
			"approve with reasons or request revisions with concrete instructions."
		),
		backstory=(
			"Senior investment reviewer ensuring thesis quality, data sufficiency, and "
			"alignment with user's constraints before approval."
		),
		allow_delegation=False,
		allow_code_execution=False,
		tools=_tools_for_reviewer(),
		llm=get_llm(),
	)
