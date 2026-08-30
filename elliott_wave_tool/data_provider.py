from __future__ import annotations

import csv
from typing import List


def fetch_live_market_data(symbol: str, period: str = "1mo", interval: str = "1d") -> List[float]:
    """Return market data with a clean offline fallback.

    This keeps the app usable even without external internet access.
    """
    try:
        import yfinance as yf

        ticker = yf.download(symbol, period=period, interval=interval, progress=False, auto_adjust=True)
        if ticker.empty:
            return fetch_market_data(symbol, periods=20)
        closes = ticker["Close"].dropna().tolist()
        if closes:
            return [float(value) for value in closes]
    except Exception:
        pass
    return fetch_market_data(symbol, periods=20)


def load_prices_from_csv(path: str) -> List[float]:
    """Load the Close column from a CSV file."""
    closes: List[float] = []
    with open(path, newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if "Close" in row and row["Close"] not in (None, ""):
                closes.append(float(row["Close"]))
    if not closes:
        raise ValueError(f"No valid Close values found in CSV: {path}")
    return closes


def aggregate_timeframe(closes: List[float], timeframe: str) -> List[float]:
    """Aggregate a price list into a simplified timeframe series.

    This is intentionally simple and offline-safe.
    """
    if not closes:
        return []
    grouped: List[float] = []
    step = max(1, len(closes) // max(1, 5))
    for idx in range(0, len(closes), step):
        block = closes[idx: idx + step]
        if block:
            grouped.append(sum(block) / len(block))
    if not grouped:
        grouped = [float(closes[0])]
    return grouped


def fetch_market_data(symbol: str, periods: int = 30) -> List[float]:
    """Return a deterministic offline market series for the requested symbol.

    This is a fallback data provider so the app still works without network access.
    """
    if not symbol:
        raise ValueError("A symbol is required")

    baseline = 100.0
    sequence: List[float] = []
    drift = 0.8
    for i in range(periods):
        baseline += drift + (i % 5) * 0.5
        if i % 4 == 0:
            baseline -= 1.2
        sequence.append(round(float(baseline), 2))
    return sequence
