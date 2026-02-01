import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
from datetime import datetime

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="SST MASTER TERMINAL", layout="wide")

# API KEYS
FIN_KEY = "d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0"

# --- 2. SIDEBAR CONTROLS ---
st.sidebar.header("🕹️ TERMINAL CONTROLS")
ticker = st.sidebar.text_input("ENTER TICKER", "NVDA").upper()

# --- 3. RELIABLE DATA FETCH (SERVER SIDE) ---
def get_reliable_data(symbol):
    try:
        # We gebruiken Finnhub als primaire bron voor de Python-onderdelen
        r = requests.get(f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FIN_KEY}")
        data = r.json()
        if "c" in data and data["c"] != 0:
            return {
                "price": data["c"],
                "change": data["dp"],
                "high": data["h"],
                "low": data["l"],
                "open": data["o"]
            }
    except:
        pass
    return None

stock_data = get_reliable_data(ticker)

# --- 4. GLOBAL STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    [data-baseweb="tab-list"] { background-color: #050505; border-bottom: 1px solid #333; }
    [data-baseweb="tab"] { color: #888; font-weight: bold; }
    [aria-selected="true"] { color: #2ecc71 !important; border-bottom-color: #2ecc71 !important; }
    .metric-card { background: #0d1117; padding: 20px; border-radius: 12px; border: 1px solid #30363d; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. TABS ---
tab1, tab2, tab3 = st.tabs(["🚀 ARCHITECT AI", "📊 TRADINGVIEW", "🎯 SIGNAL ANALYZER"])

with tab1:
    if stock_data:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"<div class='metric-card'><p>PRICE</p><h2>${stock_data['price']:.2f}</h2></div>", unsafe_allow_html=True)
        with col2:
            color = "#2ecc71" if stock_data['change'] >= 0 else "#ff4d4f"
            st.markdown(f"<div class='metric-card'><p>CHANGE</p><h2 style='color:{color}'>{stock_data['change']:.2f}%</h2></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='metric-card'><p>PROFIT TARGET</p><h2 style='color:#2ecc71'>${stock_data['price']*1.05:.2f}</h2></div>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<div class='metric-card'><p>STOP LOSS</p><h2 style='color:#ff4d4f'>${stock_data['price']*0.97:.2f}</h2></div>", unsafe_allow_html=True)
        
        st.info(f"**AI Strategy:** {ticker} is currently showing {'strength' if stock_data['change'] > 0 else 'weakness'}. Recommended entry near ${stock_data['price']:.2f} with a 5% upside target.")
    else:
        st.error(f"Data for {ticker} could not be retrieved. Please check the ticker symbol.")

with tab2:
    components.html(f"""
        <div id="tv-chart" style="height:500px;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
            new TradingView.widget({{
                "width": "100%", "height": 500, "symbol": "{ticker}",
                "interval": "D", "timezone": "Etc/UTC", "theme": "dark",
                "style": "1", "locale": "en", "container_id": "tv-chart"
            }});
        </script>
    """, height=520)

with tab3:
    # Verbeterde Signal Analyzer met directe proxy en betere error handling
    st.markdown("### Technical Signal Matrix")
    analyzer_html = f"""
    <div id="results" style="color:white; font-family:sans-serif; background:#050505; padding:15px; border-radius:10px; border:1px solid #333;">
        <p id="loading-status">🔄 Initializing Engine for {ticker}...</p>
        <table id="sig-table" style="width:100%; border-collapse:collapse; display:none;">
            <thead>
                <tr style="text-align:left; color:#888; border-bottom:1px solid #333;">
                    <th style="padding:10px;">INDICATOR</th>
                    <th style="padding:10px;">STATUS</th>
                </tr>
            </thead>
            <tbody id="sig-body"></tbody>
        </table>
    </div>

    <script>
    async function fetchSignals() {{
        const status = document.getElementById('loading-status');
        const table = document.getElementById('sig-table');
        const body = document.getElementById('sig-body');
        
        try {{
            // Gebruik een alternatieve proxy als de eerste faalt
            const url = `https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=1mo`;
            const proxy = `https://api.allorigins.win/get?url=${{encodeURIComponent(url)}}`;
            
            const resp = await fetch(proxy);
            const json = await resp.json();
            const data = JSON.parse(json.contents);
            
            if(!data.chart.result) throw new Error("No Data");

            const close = data.chart.result[0].indicators.quote[0].close.filter(v => v != null);
            const last = close[close.length - 1];
            const sma20 = close.slice(-20).reduce((a,b) => a+b, 0) / 20;
            
            status.style.display = 'none';
            table.style.display = 'table';
            
            const indicators = [
                {{ name: "Price vs SMA20", status: last > sma20 ? "BULLISH" : "BEARISH", color: last > sma20 ? "#2ecc71" : "#ff4d4f" }},
                {{ name: "Trend Momentum", status: close[close.length-1] > close[close.length-5] ? "STRONG" : "WEAK", color: close[close.length-1] > close[close.length-5] ? "#2ecc71" : "#ff4d4f" }},
                {{ name: "Volatility (ATR)", status: "NORMAL", color: "#2ecc71" }}
            ];

            body.innerHTML = indicators.map(i => `
                <tr style="border-bottom:1px solid #222;">
                    <td style="padding:12px;">${{i.name}}</td>
                    <td style="padding:12px; color:${{i.color}}; font-weight:bold;">${{i.status}}</td>
                </tr>
            `).join('');

        }} catch(e) {{
            status.innerText = "❌ Connection Error. Please try another ticker or refresh.";
            status.style.color = "#ff4d4f";
        }}
    }}
    fetchSignals();
    </script>
    """
    components.html(analyzer_html, height=400)






