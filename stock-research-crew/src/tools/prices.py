import datetime as dt
from typing import List, Optional

import pandas as pd
import yfinance as yf


def fetch_price_history(ticker: str, period: str = "5y", interval: str = "1d") -> pd.DataFrame:
	"""Fetch historical OHLCV price data using yfinance.

	Returns a DataFrame with columns: Open, High, Low, Close, Adj Close, Volume.
	"""
	data = yf.download(ticker, period=period, interval=interval, auto_adjust=False, progress=False)
	if not isinstance(data, pd.DataFrame) or data.empty:
		raise ValueError(f"No price data for {ticker}")
	data.index = pd.to_datetime(data.index)
	return data


def compute_trend_metrics(prices: pd.DataFrame) -> dict:
	"""Compute simple trend metrics for positional trading horizon (1-2 years)."""
	close = prices["Adj Close"].dropna() if "Adj Close" in prices else prices["Close"].dropna()
	result = {}
	for window in [50, 100, 200]:
		ma = close.rolling(window).mean()
		result[f"ma_{window}"] = float(ma.iloc[-1]) if len(ma) else None
		result[f"above_ma_{window}"] = bool(close.iloc[-1] > ma.iloc[-1]) if len(ma) else None
	
	# 52-week metrics
	last_252 = close.tail(252)
	if len(last_252):
		result["wk52_high"] = float(last_252.max())
		result["wk52_low"] = float(last_252.min())
		result["off_high_pct"] = float((close.iloc[-1] / last_252.max() - 1) * 100)
		result["from_low_pct"] = float((close.iloc[-1] / last_252.min() - 1) * 100)
	
	# Recent momentum
	for lookback in [21, 63, 126, 252]:
		if len(close) >= lookback + 1:
			result[f"ret_{lookback}d_pct"] = float((close.iloc[-1] / close.iloc[-lookback-1] - 1) * 100)
	
	return result


def simple_technical_flags(prices: pd.DataFrame) -> List[str]:
	"""Return a list of simple bullish flags for positional uptrend bias."""
	flags: List[str] = []
	metrics = compute_trend_metrics(prices)
	if metrics.get("above_ma_200") and metrics.get("above_ma_100"):
		flags.append("Price above 100/200 DMA")
	if metrics.get("ret_126d_pct", 0) > 10:
		flags.append("6-month positive momentum > 10%")
	if metrics.get("off_high_pct", 0) > -15:
		flags.append("Within 15% of 52-week high")
	return flags
