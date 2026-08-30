from __future__ import annotations

import json
from pathlib import Path

from flask import Flask, render_template_string, request

from elliott_wave_tool.analysis import ElliottWaveAnalyzer
from elliott_wave_tool.backtester import ElliottBacktester
from elliott_wave_tool.data_provider import fetch_live_market_data, load_prices_from_csv
from elliott_wave_tool.market_data import build_signal_summary
from elliott_wave_tool.plotting import export_prices_to_csv, generate_plotly_chart_html, generate_price_plot
from elliott_wave_tool.strategy import optimize_strategy

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html>
  <head>
    <title>Elliott Wave Dashboard</title>
    <style>
      body { font-family: Arial, sans-serif; margin: 2rem; background: #111827; color: #f3f4f6; }
      .container { max-width: 1100px; margin: auto; }
      .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; }
      .card { background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 10px; }
      form { display: flex; gap: 1rem; flex-wrap: wrap; }
      input, select { flex: 1; min-width: 180px; padding: 0.75rem; }
      button { padding: 0.75rem 1.25rem; }
      pre { background: rgba(255,255,255,0.06); padding: 1rem; border-radius: 8px; overflow: auto; }
      img { max-width: 100%; border-radius: 8px; margin-top: 1rem; }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Elliott Wave Dashboard</h1>
      <form method="post" enctype="multipart/form-data">
        <input name="prices" value="{{ default_prices }}" placeholder="100,102,101,104,110,108,112" />
        <select name="source">
          <option value="manual">Manual prices</option>
          <option value="live">Live fallback data</option>
          <option value="csv">CSV upload</option>
        </select>
        <input type="file" name="csv_file" accept=".csv" />
        <button type="submit">Analyze</button>
      </form>
      {% if analysis %}
        <div class="grid">
          <div class="card">
            <h2>Signal Summary</h2>
            <pre>{{ signal_summary | tojson(indent=2) }}</pre>
          </div>
          <div class="card">
            <h2>Backtest</h2>
            <pre>{{ backtest | tojson(indent=2) }}</pre>
          </div>
          <div class="card">
            <h2>Strategy Optimization</h2>
            <pre>{{ strategy | tojson(indent=2) }}</pre>
          </div>
        </div>
        {% if plot_path %}
          <h2>Price Plot</h2>
          <img src="{{ plot_path }}" alt="Price plot" />
          <div>{{ plotly_html | safe }}</div>
        {% endif %}
        <div class="card">
          <h2>Exports</h2>
          <a href="/download/csv" style="color:white;">Download CSV</a>
        </div>
      {% endif %}
    </div>
  </body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    default_prices = "100,102,101,104,110,108,112,118,115,121,128,123,130"
    if request.method == "POST":
        prices = request.form.get("prices", default_prices)
        source = request.form.get("source", "manual")
        csv_file = request.files.get("csv_file")

        if source == "live":
            closes = fetch_live_market_data("AAPL", period="1mo")
        elif source == "csv" and csv_file and csv_file.filename:
            upload_path = Path("uploads")
            upload_path.mkdir(exist_ok=True)
            csv_path = upload_path / csv_file.filename
            csv_file.save(str(csv_path))
            closes = load_prices_from_csv(str(csv_path))
        else:
            closes = [float(item.strip()) for item in prices.split(",") if item.strip()]

        analysis = ElliottWaveAnalyzer(closes).analyze()
        signal_summary = build_signal_summary(closes)
        strategy = optimize_strategy(closes)
        backtest = ElliottBacktester(closes).run()

        plot_dir = Path("static")
        plot_dir.mkdir(exist_ok=True)
        plot_path = plot_dir / "plot.png"
        generate_price_plot(closes, str(plot_path))
        plotly_html = generate_plotly_chart_html(closes)
        export_prices_to_csv(closes, str(plot_dir / "prices.csv"))

        return render_template_string(
            HTML_TEMPLATE,
            default_prices=prices,
            analysis=json.dumps(analysis, indent=2),
            signal_summary=signal_summary,
            backtest=backtest,
            strategy=strategy,
            plot_path="/static/plot.png",
            plotly_html=plotly_html,
        )

    return render_template_string(HTML_TEMPLATE, default_prices=default_prices, analysis=None, signal_summary=None, backtest=None, strategy=None, plot_path=None, plotly_html=None)


@app.route("/download/csv")
def download_csv():
    csv_path = Path("static") / "prices.csv"
    if not csv_path.exists():
        return "No CSV export available yet."
    return csv_path.read_bytes(), 200, {"Content-Type": "text/csv", "Content-Disposition": "attachment; filename=prices.csv"}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
