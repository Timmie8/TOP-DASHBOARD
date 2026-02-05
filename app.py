import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas_ta as ta
import pandas as pd
import os
from datetime import datetime, timedelta

# 1. Page Configuration
st.set_page_config(page_title="SST ELITE TERMINAL", layout="wide")

WATCHLIST_FILE = "watchlist_data.csv"

def load_watchlist():
    if os.path.exists(WATCHLIST_FILE):
        return pd.read_csv(WATCHLIST_FILE)['ticker'].tolist()
    return ["NVDA", "AAPL", "TSLA"]

def save_watchlist(watchlist):
    pd.DataFrame({'ticker': watchlist}).to_csv(WATCHLIST_FILE, index=False)

# Uitgebreide CSS voor Earnings Alerts
st.markdown("""
    <style>
    .block-container { padding: 1rem !important; background-color: #050608; }
    .kpi-card { background: linear-gradient(145deg, #0d1117, #161b22); border: 1px solid #30363d; padding: 15px; border-radius: 12px; text-align: center; }
    .kpi-value { font-size: 1.6rem; font-weight: 800; }
    .kpi-label { font-size: 0.65rem; color: #8b949e; text-transform: uppercase; }
    .score-high { color: #3fb950 !important; text-shadow: 0 0 12px rgba(63, 185, 80, 0.6); }
    .score-mid { color: #d29922 !important; text-shadow: 0 0 10px rgba(210, 153, 34, 0.6); }
    .score-low { color: #f85149 !important; text-shadow: 0 0 10px rgba(248, 81, 73, 0.6); }
    
    /* Earnings Alert Style */
    .earnings-imminent { 
        background: rgba(248, 81, 73, 0.1); 
        border: 1px solid #f85149; 
        color: #f85149; 
        padding: 8px; 
        border-radius: 8px; 
        font-weight: bold; 
        animation: blink 2s infinite;
        margin-bottom: 10px;
    }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
    
    .wl-card { background: #0d1117; border: 1px solid #30363d; border-radius: 12px; padding: 15px; margin-bottom: 5px; }
    .alert-trend { border: 2px solid #3fb950 !important; }
    .alert-breakout { border: 2px solid #2563eb !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Analysis Function met Earnings
@st.cache_data(ttl=3600) # Earnings hoeven minder vaak ververst te worden
def get_earnings_date(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        calendar = ticker.calendar
        if calendar is not None and 'Earnings Date' in calendar:
            return calendar['Earnings Date'][0]
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
        macd = ta.macd(df['Close'])
        ml, sl = macd.iloc[-1, 0], macd.iloc[-1, 2]
        e20, e50 = ta.ema(df['Close'], 20).iloc[-1], ta.ema(df['Close'], 50).iloc[-1]
        
        score = max(min(int(50 + (change * 12) + (rsi - 50) * 0.5), 100), 0)
        signal = "BREAKOUT" if (price > e50 and ml > sl) else "TREND" if (price > e20 and ml > sl) else "NONE"
        
        # Earnings ophalen
        earn_date = get_earnings_date(ticker_symbol)
        
        return {"symbol": ticker_symbol, "price": price, "score": score, "signal": signal, 
                "macd_bull": ml > sl, "ema_ok": price > e50, "change": change, "earnings": earn_date}
    except: return None

# Initialisatie
if 'watchlist' not in st.session_state: st.session_state.watchlist = load_watchlist()
if 'current_ticker' not in st.session_state: st.session_state.current_ticker = st.session_state.watchlist[0]
if 'last_results' not in st.session_state: st.session_state.last_results = {}

for t in st.session_state.watchlist:
    res = get_analysis(t)
    if res: st.session_state.last_results[t] = res

# --- UI ---
st.title("SST ELITE TERMINAL")
c1, c2, c3 = st.columns([4, 1, 1.5])
input_tickers = c1.text_input("", placeholder="Ticker toevoegen...", key="ticker_input").upper()

if c2.button("➕ ADD", use_container_width=True):
    if input_tickers:
        new_list = [x.strip() for x in input_tickers.split(',')]
        for t in new_list:
            if t not in st.session_state.watchlist: st.session_state.watchlist.append(t)
        save_watchlist(st.session_state.watchlist)
        st.session_state.current_ticker = new_list[-1]
        st.rerun()

# --- MAIN DISPLAY ---
active_data = st.session_state.last_results.get(st.session_state.current_ticker)
if active_data:
    # Check Earnings Alert (2 dagen)
    alert_html = ""
    if active_data["earnings"]:
        days_to_earn = (active_data["earnings"].date() - datetime.now().date()).days
        if 0 <= days_to_earn <= 2:
            alert_html = f'<div class="earnings-imminent">⚠️ EARNINGS OVER {days_to_earn} DAGEN ({active_data["earnings"].strftime("%d %b")})</div>'

    st.markdown(alert_html, unsafe_allow_html=True)

    # KPI's...
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Price</div><div class="kpi-value">S{active_data["price"]:.2f}</div></div>', unsafe_allow_html=True)
    with k2: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Score</div><div class="kpi-value">{active_data["score"]}</div></div>', unsafe_allow_html=True)
    with k3: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Earnings</div><div class="kpi-value" style="font-size:1rem;">{active_data["earnings"].strftime("%d-%m") if active_data["earnings"] else "N/A"}</div></div>', unsafe_allow_html=True)
    # ... overige kpi's ...

    # Chart & Sidebar
    col_chart, col_alerts = st.columns([3, 1])
    with col_chart:
        tv_html = f"""<div id="tv-chart" style="height: 500px; border: 1px solid #30363d; border-radius: 12px;"></div>
        <script src="https://s3.tradingview.com/tv.js"></script>
        <script>new TradingView.widget({{"autosize": true, "symbol": "{active_data['symbol']}", "interval": "D", "theme": "dark", "container_id": "tv-chart"}});</script>"""
        components.html(tv_html, height=510)
    
    with col_alerts:
        st.markdown('<p style="color:#8b949e; font-size:0.75rem; font-weight:bold;">EARNINGS & SIGNALS</p>', unsafe_allow_html=True)
        with st.container(height=465, border=True):
            for item in st.session_state.watchlist:
                r = st.session_state.last_results.get(item)
                if r and r["earnings"]:
                    days = (r["earnings"].date() - datetime.now().date()).days
                    if 0 <= days <= 2:
                        st.markdown(f'<div style="color:#f85149; font-size:0.8rem; padding:5px; border:1px solid #f85149; border-radius:5px; margin-bottom:5px;">🚨 {item} Earnings: {r["earnings"].strftime("%d %b")}</div>', unsafe_allow_html=True)
            # ... bestaande signals ...

# --- WATCHLIST GRID ---
st.write("---")
cols = st.columns(3)
for idx, item in enumerate(st.session_state.watchlist):
    w = st.session_state.last_results.get(item)
    if w:
        border_c = "alert-trend" if w['signal'] == "TREND" else "alert-breakout" if w['signal'] == "BREAKOUT" else ""
        earn_info = w["earnings"].strftime("%d/%m") if w["earnings"] else "--"
        with cols[idx % 3]:
            st.markdown(f"""<div class="wl-card {border_c}">
                <b>{item}</b> | <span style="font-size:0.7rem;">Earnings: {earn_info}</span>
                <div style="display:flex; justify-content:space-between; margin-top:5px;">
                    <span class="score-label-white">Score: {w['score']}</span>
                    <span>{w['signal']}</span>
                </div></div>""", unsafe_allow_html=True)
            if st.button("VIEW", key=f"v_{item}"): 
                st.session_state.current_ticker = item
                st.rerun()












































