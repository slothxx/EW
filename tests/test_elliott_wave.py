from elliott_wave_tool.analysis import ElliottWaveAnalyzer
from elliott_wave_tool.backtester import ElliottBacktester
from elliott_wave_tool.data_provider import fetch_live_market_data, fetch_market_data, load_prices_from_csv, aggregate_timeframe
from elliott_wave_tool.market_data import build_signal_summary
from elliott_wave_tool.plotting import generate_price_plot, generate_plotly_chart_html, export_prices_to_csv
from elliott_wave_tool.strategy import optimize_strategy


def test_detects_bullish_wave_structure():
    closes = [100, 102, 101, 104, 110, 108, 112, 118, 115, 121, 128, 123, 130]

    result = ElliottWaveAnalyzer(closes).analyze()

    assert result["trend"] == "bullish"
    assert result["current_phase"] in {"impulse", "correction", "consolidation"}
    assert result["confidence"] >= 0
    assert result["confidence"] <= 100
    assert "wave_structure" in result
    assert isinstance(result["wave_structure"], list)


def test_detects_bearish_wave_structure():
    closes = [130, 128, 123, 121, 118, 112, 108, 110, 104, 101, 102, 100]

    result = ElliottWaveAnalyzer(closes).analyze()

    assert result["trend"] == "bearish"
    assert result["confidence"] >= 0
    assert result["confidence"] <= 100


def test_backtester_generates_metrics_for_bullish_series():
    closes = [100, 101, 103, 110, 115, 121, 128, 134, 141]
    result = ElliottBacktester(closes).run()

    assert "equity_curve" in result
    assert "final_equity" in result
    assert "total_return" in result
    assert "trades" in result
    assert result["final_equity"] >= 0


def test_signal_summary_builds_expected_keys():
    summary = build_signal_summary([100, 102, 101, 104, 110, 108, 112, 118, 115, 121, 128, 123, 130])

    assert summary["trend"] in {"bullish", "bearish", "neutral"}
    assert summary["confidence"] >= 0
    assert summary["confidence"] <= 100
    assert "phase" in summary
    assert "wave_structure" in summary


def test_strategy_optimizer_returns_ranked_configs():
    closes = [100, 101, 103, 110, 115, 121, 128, 134, 141]
    result = optimize_strategy(closes)

    assert isinstance(result, list)
    assert len(result) >= 1
    assert "config" in result[0]
    assert "score" in result[0]


def test_plot_generator_creates_png_file(tmp_path):
    output = tmp_path / "sample_plot.png"
    generate_price_plot([100, 102, 101, 104, 110, 108, 112, 118], str(output))

    assert output.exists()
    assert output.stat().st_size > 0


def test_load_prices_from_csv_parses_close_column(tmp_path):
    csv_path = tmp_path / "prices.csv"
    csv_path.write_text("Date,Close\n2024-01-01,100\n2024-01-02,102\n2024-01-03,101\n")

    closes = load_prices_from_csv(str(csv_path))

    assert closes == [100.0, 102.0, 101.0]


def test_aggregate_timeframe_collapses_series():
    closes = [100, 102, 101, 104, 110, 108]
    result = aggregate_timeframe(closes, "5m")

    assert isinstance(result, list)
    assert len(result) >= 1
    assert result[0] >= 0


def test_fetch_market_data_works_without_network():
    data = fetch_market_data("FAKE", periods=8)

    assert isinstance(data, list)
    assert len(data) >= 5
    assert all(isinstance(value, float) for value in data)


def test_fetch_live_market_data_falls_back_cleanly():
    data = fetch_live_market_data("FAKE", period="1mo")

    assert isinstance(data, list)
    assert len(data) >= 5
    assert all(isinstance(value, float) for value in data)


def test_generate_plotly_chart_html_contains_trace():
    html = generate_plotly_chart_html([100, 102, 101, 104, 110])

    assert "plotly" in html.lower()
    assert "trace" in html.lower()


def test_export_prices_to_csv_writes_valid_file(tmp_path):
    path = tmp_path / "export.csv"
    export_prices_to_csv([100, 102, 101], str(path))

    assert path.exists()
    assert path.stat().st_size > 0
