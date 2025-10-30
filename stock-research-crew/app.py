import json
import re
import streamlit as st
from src.orchestrator import build_crew

st.set_page_config(page_title="CrewAI Stock Research", layout="wide")

st.title("CrewAI Stock Research Team")
st.markdown("Enter your preferences and let the 3-agent crew research, analyze, and review opportunities.")

with st.sidebar:
	st.header("Inputs")
	market = st.selectbox("Market", ["India (NSE/BSE)", "US", "Other"], index=0)
	theme = st.selectbox("Theme", ["Momentum", "Growth", "Value", "Quality"], index=0)
	risk = st.selectbox("Risk", ["Low", "Medium", "High"], index=1)
	min_mcap = st.text_input("Min Market Cap (e.g., 2000Cr, 2B)", "2000Cr")
	horizon = st.selectbox("Horizon", ["1 year", "2 years"], index=1)
	keywords = st.text_input("Keywords", "earnings buyback IPO demerger uptrend setup")
	tickers_hint = st.text_input("Optional tickers hint (comma-separated)", "")
	go = st.button("Run Crew")

if go:
	user_prefs = {
		"market": market,
		"theme": theme,
		"risk": risk,
		"min_market_cap": min_mcap,
		"horizon": horizon,
		"keywords": keywords,
		"tickers_hint": [t.strip() for t in tickers_hint.split(",") if t.strip()],
	}
	crew = build_crew(user_prefs)
	with st.spinner("Running agents (research → analysis → review)..."):
		out = crew.kickoff()

	text = str(out)
	approved = bool(re.search(r"\bAPPROVE\b", text, re.IGNORECASE))

	st.subheader("Reviewer Decision")
	if approved:
		st.success("APPROVED by Agent3 - showing final results")
	else:
		st.error("Reviewer requested revisions. Showing feedback for iteration.")

	st.code(text)

	if approved:
		st.markdown("Download result")
		st.download_button(
			label="Download JSON",
			data=json.dumps({"result": text, "inputs": user_prefs}, indent=2),
			file_name="crewai_stock_research.json",
			mime="application/json",
		)
