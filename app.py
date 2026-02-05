import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas_ta as ta
import pandas as pd
import os
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="SST ELITE TERMINAL", layout="wide")

WATCHLIST_FILE = "watchlist_data.csv"

# --- AUDIO FUNCTIE ---
def play_notification_sound():
    # Gebruik een betrouwbare korte "ping" of "notification" URL
    audio_url = "https://actions.google.com/sounds/v1/alarms/beep_short.ogg"
    sound_html = f"""
        <audio autoplay>
            <source src="{audio_url}" type="audio/ogg">
        </audio>
    """
    st.components.v1.html(sound_html, height=0, width=0)

# 2. Data Persistence & Helpers
def load_watchlist():
    if os.path.exists(WATCHLIST_FILE):
        try: return pd.read_csv(WATCHLIST_FILE)['ticker'].tolist()
        except: pass
    return ["NVDA", "AAPL", "TSLA"]

def save_watchlist(watchlist):
    pd.DataFrame({'ticker': watchlist}).to_csv(WATCHLIST_FILE, index=False)

# CSS Styling (Geluidsindicator toegevoegd)
st.markdown("""
    <style>
    .block-container { padding: 1rem !important; background-color: #050608; }
    .kpi-card { background: linear-gradient(145deg, #0d1117, #161b22); border: 1px solid #30363d; padding: 15px; border-radius: 12px; text-align: center; }
    .kpi-value { font-size: 1.6rem; font-weight: 800; }
    .earnings-imminent { 
        background: rgba(248, 81, 73, 0.2); border: 1px solid #f85149; color: #f85149; 
        padding: 12px; border-radius: 8px; font-weight: bold; text-align: center;
        animation: blink 2s infinite; margin-bottom: 15px;
    }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.6; } 100% { opacity: 1; } }
    .wl-card { background: #0d1117; border: 1px solid #30363d; border-radius: 12px; padding: 15px; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Earnings & Analysis
@st.cache_data(ttl=3600)
def get_earnings_info(ticker_symbol):
    try:
        t_obj = yf.Ticker(ticker_symbol)
        cal = t_obj.calendar
        if cal is not None and 'Earnings Date' in cal: return cal['Earnings Date'][0]
        info = t_obj.info
        if 'nextEarningsDate' in info: return datetime.fromtimestamp(info['nextEarningsDate'])
    except: return None
    return None

@st.cache_data(ttl=15)
def get_analysis(ticker_symbol):
    try:
        df = yf.download(ticker_symbol, period="1y", interval="1d", progress=False, auto_adjust=True)
        if df.empty: return None
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        price = float(df['Close'].iloc[-1])
        change = ((price - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100
        rsi = ta.rsi(df['Close'], length=14).iloc[-1]
        score = max(min(int(50 + (change * 12) + (rsi - 50) * 0.5), 100), 0)
        earn_date = get_earnings_info(ticker_symbol)
        return {"symbol": ticker_symbol, "price": price, "score": score, "earnings": earn_date, "change": change}
    except: return None

# Init
if 'watchlist' not in st.session_state: st.session_state.watchlist = load_watchlist()
if 'current_ticker' not in st.session_state: st.session_state.current_ticker = st.session_state.watchlist[0]
if 'last_results' not in st.session_state: st.session_state.last_results = {}

# Sync & Alert Detection
alert_triggered = False
today = datetime.now().date()

for t in st.session_state.watchlist:
    res = get_analysis(t)
    if res: 
        st.session_state.last_results[t] = res
        # Check voor geluids-trigger (Earnings binnen 2 dagen)
        if res.get("earnings"):
            ed = res["earnings"].date() if hasattr(res["earnings"], 'date') else res["earnings"]
            if 0 <= (ed - today).days <= 2:
                alert_triggered = True

# --- UI ---
st.title("SST ELITE TERMINAL")

# Speel geluid af als er een alert is
if alert_triggered:
    play_notification_sound()

# --- MAIN DISPLAY ---
active_data = st.session_state.last_results.get(st.session_state.current_ticker)
if active_data:
    earn_str = "N/A"
    if active_data.get("earnings"):
        ed = active_data["earnings"].date() if hasattr(active_data["earnings"], 'date') else active_data["earnings"]
        earn_str = ed.strftime("%d %b")
        if 0 <= (ed - today).days <= 2:
            st.markdown(f'<div class="earnings-imminent">🔊 ALERT: EARNINGS NABIJ ({earn_str})</div>', unsafe_allow_html=True)

    # De rest van je KPI kaarten en Chart (zoals in vorige versie)...
    st.write(f"Displaying data for: {st.session_state.current_ticker}")
    # ... (KPI's en TradingView widget) ...










































