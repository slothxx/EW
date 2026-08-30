#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from typing import List

from elliott_wave_tool.analysis import ElliottWaveAnalyzer
from elliott_wave_tool.backtester import ElliottBacktester
from elliott_wave_tool.market_data import build_signal_summary


def parse_prices(raw_prices: str) -> List[float]:
    return [float(item.strip()) for item in raw_prices.split(",") if item.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Elliott Wave trading dashboard")
    parser.add_argument("--prices", required=True, help="Comma-separated close prices")
    args = parser.parse_args()

    closes = parse_prices(args.prices)
    summary = build_signal_summary(closes)
    analysis = ElliottWaveAnalyzer(closes).analyze()
    backtest = ElliottBacktester(closes).run()

    dashboard = {
        "signal_summary": summary,
        "analysis": analysis,
        "backtest": backtest,
    }

    print(json.dumps(dashboard, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
