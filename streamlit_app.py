from __future__ import annotations

from pathlib import Path

import streamlit as st

from elliott_wave_tool.analysis import ElliottWaveAnalyzer
from elliott_wave_tool.backtester import ElliottBacktester
from elliott_wave_tool.data_provider import fetch_live_market_data, load_prices_from_csv
from elliott_wave_tool.market_data import build_signal_summary
from elliott_wave_tool.plotting import export_prices_to_csv, generate_plotly_chart_html, generate_price_plot
from elliott_wave_tool.strategy import build_report, compare_symbols, optimize_strategy

st.set_page_config(page_title="Elliott Wave Trader", page_icon="📈", layout="wide")

st.title("Elliott Wave Trading Dashboard")
st.caption("Classical Elliott Wave-inspired technical analysis, strategy comparison, and chart review.")

with st.sidebar:
    st.header("Inputs")
    symbol = st.text_input("Symbol", value="AAPL")
    symbol_b = st.text_input("Compare symbol", value="MSFT")
    source = st.selectbox("Data source", ["manual", "live fallback", "csv upload"])
    period = st.selectbox("Period", ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y"], index=3)
    interval = st.selectbox("Interval", ["1d", "1wk", "1mo"], index=0)
    manual_prices = st.text_area("Manual prices", value="100,102,101,104,110,108,112,118,115,121,128,123,130")
    uploaded_file = st.file_uploader("CSV upload", type=["csv"])
    submit = st.button("Analyze", type="primary")


if submit:
    if source == "live fallback":
        closes = fetch_live_market_data(symbol, period=period, interval=interval)
    elif source == "csv upload" and uploaded_file is not None:
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        csv_path = upload_dir / uploaded_file.name
        csv_path.write_bytes(uploaded_file.getvalue())
        closes = load_prices_from_csv(str(csv_path))
    else:
        closes = [float(item.strip()) for item in manual_prices.split(",") if item.strip()]

    analysis = ElliottWaveAnalyzer(closes).analyze()
    summary = build_signal_summary(closes)
    backtest = ElliottBacktester(closes).run()
    strategies = optimize_strategy(closes)

    plot_dir = Path("static")
    plot_dir.mkdir(exist_ok=True)
    plot_path = plot_dir / "plot.png"
    generate_price_plot(closes, str(plot_path))
    plot_html = generate_plotly_chart_html(closes)
    export_path = plot_dir / "prices.csv"
    export_prices_to_csv(closes, str(export_path))

    col1, col2, col3 = st.columns(3)
    col1.metric("Trend", analysis["trend"].title())
    col2.metric("Phase", analysis["current_phase"].title())
    col3.metric("Confidence", f"{analysis['confidence']}%")

    col4, col5, col6 = st.columns(3)
    col4.metric("Support", f"{summary['support']:.2f}")
    col5.metric("Resistance", f"{summary['resistance']:.2f}")
    col6.metric("Return", f"{backtest['total_return']}%")

    compared = compare_symbols([
        {"symbol": symbol, "score": float(analysis["confidence"])},
        {"symbol": symbol_b, "score": float(analysis["confidence"]) * 0.96},
    ])

    st.subheader("Signal Summary")
    st.json(summary)

    st.subheader("Backtest")
    st.json(backtest)

    st.subheader("Strategy Comparison")
    st.dataframe(strategies, use_container_width=True)

    st.subheader("Multi-Symbol Comparison")
    st.dataframe(compared, use_container_width=True)

    st.subheader("Report")
    st.text(build_report(symbol, closes, analysis))

    st.subheader("Price Chart")
    st.image(str(plot_path), use_container_width=True)
    st.components.v1.html(plot_html, height=520, scrolling=True)

    st.download_button("Download CSV", data=export_path.read_bytes(), file_name="prices.csv", mime="text/csv")
else:
    st.info("Choose a data source and click Analyze to run the Elliott Wave dashboard.")
