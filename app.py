import streamlit as st
import streamlit.components.v1 as components
import requests

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="SST MASTER TERMINAL", layout="wide")

# API KEYS
FIN_KEY = "d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0"

# --- 2. SIDEBAR & TICKER ---
st.sidebar.header("🕹️ TERMINAL CONTROLS")
user_input = st.sidebar.text_input("ENTER TICKER", "NVDA").upper()
clean_ticker = user_input.split(':')[-1]
# Voor TradingView widgets gebruiken we vaak de beursnaam erbij
tv_ticker = f"NASDAQ:{clean_ticker}" 

# --- 3. SERVER-SIDE DATA (Voor Tab 1) ---
def get_price(symbol):
    try:
        r = requests.get(f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FIN_KEY}")
        return r.json().get('c', 0)
    except: return 0

current_price = get_price(clean_ticker)

# --- 4. GLOBAL CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    [data-baseweb="tab-list"] { background-color: #050505; border-bottom: 1px solid #333; }
    [data-baseweb="tab"] { color: #888; font-weight: bold; height: 50px; }
    [aria-selected="true"] { color: #2ecc71 !important; border-bottom-color: #2ecc71 !important; }
    .metric-box { background: #0d1117; padding: 20px; border-radius: 12px; border: 1px solid #333; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. TABS ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🚀 ARCHITECT AI", 
    "📊 MARKET METERS", 
    "🛡️ RISK SCANNER", 
    "🔍 DEEP SCANNER", 
    "⚡ PRO DASHBOARD",
    "🎯 SIGNAL ANALYZER"
])

# --- TAB 1: ARCHITECT AI (Server-side) ---
with tab1:
    if current_price > 0:
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='metric-box'><p>LIVE PRICE</p><h2>${current_price:.2f}</h2></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='metric-box'><p>PROFIT TARGET</p><h2 style='color:#2ecc71'>${current_price*1.07:.2f}</h2></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='metric-box'><p>STOP LOSS</p><h2 style='color:#ff4d4f'>${current_price*0.96:.2f}</h2></div>", unsafe_allow_html=True)
    else:
        st.error("Connection to Finnhub failed. Check your API key or Ticker.")

# --- TAB 2: MARKET METERS (Technical Gauge) ---
with tab2:
    components.html(f"""
        <div style="height:500px; background:#050505;">
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
            {{ "interval": "1D", "width": "100%", "height": "100%", "symbol": "{tv_ticker}", "showIntervalTabs": true, "colorTheme": "dark", "locale": "en" }}
            </script>
        </div>
    """, height=520)

# --- TAB 3: RISK SCANNER (Fundamental & Ratings) ---
with tab3:
    components.html(f"""
        <div style="height:500px;">
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-profile.js" async>
            {{ "symbol": "{tv_ticker}", "width": "100%", "height": "100%", "colorTheme": "dark", "isTransparent": false, "locale": "en" }}
            </script>
        </div>
    """, height=520)

# --- TAB 4: DEEP SCANNER (Charts & Indicators) ---
with tab4:
    components.html(f"""
        <div id="tradingview_deep" style="height:500px;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({{
          "width": "100%", "height": 500, "symbol": "{tv_ticker}",
          "interval": "D", "timezone": "Etc/UTC", "theme": "dark",
          "style": "1", "locale": "en", "toolbar_bg": "#f1f3f6",
          "enable_publishing": false, "hide_side_toolbar": false, "container_id": "tradingview_deep"
        }});
        </script>
    """, height=520)

# --- TAB 5: PRO DASHBOARD (Market Overview) ---
with tab5:
    components.html(f"""
        <div style="height:500px;">
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-hotlists.js" async>
            {{ "colorTheme": "dark", "dateRange": "12M", "showChart": true, "locale": "en", "width": "100%", "height": "100%" }}
            </script>
        </div>
    """, height=520)

# --- TAB 6: SIGNAL ANALYZER (Financial Screener Data) ---
with tab6:
    components.html(f"""
        <div style="height:500px;">
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-financials.js" async>
            {{ "symbol": "{tv_ticker}", "colorTheme": "dark", "displayMode": "regular", "width": "100%", "height": "100%", "locale": "en" }}
            </script>
        </div>
    """, height=520)








