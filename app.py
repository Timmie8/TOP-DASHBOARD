import streamlit as st
import streamlit.components.v1 as components

# 1. Pagina instellingen voor een 'Full App' gevoel
st.set_page_config(page_title="AI SMART TERMINAL", layout="wide")

# Verberg Streamlit decoratie
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding: 0px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Jouw volledige HTML code in een string
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #050608; font-family: sans-serif; color: white; padding: 20px; }
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

        <div id="signalCard" style="background: #1e3a8a; padding: 20px; border-radius: 1.5rem; text-align: center; margin-bottom: 15px;">
            <p class="label">AI Decision</p>
            <div id="adviceVal" style="font-size: 2rem; font-weight: 900;">--</div>
        </div>

        <div class="data-strip">
            <p class="label">Market Price</p>
            <div id="priceVal" class="value">--</div>
        </div>

        <div class="data-strip" style="border-left-color: #10b981;">
            <p class="label">AI Profit Target</p>
            <div id="targetVal" class="value" style="color: #10b981;">--</div>
        </div>

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

            new TradingView.widget({
                "autosize": true, "symbol": ticker, "interval": "D", "theme": "dark", "style": "1", "container_id": "chart_container", "hide_top_toolbar": true, "locale": "en"
            });
        }
        window.onload = fetchAIData;
    </script>
</body>
</html>
"""

# 3. Rendert de HTML
components.html(html_code, height=1000, scrolling=True)
















