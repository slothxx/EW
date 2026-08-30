from __future__ import annotations

from typing import Dict, List


def optimize_strategy(closes: List[float]) -> List[Dict[str, float | str | int]]:
    """Evaluate a few parameter set candidates for a simple strategy search."""
    candidate_configs = [
        {"name": "trend_following", "lookback": 3, "threshold": 0.6},
        {"name": "balanced", "lookback": 5, "threshold": 1.0},
        {"name": "momentum", "lookback": 7, "threshold": 1.4},
    ]

    results: List[Dict[str, float | str | int]] = []
    for config in candidate_configs:
        lookback = config["lookback"]
        threshold = config["threshold"]
        if len(closes) < lookback + 1:
            score = 0.0
        else:
            changes = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
            recent = changes[-lookback:]
            avg_move = sum(abs(value) for value in recent) / len(recent)
            score = max(0.0, min(100.0, (avg_move / max(abs(closes[-1]), 1.0)) * 100.0 - threshold * 20.0))

        results.append({
            "config": config,
            "score": round(float(score), 2),
        })

    return sorted(results, key=lambda item: item["score"], reverse=True)


def compare_symbols(symbol_results: List[Dict[str, object]]) -> List[Dict[str, object]]:
    """Rank and compare multiple symbol analyses."""
    return sorted(symbol_results, key=lambda item: float(item["score"]), reverse=True)


def build_report(symbol: str, closes: List[float], result: Dict[str, object]) -> str:
    """Build a small human-readable strategy report."""
    return (
        f"Symbol: {symbol}\n"
        f"Samples: {len(closes)}\n"
        f"Trend: {result.get('trend', 'unknown')}\n"
        f"Confidence: {result.get('confidence', 0)}%\n"
        f"Phase: {result.get('current_phase', 'unknown')}\n"
    )
