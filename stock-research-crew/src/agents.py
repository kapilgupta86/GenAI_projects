from typing import List
from crewai import Agent

from .tools.wrappers import (
	WEB_SEARCH,
	FETCH_PAGE_SUMMARY,
	FETCH_PRICE_HISTORY,
	COMPUTE_TREND_METRICS,
	SIMPLE_TECH_FLAGS,
	FETCH_FUNDAMENTALS,
)
from .llm import get_llm


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
		tools=[WEB_SEARCH, FETCH_PAGE_SUMMARY, FETCH_PRICE_HISTORY, COMPUTE_TREND_METRICS, SIMPLE_TECH_FLAGS, FETCH_FUNDAMENTALS],
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
		tools=[FETCH_PRICE_HISTORY, COMPUTE_TREND_METRICS, SIMPLE_TECH_FLAGS, FETCH_FUNDAMENTALS],
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
		tools=[FETCH_PRICE_HISTORY, COMPUTE_TREND_METRICS, SIMPLE_TECH_FLAGS, FETCH_FUNDAMENTALS, WEB_SEARCH, FETCH_PAGE_SUMMARY],
		llm=get_llm(),
	)
