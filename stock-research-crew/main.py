import json
from typing import Dict, Any
from src.orchestrator import build_crew


def run_once(user_prefs: Dict[str, Any]) -> Dict[str, Any]:
	crew = build_crew(user_prefs)
	result = crew.kickoff()
	return {"text": str(result)}


if __name__ == "__main__":
	prefs = {
		"market": "NSE/BSE or US",
		"theme": "growth or value or momentum",
		"risk": "medium",
		"min_market_cap": "1000Cr or 1B",
		"horizon": "1-2 years",
		"keywords": "buyback earnings IPO demerger uptrend",
	}
	out = run_once(prefs)
	print(json.dumps(out, indent=2))
