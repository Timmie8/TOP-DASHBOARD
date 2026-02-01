import streamlit as st
import streamlit.components.v1 as components

# 1. Pagina instellingen
st.set_page_config(page_title="SST AI TRADER", layout="wide")

# Verberg Streamlit decoratie
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding: 0px; background-color: #050608; }
    .stTabs [data-baseweb="tab-list"] { background-color: #0d1117; border-bottom: 1px solid #30363d; gap: 10px; }
    .stTabs [data-baseweb="tab"] { color: #8b949e; font-weight: bold; }
    .stTabs [aria-selected="true"] { color: #2ecc71 !important; border-bottom-color: #2ecc71 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- TOOL 1: AI SMART TERMINAL ---
tool_smart_terminal = """
<!DOCTYPE html>
<html>
<head>
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
            <input id="tickerInput" type="text" value="NVDA">
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
            const res = await fetch('https://finnhub.io/api/v1/quote?symbol='+ticker+'&token=d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0');
            const data = await res.json();
            document.getElementById('priceVal').innerText = '$' + data.c.toFixed(2);
            document.getElementById('targetVal').innerText = '$' + (data.c * 1.05).toFixed(2);
            document.getElementById('adviceVal').innerText = data.dp > 0 ? "STRONG BUY" : "HOLD";
            document.getElementById('signalCard').style.backgroundColor = data.dp > 0 ? "#065f46" : "#1e3a8a";
            new TradingView.widget({"autosize": true, "symbol": ticker, "interval": "D", "theme": "dark", "container_id": "chart_container", "hide_top_toolbar": true});
        }
        window.onload = fetchAIData;
    </script>
</body>
</html>
"""

# --- TOOL 2: RISK & TIER SYSTEM ---
tool_risk_tier = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: sans-serif; background: #0d1117; color: #c9d1d9; padding: 20px; }
        .container { max-width: 850px; margin: auto; background: #161b22; padding: 25px; border-radius: 12px; border: 1px solid #30363d; }
        .search-group { display: flex; gap: 10px; margin-bottom: 15px; }
        input { flex: 1; background: #0d1117; border: 1px solid #30363d; color: white; padding: 12px; border-radius: 6px; }
        button { border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-weight: bold; background: #1f6feb; color: white; }
        .card { position: relative; background: #0d1117; border: 2px solid #30363d; padding: 20px; border-radius: 10px; margin-bottom: 15px; border-left: 8px solid #39d353; }
        .tier-A { border-color: #39d353; }
        .tier-indicator { font-size: 1.8em; font-weight: 900; color: #39d353; }
        .levels { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-top: 15px; }
        .level { background: #161b22; padding: 10px; border-radius: 6px; text-align: center; border: 1px solid #30363d; }
    </style>
</head>
<body>
<div class="container">
    <div class="search-group">
        <input type="text" id="manualInput" placeholder="TICKER...">
        <button onclick="manualSearch()">AI ANALYSE</button>
    </div>
    <div id="display"></div>
</div>
<script>
async function manualSearch() {
    const ticker = document.getElementById("manualInput").value.toUpperCase();
    const res = await fetch('https://finnhub.io/api/v1/quote?symbol='+ticker+'&token=d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0');
    const data = await res.json();
    const html = `
        <div class="card">
            <div style="display:flex; justify-content:space-between;">
                <div><strong>${ticker}</strong><br><span style="background:green;padding:2px 5px;border-radius:4px;font-size:10px;">SWING</span></div>
                <div class="tier-indicator">A</div>
            </div>
            <div class="levels">
                <div class="level"><small>STOP</small><br>$${(data.c * 0.96).toFixed(2)}</div>
                <div class="level"><small>ENTRY</small><br>$${data.c.toFixed(2)}</div>
                <div class="level"><small>TARGET</small><br>$${(data.c * 1.08).toFixed(2)}</div>
            </div>
        </div>`;
    document.getElementById("display").insertAdjacentHTML('afterbegin', html);
}
</script>
</body>
</html>
"""

# --- RENDER TABS ---
tab1, tab2 = st.tabs(["🚀 AI SMART TERMINAL", "🛡️ RISK & TIER SYSTEM"])

with tab1:
    components.html(tool_smart_terminal, height=800, scrolling=True)

with tab2:
    components.html(tool_risk_tier, height=800, scrolling=True)


















