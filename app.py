import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas_ta as ta
import pandas as pd

# 1. Pagina Configuratie
st.set_page_config(page_title="SST ELITE TERMINAL", layout="wide")

st.markdown("""
    <style>
    .block-container { padding: 15px !important; background-color: #050608; }
    .kpi-card { background: #0d1117; border: 1px solid #30363d; padding: 15px; border-radius: 12px; text-align: center; }
    .kpi-value { font-size: 1.7rem; font-weight: 900; }
    .kpi-label { font-size: 0.75rem; color: #8b949e; text-transform: uppercase; margin-bottom: 5px; }
    .wl-box { background-color: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin-bottom: 10px; min-height: 85px; }
    .glow-green { border: 2px solid #3fb950 !important; box-shadow: 0 0 10px rgba(63, 185, 80, 0.4); animation: pulse-green 2s infinite; }
    .glow-blue { border: 2px solid #2563eb !important; box-shadow: 0 0 10px rgba(37, 99, 235, 0.4); animation: pulse-blue 2s infinite; }
    @keyframes pulse-green { 0% { box-shadow: 0 0 5px rgba(63, 185, 80, 0.2); } 50% { box-shadow: 0 0 15px rgba(63, 185, 80, 0.6); } 100% { box-shadow: 0 0 5px rgba(63, 185, 80, 0.2); } }
    @keyframes pulse-blue { 0% { box-shadow: 0 0 5px rgba(37, 99, 235, 0.2); } 50% { box-shadow: 0 0 15px rgba(37, 99, 235, 0.6); } 100% { box-shadow: 0 0 5px rgba(37, 99, 235, 0.2); } }
    .stButton button { border-radius: 4px; padding: 0px 5px; font-size: 0.75rem; height: 30px; }
    </style>
    """, unsafe_allow_html=True)

# 2. State Management
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = ["NVDA", "AAPL", "BTC-USD", "ETH-USD", "TSLA"]
if 'current_ticker' not in st.session_state:
    st.session_state.current_ticker = "NVDA"
if 'last_results' not in st.session_state:
    st.session_state.last_results = {}

