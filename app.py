import streamlit as st
import streamlit.components.v1 as components
import requests
import json

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="SST MASTER TERMINAL", layout="wide")

st.sidebar.header("🕹️ TERMINAL CONTROLS")
ticker = st.sidebar.text_input("SET GLOBAL TICKER", "NVDA").upper()
# TradingView needs a prefix for some tickers
tv_ticker = f"NASDAQ:{ticker}" if ":" not in ticker else ticker

# --- 2. DATA ENGINE (Python Fetch) ---
def fetch_terminal_data(symbol):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1y"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=5)
        return r.json()
    except:
        return None

data_json = fetch_terminal_data(ticker)

# --- 3. GLOBAL STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    [data-baseweb="tab-list"] { background-color: #050505; border-bottom: 1px solid #333; }
    [data-baseweb="tab"] { height: 50px; background-color: #0d1117; color: #8b949e; border-radius: 8px 8px 0 0; }
    [aria-selected="true"] { background-color: #2ecc71 !important; color: black !important; font-weight: bold; }
    iframe { border: none !important; width: 100% !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. THE 6 TABS ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🚀 ARCHITECT AI", "📊 MARKET METERS", "🛡️ RISK SCANNER", 
    "🔍 DEEP SCANNER", "⚡ PRO DASHBOARD", "🎯 SIGNAL ANALYZER"
])

# --- TAB 1: ARCHITECT AI ---
with tab1:
    if data_json:
        close_prices = data_json['chart']['result'][0]['indicators']['quote'][0]['close']
        last_p = [x for x in close_prices if x is not None][-1]
        st.markdown(f"""
        <div style="background:#0d1117; padding:25px; border-radius:15px; border:1px solid #30363d;">
            <h2 style="color:#2ecc71; margin-bottom:10px;">SST ARCHITECT AI | {ticker}</h2>
            <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:15px;">
                <div style="background:#161b22; padding:15px; border-radius:10px; text-align:center; border:1px solid #333;">
                    <p style="color:#888; font-size:12px;">AI ENTRY PRICE</p>
                    <h2 style="margin:5px 0;">${last_p:.2f}</h2>
                </div>
                <div style="background:#161b22; padding:15px; border-radius:10px; text-align:center; border:1px solid #333;">
                    <p style="color:#2ecc71; font-size:12px;">PROFIT TARGET</p>
                    <h2 style="margin:5px 0;">${last_p * 1.05:.2f}</h2>
                </div>
                <div style="background:#161b22; padding:15px; border-radius:10px; text-align:center; border:1px solid #333;">
                    <p style="color:#f85149; font-size:12px;">STOP LOSS</p>
                    <h2 style="margin:5px 0;">${last_p * 0.97:.2f}</h2>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("Waiting for data...")

# --- TAB 2: MARKET METERS (Technical Gauges) ---
with tab2:
    components.html(f"""
        <div style="height:450px;">
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
            {{ "interval": "1D", "width": "100%", "height": "100%", "symbol": "{tv_ticker}", "showIntervalTabs": true, "colorTheme": "dark", "locale": "en" }}
            </script>
        </div>
    """, height=470)

# --- TAB 3: RISK SCANNER ---
with tab3:
    components.html(f"""
        <div style="height:450px;">
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-profile.js" async>
            {{ "symbol": "{tv_ticker}", "width": "100%", "height": "100%", "colorTheme": "dark", "locale": "en" }}
            </script>
        </div>
    """, height=470)

# --- TAB 4: DEEP SCANNER ---
with tab4:
    components.html(f"""
        <div id="tv_chart" style="height:500px;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
            new TradingView.widget({{
                "width": "100%", "height": 500, "symbol": "{tv_ticker}", "interval": "D",
                "theme": "dark", "style": "1", "locale": "en", "container_id": "tv_chart"
            }});
        </script>
    """, height=520)

# --- TAB 5 & 6 (Keep your working logic) ---
# ... (Hier de code van de vorige stap implementeren)















