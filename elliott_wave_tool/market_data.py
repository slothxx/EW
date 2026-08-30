from __future__ import annotations

from typing import Dict, List

from .analysis import ElliottWaveAnalyzer


def build_signal_summary(closes: List[float]) -> Dict[str, object]:
    analyzer = ElliottWaveAnalyzer(closes)
    analysis = analyzer.analyze()
    return {
        "trend": analysis["trend"],
        "confidence": analysis["confidence"],
        "phase": analysis["current_phase"],
        "wave_structure": analysis["wave_structure"],
        "price_change": analysis["price_change"],
        "support": analysis["support"],
        "resistance": analysis["resistance"],
        "signal": analysis["signals"]["primary"],
    }