# 3. Analyse Functie
@st.cache_data(ttl=10)
def get_analysis(ticker_symbol):
    try:
        df = yf.download(ticker_symbol, period="1y", interval="1d", progress=False, auto_adjust=True)
        if df.empty or len(df) < 20: return None
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)

        price = float(df['Close'].iloc[-1])
        change = ((price - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100
        rsi = ta.rsi(df['Close'], length=14).iloc[-1]
        macd = ta.macd(df['Close'])
        ml, sl = macd.iloc[-1, 0], macd.iloc[-1, 2]
        e20, e50, e200 = ta.ema(df['Close'], 20).iloc[-1], ta.ema(df['Close'], 50).iloc[-1], ta.ema(df['Close'], 200).iloc[-1]
        upper_bb = ta.bbands(df['Close'], length=20).iloc[-1, 2]
        vol_avg = df['Volume'].rolling(20).mean().iloc[-1]
        vol_curr = df['Volume'].iloc[-1]

        score = max(min(int(50 + (change * 12)), 99), 5)
        
        signal_val, signal_text = 0, "NONE"
        if price > upper_bb and ml > sl and price > e50 and vol_curr > vol_avg:
            signal_text = "BREAKOUT"; signal_val = 2
        elif price > e20 and price > e50 and price > e200 and ml > sl and 40 <= rsi <= 60:
            signal_text = "TREND"; signal_val = 1

        return {
            "symbol": ticker_symbol, "price": price, "score": score, "signal": signal_text, 
            "priority": signal_val, "macd_bull": ml > sl, "ema_ok": price > e20 and price > e50 and price > e200, "change": change
        }
    except: return None

# --- SYNC DATA ---
for t in st.session_state.watchlist:
    res = get_analysis(t)
    if res: st.session_state.last_results[t] = res

# --- UI: TOP BAR ---
st.title("🚀 SST ELITE DASHBOARD")
c1, c2, c3 = st.columns([4, 1, 1.5])
input_tickers = c1.text_input("", placeholder="Tickers (bv: NVDA, AAPL)", label_visibility="collapsed").upper()

if c2.button("➕ ADD", use_container_width=True):
    if input_tickers:
        new_list = [t.strip() for t in input_tickers.split(',') if t.strip()]
        for t in new_list:
            if t not in st.session_state.watchlist: st.session_state.watchlist.append(t)
        st.rerun()

if c3.button("🔍 SCAN & SORTEER", use_container_width=True):
    st.session_state.watchlist.sort(key=lambda x: (st.session_state.last_results.get(x, {}).get('priority', 0), 
                                                 st.session_state.last_results.get(x, {}).get('score', 0)), reverse=True)
    st.rerun()

# --- UI: KPI SECTIE ---
active_data = st.session_state.last_results.get(st.session_state.current_ticker)
if active_data:
    k1, k2, k3, k4, k5 = st.columns(5)
    p_color = "#3fb950" if active_data['change'] >= 0 else "#f85149"
    s_color = "#3fb950" if active_data['score'] > 60 else "#d29922" if active_data['score'] >= 40 else "#f85149"
    m_color = "#3fb950" if active_data['macd_bull'] else "#f85149"
    e_color = "#3fb950" if active_data['ema_ok'] else "#f85149"
    sig = active_data['signal']
    sig_color = "#3fb950" if sig == "TREND" else "#2563eb" if sig == "BREAKOUT" else "#8b949e"

    with k1: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Price</div><div class="kpi-value" style="color:{p_color}">${active_data["price"]:.2f}</div></div>', unsafe_allow_html=True)
    with k2: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Score</div><div class="kpi-value" style="color:{s_color}">{active_data["score"]}</div></div>', unsafe_allow_html=True)
    with k3: st.markdown(f'<div class="kpi-card"><div class="kpi-label">MACD</div><div class="kpi-value" style="color:{m_color}">{"BULL" if active_data["macd_bull"] else "BEAR"}</div></div>', unsafe_allow_html=True)
    with k4: st.markdown(f'<div class="kpi-card"><div class="kpi-label">EMA</div><div class="kpi-value" style="color:{e_color}">{"OK" if active_data["ema_ok"] else "ZWAK"}</div></div>', unsafe_allow_html=True)
    with k5: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Signal</div><div class="kpi-value" style="color:{sig_color}">{sig}</div></div>', unsafe_allow_html=True)

    tv_html = f"""<div id="tv-chart" style="height: 500px; border: 1px solid #30363d; border-radius: 12px; margin-top: 15px;"></div>
    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>new TradingView.widget({{"autosize": true, "symbol": "{active_data['symbol']}", "interval": "D", "theme": "dark", "container_id": "tv-chart"}});</script>"""
    components.html(tv_html, height=520)

# --- UI: GRID WATCHLIST ---
st.write("---")
cols = st.columns(3)
for idx, item in enumerate(st.session_state.watchlist):
    w = st.session_state.last_results.get(item)
    if w:
        glow = "glow-green" if w['signal'] == "TREND" else "glow-blue" if w['signal'] == "BREAKOUT" else ""
        s_clr = "#3fb950" if w['signal'] == "TREND" else "#2563eb" if w['signal'] == "BREAKOUT" else "#8b949e"
        with cols[idx % 3]:
            # HTML code opgesplitst om SyntaxErrors te voorkomen
            st.markdown(f"""
                <div class="wl-box {glow}">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color:white; font-weight:900; font-size:1.1rem;">{item}</span>
                        <span style="color:{s_clr}; font-weight:bold; font-size:0.8rem;">{w['signal']}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top:8px; color:#8b949e; font-size:0.85rem;">
                        <span>Score: <b style="color:white;">{w['score']}</b></span>
                        <span>Prijs: <b style="color:white;">${w['price']:.2f}</b></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            b1, b2 = st.columns(2)
            if b1.button(f"Bekijk {item}", key=f"v_{item}", use_container_width=True):
                st.session_state.current_ticker = item
                st.rerun()
            if b2.button(f"Wis {item}", key=f"d_{item}", use_container_width=True):
                st.session_state.watchlist.remove(item)
                st.rerun()







































