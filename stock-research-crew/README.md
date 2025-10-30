# CrewAI Stock Research Team

Three-agent CrewAI app for stock/ETF opportunity research (1-2 year horizon):
- Agent2 Researcher → finds candidates and evidence
- Agent1 Analyst → validates with fundamentals/technicals
- Agent3 Reviewer → approves or requests revisions

## Setup

```bash
python -m venv .venv
. .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

Create an optional `.env` from `.env.example` if you add API keys. Defaults use free tools.

## Run (GUI)

```bash
streamlit run app.py
```

## Run (CLI)

```bash
python main.py
```

## Docker

```bash
docker build -t stock-research-crew .
docker run --rm -p 8501:8501 stock-research-crew
```

Open http://localhost:8501

## Notes
- Data sources are free: yfinance, DuckDuckGo, basic scraping.
- Designed for positional uptrends (1-2 years), with simple technical filters.
