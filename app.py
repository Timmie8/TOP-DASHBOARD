import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas_ta as ta
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="SST ELITE TERMINAL", layout="wide")

st.markdown("""
    <style>
    .block-container { padding: 1.5rem !important; background-color: #050608; }
    
    /* Custom Modal/Popup Style */
    #popup-container {
        position: fixed;
        top: 20%;
        left: 50%;
        transform: translate(-50%, -20%);
        background: #161b22;
        border: 2px solid #58a6ff;
        border-radius: 15px;
        padding: 30px;
        z-index: 9999;
        text-align: center;
        box-shadow: 0 0 30px rgba(88, 166, 255, 0.5);
        min-width: 300px;
        animation: fadeIn 0.5s;
    }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

    /* KPI Cards */
    .kpi-card { background: #0d1117; border: 1px solid #30363d; padding: 20px; border-radius: 12px; text-align: center; }
    .kpi-value { font-size: 1.8rem; font-weight: 800; }
    .kpi-label { font-size: 0.7rem; color: #8b949e; text-transform: uppercase; }

    /* Watchlist Glow */
    .wl-card { background: #0d1117; border: 1px solid #30363d; border-radius: 12px; padding: 15px; margin-bottom: 5px; }
    .alert-trend { border: 2px solid #3fb950 !important; box-shadow: 0 0 15px rgba(63, 185, 80, 0.4); }
    .alert-breakout { border: 2px solid #2563eb !important; box-shadow: 0 0 15px rgba(37, 99, 235, 0.4); }
    
    .score-high { color: #3fb950 !important; }
    .score-mid { color: #d29922 !important; }
    .score-low { color: #f85149 !important; }

    .badge { padding: 4px 10px; border-radius: 6px; font-size: 0.65rem; font-weight: 900; }
    .badge-trend { background: rgba(63, 185, 80, 0.15); color: #3fb950; border: 1px solid #3fb950; }
    .badge-breakout { background: rgba(37, 99, 235, 0.15); color: #2563eb; border: 1px solid #2563eb; }
    
    .stButton button { background-color: #21262d; border: 1px solid #30363d; color: #c9d1d9; font-size: 0.7rem; width: 100%; height: 30px; }
    </style>
    """, unsafe_allow_html=True)

# 2. State Management
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = ["NVDA", "AAPL", "TSLA", "BTC-USD", "ETH-USD"]
if 'current_ticker' not in st.session_state:
    st.session_state.current_ticker = "NVDA"
if 'last_results' not in st.session_state:
    st.session_state.last_results = {}

