#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from elliott_wave_tool.analysis import ElliottWaveAnalyzer


def parse_prices(raw_prices: str):
    try:
        return [float(item) for item in raw_prices.split(",") if item.strip()]
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"Invalid price list: {raw_prices!r}") from exc


def main() -> None:
    parser = argparse.ArgumentParser(description="Elliott Wave-inspired technical analysis tool")
    parser.add_argument(
        "--prices",
        type=parse_prices,
        required=True,
        help="Comma-separated price list, e.g. 100,102,101,104,110,108",
    )
    args = parser.parse_args()

    result = ElliottWaveAnalyzer(args.prices).analyze()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
