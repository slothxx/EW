from __future__ import annotations

from typing import Any, Dict, List


class ElliottWaveAnalyzer:
    """A compact Elliott Wave-inspired technical analysis tool.

    This heuristic model is designed for educational and research use. It
    identifies trend direction, wave labeling, phase state, and a confidence
    score without requiring external packages.
    """

    def __init__(self, closes: List[float]):
        if len(closes) < 5:
            raise ValueError("At least 5 price points are required for analysis.")
        self.closes = [float(value) for value in closes]

    def _price_change(self) -> float:
        return self.closes[-1] - self.closes[0]

    def _direction(self) -> str:
        change = self._price_change()
        if change > 0:
            return "bullish"
        if change < 0:
            return "bearish"
        return "neutral"

    def _segment_trend_strength(self) -> float:
        if len(self.closes) < 2:
            return 0.0
        changes = [self.closes[i] - self.closes[i - 1] for i in range(1, len(self.closes))]
        average_abs_move = sum(abs(change) for change in changes) / len(changes)
        start_price = abs(self.closes[0]) or 1.0
        return (average_abs_move / start_price) * 100.0

    def _phase(self, direction: str, strength: float) -> str:
        if direction == "neutral":
            return "consolidation"
        if strength >= 2.0:
            return "impulse"
        if strength >= 0.8:
            return "correction"
        return "consolidation"

    def _wave_structure(self, direction: str) -> List[str]:
        if direction == "bullish":
            return ["1", "2", "3", "4", "5"]
        if direction == "bearish":
            return ["A", "B", "C"]
        return ["consolidation"]

    def _confidence(self, direction: str, strength: float) -> float:
        direction_score = 50.0
        if direction == "bullish":
            direction_score += min(30.0, strength * 12.0)
        elif direction == "bearish":
            direction_score += min(30.0, strength * 12.0)
        else:
            direction_score -= 20.0

        consistency = 0.0
        changes = [self.closes[i] - self.closes[i - 1] for i in range(1, len(self.closes))]
        if changes:
            positive_moves = sum(1 for value in changes if value > 0)
            negative_moves = sum(1 for value in changes if value < 0)
            if direction == "bullish":
                consistency = (positive_moves / len(changes)) * 20.0
            elif direction == "bearish":
                consistency = (negative_moves / len(changes)) * 20.0
            else:
                consistency = 0.0

        score = max(0.0, min(100.0, direction_score + consistency))
        return round(score, 2)

    def _fibonacci_levels(self) -> Dict[str, float]:
        start = min(self.closes)
        end = max(self.closes)
        range_value = end - start
        return {
            "0%": start,
            "23.6%": end - (range_value * 0.236),
            "38.2%": end - (range_value * 0.382),
            "50%": start + (range_value * 0.5),
            "61.8%": end - (range_value * 0.618),
            "100%": end,
        }

    def analyze(self) -> Dict[str, Any]:
        trend = self._direction()
        strength = self._segment_trend_strength()
        phase = self._phase(trend, strength)
        confidence = self._confidence(trend, strength)

        return {
            "trend": trend,
            "current_phase": phase,
            "confidence": confidence,
            "wave_structure": self._wave_structure(trend),
            "price_change": round(self._price_change(), 4),
            "volatility_strength": round(strength, 4),
            "fibonacci_levels": self._fibonacci_levels(),
            "support": round(min(self.closes), 4),
            "resistance": round(max(self.closes), 4),
            "signals": {
                "primary": f"{trend.upper()} trend with {phase} behavior",
                "secondary": "Classic Elliott Wave heuristics suggest directional momentum and phase alignment based on trend structure.",
            },
        }