# 3. Analysis Function
@st.cache_data(ttl=15)
def get_analysis(ticker_symbol):
    try:
        df = yf.download(ticker_symbol, period="1y", interval="1d", progress=False, auto_adjust=True)
        if df.empty or len(df) < 20: return None
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        price = float(df['Close'].iloc[-1]); change = ((price - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100
        rsi = ta.rsi(df['Close'], length=14).iloc[-1]; macd = ta.macd(df['Close'])
        ml, sl = macd.iloc[-1, 0], macd.iloc[-1, 2]
        e20, e50, e200 = ta.ema(df['Close'], 20).iloc[-1], ta.ema(df['Close'], 50).iloc[-1], ta.ema(df['Close'], 200).iloc[-1]
        score = max(min(int(50 + (change * 12)), 99), 5)
        signal_text = "NONE"
        if price > e50 and ml > sl: signal_text = "BREAKOUT"
        elif price > e20 and ml > sl and 40 <= rsi <= 60: signal_text = "TREND"
        return {"symbol": ticker_symbol, "price": price, "score": score, "signal": signal_text, "macd_bull": ml > sl, "ema_ok": price > e20, "change": change}
    except: return None

# --- SYNC DATA & POPUP LOGIC ---
popups = []
trigger_audio = False
for t in st.session_state.watchlist:
    res = get_analysis(t)
    if res:
        st.session_state.last_results[t] = res
        if res['signal'] in ["BREAKOUT", "TREND"] or res['score'] >= 90:
            popups.append(f"🚀 {t}: {res['signal']} (Score: {res['score']})")
            trigger_audio = True

# 4. Audio & 20-Second Popup Component
if popups:
    popup_msg = "<br>".join(popups)
    # This JS handles the 20-second timer and the sound
    components.html(f"""
        <div id="popup-container">
            <h2 style="color: #58a6ff; margin-bottom: 10px;">⚡ SIGNAL ALERT</h2>
            <p style="color: white; font-family: sans-serif; font-size: 1.1rem;">{popup_msg}</p>
            <p style="color: #8b949e; font-size: 0.8rem; margin-top: 20px;">Closing in 20 seconds...</p>
        </div>
        <audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg"></audio>
        <script>
            setTimeout(function() {{
                document.getElementById('popup-container').style.display = 'none';
            }}, 20000); // 20000ms = 20 seconds
        </script>
    """, height=300)

# --- UI: HEADER ---
st.title("SST ELITE TERMINAL")
c1, c2, c3 = st.columns([4, 1, 1.5])
input_tickers = c1.text_input("", placeholder="Quick Add Tickers", key="ticker_input").upper()
if c2.button("➕ ADD", use_container_width=True):
    if input_tickers:
        for t in [x.strip() for x in input_tickers.split(',')]:
            if t not in st.session_state.watchlist: st.session_state.watchlist.append(t)
        st.rerun()
if c3.button("🔄 SYNC", use_container_width=True): st.rerun()

# --- UI: MAIN CHART ---
active_data = st.session_state.last_results.get(st.session_state.current_ticker) or get_analysis(st.session_state.current_ticker)
if active_data:
    s_val = active_data["score"]; s_class = "score-high" if s_val >= 60 else "score-mid" if s_val >= 40 else "score-low"
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Price</div><div class="kpi-value">${active_data["price"]:.2f}</div></div>', unsafe_allow_html=True)
    with k2: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Momentum Score</div><div class="kpi-value {s_class}">{s_val}</div></div>', unsafe_allow_html=True)
    with k3: st.markdown(f'<div class="kpi-card"><div class="kpi-label">MACD</div><div class="kpi-value">{"BULL" if active_data["macd_bull"] else "BEAR"}</div></div>', unsafe_allow_html=True)
    with k4: st.markdown(f'<div class="kpi-card"><div class="kpi-label">EMA Stack</div><div class="kpi-value">{"OK" if active_data["ema_ok"] else "WEAK"}</div></div>', unsafe_allow_html=True)
    with k5: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Signal</div><div class="kpi-value">{active_data["signal"]}</div></div>', unsafe_allow_html=True)
    
    tv_html = f"""<div id="tv-chart" style="height: 480px; border: 1px solid #30363d; border-radius: 12px; margin-top: 15px;"></div>
    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>new TradingView.widget({{"autosize": true, "symbol": "{active_data['symbol']}", "interval": "D", "theme": "dark", "container_id": "tv-chart"}});</script>"""
    components.html(tv_html, height=500)

# --- UI: WATCHLIST ---
st.write("---")
cols = st.columns(3)
for idx, item in enumerate(st.session_state.watchlist):
    w = st.session_state.last_results.get(item)
    if w:
        alert_class = "alert-trend" if w['signal'] == "TREND" else "alert-breakout" if w['signal'] == "BREAKOUT" else ""
        sw_class = "score-high" if w['score'] >= 60 else "score-mid" if w['score'] >= 40 else "score-low"
        with cols[idx % 3]:
            st.markdown(f'<div class="wl-card {alert_class}"><div style="display:flex;justify-content:space-between"><b>{item}</b><span class="badge"> {w["signal"]}</span></div><div style="display:flex;justify-content:space-between;margin-top:10px;"><span>${w["price"]:.2f}</span><span class="{sw_class}">Score: {w["score"]}</span></div></div>', unsafe_allow_html=True)
            b1, b2 = st.columns(2)
            if b1.button("VIEW", key=f"v_{item}"): st.session_state.current_ticker = item; st.rerun()
            if b2.button("DEL", key=f"d_{item}"): st.session_state.watchlist.remove(item); st.rerun()









































