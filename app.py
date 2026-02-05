import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas_ta as ta
import pandas as pd
import os
from datetime import datetime

# 1. Pagina instellingen
st.set_page_config(page_title="SST ELITE TERMINAL", layout="wide")

WATCHLIST_FILE = "watchlist_data.csv"

# --- PERSISTENCE ---
def load_watchlist():
    if os.path.exists(WATCHLIST_FILE):
        try:
            df = pd.read_csv(WATCHLIST_FILE)
            return df['ticker'].tolist()
        except: pass
    return ["NVDA", "AAPL", "TSLA"]

def save_watchlist(watchlist):
    pd.DataFrame({'ticker': watchlist}).to_csv(WATCHLIST_FILE, index=False)

# --- STYLING ---
st.markdown("""
    <style>
    .block-container { padding: 1rem !important; background-color: #050608; }
    .kpi-card { background: linear-gradient(145deg, #0d1117, #161b22); border: 1px solid #30363d; padding: 15px; border-radius: 12px; text-align: center; }
    .kpi-value { font-size: 1.5rem; font-weight: 800; color: white; }
    .score-high { color: #3fb950 !important; text-shadow: 0 0 10px rgba(63, 185, 80, 0.5); }
    .score-label-white { color: #ffffff !important; font-weight: bold; }
    .earnings-alert { 
        background: rgba(248, 81, 73, 0.2); border: 1px solid #f85149; color: #f85149; 
        padding: 10px; border-radius: 8px; font-weight: bold; text-align: center; margin-bottom: 15px;
    }
    .wl-card { background: #0d1117; border: 1px solid #30363d; border-radius: 12px; padding: 12px; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA FUNCTIES ---
@st.cache_data(ttl=15)
def get_stock_data(ticker_symbol):
    try:
        # Data ophalen
        data = yf.download(ticker_symbol, period="1y", interval="1d", progress=False, auto_adjust=True)
        if data.empty: return None
        if isinstance(data.columns, pd.MultiIndex): data.columns = data.columns.get_level_values(0)
        
        # Ticker info voor earnings
        t_info = yf.Ticker(ticker_symbol)
        earn_date = None
        try:
            cal = t_info.calendar
            if cal is not None and 'Earnings Date' in cal:
                earn_date = cal['Earnings Date'][0]
        except: pass

        price = float(data['Close'].iloc[-1])
        change = ((price - data['Close'].iloc[-2]) / data['Close'].iloc[-2]) * 100
        rsi = ta.rsi(data['Close'], length=14).iloc[-1]
        score = max(min(int(50 + (change * 12) + (rsi - 50) * 0.5), 100), 0)
        
        return {
            "symbol": ticker_symbol, "price": price, "score": score, 
            "change": change, "earnings": earn_date
        }
    except Exception as e:
        return None

# --- STATE MANAGEMENT ---
if 'watchlist' not in st.session_state: st.session_state.watchlist = load_watchlist()
if 'current_ticker' not in st.session_state: st.session_state.current_ticker = st.session_state.watchlist[0]

# --- SYNC & ALERTS ---
results = {}
alert_triggered = False
today = datetime.now().date()

for t in st.session_state.watchlist:
    res = get_stock_data(t)
    if res:
        results[t] = res
        # Check voor geluid trigger
        if res['earnings']:
            try:
                ed = res['earnings'].date() if hasattr(res['earnings'], 'date') else res['earnings']
                if 0 <= (ed - today).days <= 2:
                    alert_triggered = True
            except: pass

# --- UI HEADER ---
st.title("SST ELITE TERMINAL")

# AUDIO INJECTIE
if alert_triggered:
    components.html("""
        <audio autoplay><source src="https://actions.google.com/sounds/v1/alarms/beep_short.ogg" type="audio/ogg"></audio>
    """, height=0)

c1, c2 = st.columns([4, 1])
new_ticker = c1.text_input("Ticker toevoegen (bijv. NVDA, TSLA)", key="add_t").upper()
if c2.button("➕ ADD") and new_ticker:
    if new_ticker not in st.session_state.watchlist:
        st.session_state.watchlist.append(new_ticker)
        save_watchlist(st.session_state.watchlist)
        st.rerun()

# --- MAIN DISPLAY ---
active = results.get(st.session_state.current_ticker)
if active:
    # Earnings Alert bovenaan
    if active['earnings']:
        try:
            ed = active['earnings'].date() if hasattr(active['earnings'], 'date') else active['earnings']
            diff = (ed - today).days
            if 0 <= diff <= 2:
                st.markdown(f'<div class="earnings-alert">🚨 EARNINGS ALERT: {active["symbol"]} rapportcijfers over {diff} dag(en)!</div>', unsafe_allow_html=True)
        except: pass

    # KPI's
    k1, k2, k3 = st.columns(3)
    k1.markdown(f'<div class="kpi-card"><div style="color:#8b949e; font-size:0.7rem;">PRICE</div><div class="kpi-value">${active["price"]:.2f}</div></div>', unsafe_allow_html=True)
    k2.markdown(f'<div class="kpi-card"><div style="color:#8b949e; font-size:0.7rem;">SCORE</div><div class="kpi-value score-high">{active["score"]}</div></div>', unsafe_allow_html=True)
    earn_disp = active['earnings'].strftime("%d %b") if active['earnings'] and hasattr(active['earnings'], 'strftime') else "N/A"
    k3.markdown(f'<div class="kpi-card"><div style="color:#8b949e; font-size:0.7rem;">EARNINGS</div><div class="kpi-value" style="font-size:1.1rem;">{earn_disp}</div></div>', unsafe_allow_html=True)

    # Chart
    st.write("")
    tv_html = f"""<div id="tv-chart" style="height: 400px; border: 1px solid #30363d; border-radius: 12px;"></div>
    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>new TradingView.widget({{"autosize": true, "symbol": "{active['symbol']}", "interval": "D", "theme": "dark", "container_id": "tv-chart"}});</script>"""
    components.html(tv_html, height=410)

# --- WATCHLIST GRID ---
st.write("---")
st.subheader("Your Watchlist")
cols = st.columns(3)
for idx, t in enumerate(st.session_state.watchlist):
    w = results.get(t)
    if w:
        with cols[idx % 3]:
            st.markdown(f"""<div class="wl-card">
                <div style="display:flex; justify-content:space-between;"><b>{t}</b> <span>${w['price']:.2f}</span></div>
                <div style="margin-top:10px;"><span class="score-label-white">Score: <span class="score-high">{w['score']}</span></span></div>
            </div>""", unsafe_allow_html=True)
            b1, b2 = st.columns(2)
            if b1.button(f"VIEW {t}", key=f"v_{t}"):
                st.session_state.current_ticker = t
                st.rerun()
            if b2.button(f"DEL {t}", key=f"d_{t}"):
                st.session_state.watchlist.remove(t)
                save_watchlist(st.session_state.watchlist)
                st.rerun()










































