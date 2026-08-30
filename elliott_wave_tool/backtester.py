from __future__ import annotations

from typing import Dict, List


class ElliottBacktester:
    """A simple backtest engine for a position-taking Elliott-style signal."""

    def __init__(self, closes: List[float], initial_capital: float = 10000.0):
        self.closes = [float(value) for value in closes]
        self.initial_capital = float(initial_capital)

    def run(self) -> Dict[str, float | List[float] | int]:
        equity = self.initial_capital
        equity_curve = [equity]
        trades = 0
        position = 0

        for index in range(1, len(self.closes)):
            previous = self.closes[index - 1]
            current = self.closes[index]
            delta = current - previous

            if delta > 0 and position <= 0:
                position = 1
                trades += 1
            elif delta < 0 and position >= 0:
                position = -1
                trades += 1

            equity *= 1.0 + (position * delta / max(previous, 1e-8))
            equity_curve.append(equity)

        total_return = ((equity / self.initial_capital) - 1.0) * 100.0

        return {
            "initial_capital": self.initial_capital,
            "final_equity": round(equity, 2),
            "total_return": round(total_return, 2),
            "trades": trades,
            "equity_curve": [round(value, 2) for value in equity_curve],
        }
