from typing import Dict, Any
from crewai import Crew, Task

from .agents import create_researcher, create_analyst, create_reviewer


def build_crew(user_prefs: Dict[str, Any]) -> Crew:
	researcher = create_researcher()
	analyst = create_analyst()
	reviewer = create_reviewer()

	prompt_preamble = (
		"You are collaborating to find positional uptrend opportunities for 1-2 years. "
		"User constraints: market/theme/risk prefs/filters are provided. Be concise, factual, reproducible."
	)

	research_task = Task(
		description=(
			f"{prompt_preamble}\n\n"
			f"Research mandate: Based on user input {user_prefs}, shortlist 5-12 liquid stocks/ETFs. "
			"For each candidate provide: ticker, market, summary of catalysts (earnings, buybacks, IPO, demerger, setup), "
			"basic fundamentals (marketCap, PE, PB, ROE if available), and simple technicals "
			"(52w range, above 100/200DMA, 6m momentum). Prefer reliable sources and include URLs."
		),
		agent=researcher,
		expected_output=(
			"A JSON-like list of candidates with fields: ticker, name, market, catalysts, fundamentals, technicals, sources."
		),
	)

	analysis_task = Task(
		description=(
			"Analyze the research list and select top 3-6 opportunities suitable for 1-2 year positional trend following. "
			"Explain rationale: fundamental durability, trend health, risk factors, and proposed entry/invalidations."
		),
		agent=analyst,
		dependencies=[research_task],
		expected_output=(
			"A ranked shortlist with rationale and checklist: trend state, valuation sanity, catalysts, risks, and monitoring plan."
		),
	)

	review_task = Task(
		description=(
			"Review the analysis. Either: APPROVE with bullet reasons and any cautions; or REQUEST-REVISIONS with clear actions "
			"(e.g., missing fundamentals, weak trend evidence, lack of sources)."
		),
		agent=reviewer,
		dependencies=[analysis_task],
		expected_output=(
			"One of: 'APPROVE: <reasons and final list>' or 'REQUEST-REVISIONS: <what to redo and why>'."
		),
	)

	return Crew(agents=[researcher, analyst, reviewer], tasks=[research_task, analysis_task, review_task])
