# Elliott Wave Trading Tool

This project is a technical analysis and trading research application inspired by classical Elliott Wave theory. It combines trend detection, Fibonacci levels, simple backtesting, strategy scoring, chart generation, and a web dashboard so you can evaluate directional signals over price series data in a realistic workflow.

## What it does

- Detects bullish, bearish, or neutral trend direction
- Labels wave structure using an Elliott-inspired heuristic
- Identifies impulse, correction, or consolidation conditions
- Scores signal confidence using trend strength and momentum consistency
- Includes Fibonacci retracement levels for the active price range
- Runs a simple direction-based backtest on the price series
- Optimizes a few candidate strategy configurations
- Generates PNG price plots for chart review
- Supports offline market-data generation and CSV imports
- Includes a local web dashboard for interactive analysis

## Quick start

### Basic signal analysis

```bash
python3 app.py --prices 100,102,101,104,110,108,112,118,115,121,128,123,130
```

### Dashboard summary with backtest

```bash
python3 trading_dashboard.py --prices 100,102,101,104,110,108,112,118,115,121,128,123,130
```

### Offline market-data research

```bash
python3 market_data_ui.py --symbol AAPL --periods 30 --timeframe 5m
```

### CSV import

```bash
python3 market_data_ui.py --csv data/prices.csv --timeframe 1d
```

### Start the web dashboard

```bash
python3 web_app.py
```

Then open http://localhost:5000 in a browser.

## Example output

```json
{
  "signal_summary": {
    "phase": "impulse",
    "price_change": 30.0,
    "resistance": 130.0,
    "signal": "BULLISH trend with impulse behavior",
    "support": 100.0,
    "trend": "bullish",
    "wave_structure": ["1", "2", "3", "4", "5"],
    "confidence": 88.24
  },
  "analysis": {
    "confidence": 88.24,
    "current_phase": "impulse",
    "fibonacci_levels": {
      "0%": 100.0,
      "23.6%": 104.98,
      "38.2%": 107.86,
      "50%": 110.0,
      "61.8%": 112.14,
      "100%": 130.0
    },
    "trend": "bullish",
    "wave_structure": ["1", "2", "3", "4", "5"]
  },
  "backtest": {
    "initial_capital": 10000.0,
    "final_equity": 11250.0,
    "total_return": 12.5,
    "trades": 5,
    "equity_curve": [10000.0, 10100.0, 10250.0, ...]
  }
}
```

## Notes

This project is designed for research, prototyping, and learning. It is not a financial advisor, it does not execute trades, and it should not be treated as a guaranteed or production-ready trading system.
