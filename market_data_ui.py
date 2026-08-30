#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from elliott_wave_tool.analysis import ElliottWaveAnalyzer
from elliott_wave_tool.data_provider import aggregate_timeframe, fetch_market_data, load_prices_from_csv
from elliott_wave_tool.market_data import build_signal_summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Market data research CLI")
    parser.add_argument("--symbol", default="FAKE", help="Ticker symbol or data source label")
    parser.add_argument("--csv", help="Optional CSV file containing Close values")
    parser.add_argument("--periods", type=int, default=30, help="Number of offline periods to generate")
    parser.add_argument("--timeframe", default="5m", help="Timeframe label for aggregation")
    args = parser.parse_args()

    if args.csv:
        closes = load_prices_from_csv(args.csv)
    else:
        closes = fetch_market_data(args.symbol, periods=args.periods)

    aggregated = aggregate_timeframe(closes, args.timeframe)
    analysis = ElliottWaveAnalyzer(closes).analyze()
    summary = build_signal_summary(closes)

    payload = {
        "symbol": args.symbol,
        "timeframe": args.timeframe,
        "raw_close_series": closes,
        "aggregated_series": aggregated,
        "signal_summary": summary,
        "analysis": analysis,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
