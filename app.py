import streamlit as st
import streamlit.components.v1 as components

# 1. Pagina instellingen
st.set_page_config(page_title="SST AI TRADER", layout="wide")

# Verberg Streamlit balken en zorg voor een donkere achtergrond
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding: 0px; background-color: #050608; }
    /* Styling voor de Tabs zelf */
    .stTabs [data-baseweb="tab-list"] { background-color: #0d1117; border-bottom: 1px solid #30363d; gap: 10px; }
    .stTabs [data-baseweb="tab"] { color: #8b949e; font-weight: bold; }
    .stTabs [aria-selected="true"] { color: #2ecc71 !important; border-bottom-color: #2ecc71 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DE TOOLS DEFINIËREN ---

# JOUW CODE 1: AI SMART TERMINAL (BLAUW)
tool_smart_terminal = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #050608; color: white; font-family: sans-serif; padding: 20px; }
        .data-strip { background: #11141b; border-radius: 1.5rem; border: 1px solid #1f2937; margin-bottom: 1rem; padding: 1.5rem; border-left: 8px solid #3b82f6; }
        .value { font-size: 2.5rem; font-weight: 900; }
        .label { color: #6b7280; text-transform: uppercase; font-size: 0.75rem; font-weight: 800; }
        #chart_box { height: 400px; border-radius: 1.5rem; overflow: hidden; border: 1px solid #1f2937; }
        input { background: #11141b; border: 2px solid #1f2937; padding: 15px; border-radius: 1rem; color: white; width: 60%; font-size: 1.5rem; }
        button { background: #2563eb; padding: 15px 30px; border-radius: 1rem; font-weight: 900; cursor: pointer; border: none; color: white; }
    </style>
</head>
<body>
    <div style="max-width: 600px; margin: auto;">
        <div style="display: flex; gap: 10px; margin-bottom: 20px;">
            <input id="tickerInput" type="text" value="NVDA" placeholder="TICKER">
            <button onclick="fetchAIData()">SCAN</button>
        </div>
        <div id="signalCard" style="background: #1e3a8a; padding: 20px; border-radius: 1.5rem; text-align: center; margin-bottom: 15px;"><p class="label">AI Decision</p><div id="adviceVal" style="font-size: 2rem; font-weight: 900;">--</div></div>
        <div class="data-strip"><p class="label">Market Price</p><div id="priceVal" class="value">--</div></div>
        <div class="data-strip" style="border-left-color: #10b981;"><p class="label">AI Profit Target</p><div id="targetVal" class="value" style="color: #10b981;">--</div></div>
        <div id="chart_box"><div id="chart_container" style="height: 100%;"></div></div>
    </div>
    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>
        async function fetchAIData() {
            const ticker = document.getElementById('tickerInput').value.toUpperCase();
            const response = await fetch(`https://finnhub.io/api/v1/quote?symbol=${ticker}&token=d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0`);
            const data = await response.json();
            document.getElementById('priceVal').innerText = '$' + data.c.toFixed(2);
            document.getElementById('targetVal').innerText = '$' + (data.c * 1.05).toFixed(2);
            document.getElementById('adviceVal').innerText = data.dp > 0 ? "STRONG BUY" : "HOLD";
            document.getElementById('signalCard').style.backgroundColor = data.dp > 0 ? "#065f46" : "#1e3a8a";
            new TradingView.widget({"autosize": true, "symbol": ticker, "interval": "D", "theme": "dark", "style": "1", "container_id": "chart_container", "hide_top_toolbar": true, "locale": "en"});
        }
        window.onload = fetchAIData;
    </script>
</body>
</html>
"""

# JOUW CODE 2: AI TRADER - DYNAMIC RISK & TIER (DONKERGRIJS)
tool_risk_tier = """
<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0d1117; color: #c9d1d9; padding: 20px; }
        .container { max-width: 850px; margin: auto; background: #161b22; padding: 25px; border-radius: 12px; border: 1px solid #30363d; }
        .controls { background: #21262d; padding: 20px; border-radius: 10px; border: 1px solid #30363d; margin-bottom: 20px; }
        .search-group { display: flex; gap: 10px; margin-bottom: 15px; }
        input { flex: 1; background: #0d1117; border: 1px solid #30363d; color: white; padding: 12px; border-radius: 6px; text-transform: uppercase; }
        button { border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-weight: bold; }
        .btn-blue { background: #1f6feb; color: white; }
        .btn-green { background: #238636; color: white; }
        .btn-outline { background: transparent; border: 1px solid #f85149; color: #f85149; }
        .card { position: relative; background: #0d1117; border: 2px solid #30363d; padding: 20px; border-radius: 10px; margin-bottom: 15px; transition: 0.3s; }
        .tier-A { border-color: #39d353 !important; border-left: 8px solid #39d353; }
        .tier-B { border-color: #58a6ff !important; border-left: 8px solid #58a6ff; }
        .tier-C { border-color: #d29922 !important; border-left: 8px solid #d29922; }
        .tier-D { border-color: #f85149 !important; border-left: 8px solid #f85149; }
        .header-flex { display: flex; justify-content: space-between; align-items: flex-start; }
        .tier-indicator { font-size: 1.8em; font-weight: 900; line-height: 1; }
        .status-badge { padding: 4px 10px; border-radius: 4px; font-size: 0.7em; font-weight: bold; text-transform: uppercase; display: inline-block; margin-top: 5px; }
        .bg-swing { background: #238636; color: white; }
        .bg-hold { background: #d29922; color: #0d1117; }
        .bg-noswing { background: #f85149; color: white; }
        .levels { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-top: 15px; }
        .level { background: #161b22; padding: 10px; border-radius: 6px; text-align: center; border: 1px solid #30363d; }
        .label-text { font-size: 0.7em; color: #8b949e; display: block; margin-bottom: 2px; }
        .price-text { font-weight: bold; font-family: monospace; font-size: 1.1em; display: block; }
        .tp { color: #39d353; } .sl { color: #f85149; }
        .news-box { margin-top: 15px; padding-top: 15px; border-top: 1px solid #30363d; font-size: 0.85em; }
        .ai-intel { background: rgba(88, 166, 255, 0.1); padding: 8px; border-radius: 4px; margin-top: 10px; border-left: 3px solid #58a6ff; font-style: italic; }
        .btn-delete { position: absolute; top: 10px; right: 10px; background: none; color: #8b949e; font-size: 22px; cursor: pointer; border: none; }
    </style>
</head>
<body>
<div class="container">
    <div class="controls">
        <div class="search-group">
            <input type="text" id="manualInput" placeholder="TICKER...">
            <button class="btn-blue" onclick="manualSearch()">AI ANALYSE</button>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <button class="btn-green" onclick="startAutoScan()">START AUTO-SCAN</button>
            <button class="btn-outline" onclick="document.getElementById('display').innerHTML=''">WIS ALLES</button>
        </div>
    </div>
    <div id="status" style="text-align: center; font-size: 0.8em; margin-bottom: 10px; color: #8b949e;"></div>
    <div id="display"></div>
</div>
<script>
const API_KEY = "d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0";
const TICKERS = ["AAPL", "TSLA", "NVDA", "AMZN", "MSFT", "AMD", "META", "GOOGL", "NFLX"];

async function analyzeTicker(ticker, isManual = false) {
    const display = document.getElementById("display");
    ticker = ticker.toUpperCase();
    try {
        const quoteRes = await fetch(`https://finnhub.io/api/v1/quote?symbol=${ticker}&token=${API_KEY}`);
        const data = await quoteRes.json();
        if (!data.c) return;
        const newsRes = await fetch(`https://finnhub.io/api/v1/company-news?symbol=${ticker}&from=2026-01-01&to=2026-01-26&token=${API_KEY}`);
        const news = await newsRes.json();
        const latestNews = news.length > 0 ? news[0] : null;
        const current = data.c, vola = ((data.h - data.l) / current) * 100;
        let dynStopPerc = Math.min(Math.max(vola * 1.5, 2.0), 6.0).toFixed(1);
        let dynTargetPerc = (dynStopPerc * 2.3).toFixed(1);
        let score = 50 + (data.dp * 6) - (vola * 2);
        score = Math.min(Math.max(score, 1), 99);
        let tier = "C", statusClass = "bg-hold", statusText = "HOLD", tierColor = "#d29922";
        if (score > 75 && vola < 4) { tier = "A"; statusClass = "bg-swing"; statusText = "SWING"; tierColor = "#39d353"; }
        else if (score > 60) { tier = "B"; statusClass = "bg-swing"; statusText = "SWING"; tierColor = "#58a6ff"; }
        else if (score < 40 || vola > 7) { tier = "D"; statusClass = "bg-noswing"; statusText = "NO SWING"; tierColor = "#f85149"; }
        const id = 'id-' + Date.now() + ticker;
        const html = `
            <div class="card tier-${tier}" id="${id}">
                <button class="btn-delete" onclick="document.getElementById('${id}').remove()">×</button>
                <div class="header-flex">
                    <div><strong>${ticker}</strong><br><span class="status-badge ${statusClass

















