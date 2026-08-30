from __future__ import annotations

import csv
from typing import Iterable


def generate_price_plot(closes: Iterable[float], output_path: str) -> str:
    """Generate a minimal PNG plot using matplotlib if available.

    This function is intentionally lightweight and safe for research workflows.
    """
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:  # pragma: no cover - environment dependent
        raise RuntimeError("matplotlib is required for plot generation") from exc

    series = list(closes)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(series, color="steelblue", linewidth=2)
    ax.set_title("Price Series")
    ax.set_xlabel("Index")
    ax.set_ylabel("Price")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path


def generate_plotly_chart_html(closes: Iterable[float]) -> str:
    """Generate an embeddable Plotly HTML block for richer charting."""
    series = list(closes)
    values = ", ".join(str(value) for value in series)
    return f"""
    <div id="chart"></div>
    <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
    <script>
      const trace = {{
        x: Array.from({{ length: {len(series)} }}, (_, i) => i),
        y: [{values}],
        type: 'scatter',
        mode: 'lines',
        line: {{ color: 'steelblue', width: 2 }}
      }};
      Plotly.newPlot('chart', [trace], {{ margin: {{ t: 20, r: 20, b: 30, l: 40 }} }});
    </script>
    """


def export_prices_to_csv(closes: Iterable[float], output_path: str) -> str:
    """Export a close-price series to a CSV file."""
    series = list(closes)
    with open(output_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Close"])
        for value in series:
            writer.writerow([value])
    return output_path
