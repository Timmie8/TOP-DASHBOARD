import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas_ta as ta
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="SST ELITE TERMINAL", layout="wide")

st.markdown("""
    <style>
    .block-container { padding: 1rem !important; background-color: #050608; }
    
    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(145deg, #0d1117, #161b22);
        border: 1px solid #30363d;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .kpi-value { font-size: 1.6rem; font-weight: 800; }
    .kpi-label { font-size: 0.65rem; color: #8b949e; text-transform: uppercase; margin-bottom: 5px; }

    /* Score Colors - High Contrast */
    .score-high { color: #3fb950 !important; text-shadow: 0 0 10px rgba(63, 185, 80, 0.4); }
    .score-mid { color: #d29922 !important; text-shadow: 0 0 10px rgba(210, 153, 34, 0.4); }
    .score-low { color: #f85149 !important; text-shadow: 0 0 10px rgba(248, 81, 73, 0.4); }
    .text-bull { color: #3fb950 !important; }
    .text-bear { color: #f85149 !important; }

    /* Alert Box Sidebar */
    .alert-sidebar {
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 15px;
        height: 500px;
        overflow-y: auto;
    }
    .alert-item {
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
        font-size: 0.85rem;
        border-left: 4px solid;
    }
    .alert-success { background: rgba(63, 185, 80, 0.1); border-left-color: #3fb950; color: #3fb950; }
    .alert-warning { background: rgba(210, 153, 34, 0.1); border-left-color: #d29922; color: #d29922; }

    /* Watchlist Grid Cards */
    .wl-card {
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 5px;
    }
    .alert-trend { border: 2px solid #3fb950 !important; box-shadow: 0 0 12px rgba(63, 185, 80, 0.4); }
    .alert-breakout { border: 2px solid #2563eb !important; box-shadow: 0 0 12px rgba(37, 99, 235, 0.4); }

    .badge { padding: 4px 8px; border-radius: 6px; font-size: 0.6rem; font-weight: 900; text-transform: uppercase; }
    .badge-trend { background: rgba(63, 185, 80, 0.15); color: #3fb950; border: 1px solid #3fb950; }
    .badge-breakout { background: rgba(37, 99, 235, 0.15); color: #2563eb; border: 1px solid #2563eb; }
    .badge-none { background: rgba(139, 148, 158, 0.1); color: #8b949e; border: 1px solid #30363d; }
    
    .stButton button { background-color: #21262d; border: 1px solid #30363d; font-size: 0.7rem; height: 30px; }
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
        
        price = float(df['Close'].iloc[-1])
        change = ((price - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100
        rsi = ta.rsi(df['Close'], length=14).iloc[-1]
        macd = ta.macd(df['Close'])
        ml, sl = macd.iloc[-1, 0], macd.iloc[-1, 2]
        e20, e50, e200 = ta.ema(df['Close'], 20).iloc[-1], ta.ema(df['Close'], 50).iloc[-1], ta.ema(df['Close'], 200).iloc[-1]
        
        score = max(min(int(50 + (change * 12)), 99), 5)
        signal_text = "NONE"
        if price > e50 and ml > sl: signal_text = "BREAKOUT"
        elif price > e20 and ml > sl and 40 <= rsi <= 60: signal_text = "TREND"
            
        return {
            "symbol": ticker_symbol, "price": price, "score": score, "signal": signal_text, 
            "macd_bull": ml > sl, "ema_ok": price > e20 and price > e50 and price > e200, "change": change
        }
    except: return None

# --- PRE-CALCULATE DATA ---
active_alerts = []
for t in st.session_state.watchlist:
    res = get_analysis(t)
    if res:
        st.session_state.last_results[t] = res
        if res['score'] >= 90: active_alerts.append({"msg": f"🔥 {t}: Momentum Alert ({res['score']})", "type": "warning"})
        if res['signal'] in ["BREAKOUT", "TREND"]: active_alerts.append({"msg": f"📈 {t}: {res['signal']} Signal!", "type": "success"})

# --- UI: HEADER ---
st.title("SST ELITE TERMINAL")
c1, c2, c3 = st.columns([4, 1, 1.5])
input_tickers = c1.text_input("", placeholder="Quick Add (e.g. MSFT, AMZN)", key="ticker_input").upper()
if c2.button("➕ ADD", use_container_width=True):
    if input_tickers:
        for t in [x.strip() for x in input_tickers.split(',')]:
            if t not in st.session_state.watchlist: st.session_state.watchlist.append(t)
        st.rerun()
if c3.button("🔄 SYNC", use_container_width=True): st.rerun()

# --- UI: MAIN KPI BAR ---
active_data = st.session_state.last_results.get(st.session_state.current_ticker) or get_analysis(st.session_state.current_ticker)
if active_data:
    s_val = active_data["score"]
    s_class = "score-high" if s_val >= 60 else "score-mid" if s_val >= 40 else "score-low"
    macd_class = "text-bull" if active_data["macd_bull"] else "text-bear"
    ema_class = "text-bull" if active_data["ema_ok"] else "text-bear"
    price_class = "text-bull" if active_data["change"] >= 0 else "text-bear"

    k1, k2, k3, k4, k5 = st.columns(5)
    with k1: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Price</div><div class="kpi-value {price_class}">${active_data["price"]:.2f}</div></div>', unsafe_allow_html=True)
    with k2: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Momentum Score</div><div class="kpi-value {s_class}">{s_val}</div></div>', unsafe_allow_html=True)
    with k3: st.markdown(f'<div class="kpi-card"><div class="kpi-label">MACD</div><div class="kpi-value {macd_class}">{"BULL" if active_data["macd_bull"] else "BEAR"}</div></div>', unsafe_allow_html=True)
    with k4: st.markdown(f'<div class="kpi-card"><div class="kpi-label">EMA Stack</div><div class="kpi-value {ema_class}">{"HEALTHY" if active_data["ema_ok"] else "WEAK"}</div></div>', unsafe_allow_html=True)
    with k5: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Signal</div><div class="kpi-value" style="color:white;">{active_data["signal"]}</div></div>', unsafe_allow_html=True)

    # --- CHART AND ALERTS SIDE-BY-SIDE ---
    col_chart, col_alerts = st.columns([3, 1])
    with col_chart:
        tv_html = f"""<div id="tv-chart" style="height: 500px; border: 1px solid #30363d; border-radius: 12px;"></div>
        <script src="https://s3.tradingview.com/tv.js"></script>
        <script>new TradingView.widget({{"autosize": true, "symbol": "{active_data['symbol']}", "interval": "D", "theme": "dark", "container_id": "tv-chart"}});</script>"""
        components.html(tv_html, height=510)
        
    with col_alerts:
        st.markdown('<p style="color:#8b949e; font-size:0.75rem; font-weight:bold; text-transform:uppercase;">Live Signals</p>', unsafe_allow_html=True)
        alert_html = "".join([f'<div class="alert-item alert-{a["type"]}">{a["msg"]}</div>' for a in active_alerts])
        if not alert_html: alert_html = '<p style="color:#444; font-size:0.8rem;">Scanning markets...</p>'
        st.markdown(f'<div class="alert-sidebar">{alert_html}</div>', unsafe_allow_html=True)
        
        if active_alerts:
            components.html(f"""
                <audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg"></audio>
                <div id="popup" style="position:fixed; top:20px; right:20px; background:#161b22; border:2px solid #2563eb; color:white; padding:15px; border-radius:10px; z-index:10000; box-shadow:0 0 20px rgba(0,0,0,0.5); font-family:sans-serif;">
                    <b style="color:#2563eb">⚡ SIGNAL DETECTED</b><br><span style="font-size:0.9rem">Check the live signal sidebar.</span>
                </div>
                <script>setTimeout(()=>{{document.getElementById('popup').style.display='none'}}, 20000);</script>
            """, height=0)

# --- UI: WATCHLIST GRID ---
st.write("---")
st.subheader("Watchlist Monitor")
cols = st.columns(3)
for idx, item in enumerate(st.session_state.watchlist):
    w = st.session_state.last_results.get(item)
    if w:
        alert_c = "alert-trend" if w['signal'] == "TREND" else "alert-breakout" if w['signal'] == "BREAKOUT" else ""
        badge_c = "badge-trend" if w['signal'] == "TREND" else "badge-breakout" if w['signal'] == "BREAKOUT" else "badge-none"
        sw_c = "score-high" if w['score'] >= 60 else "score-mid" if w['score'] >= 40 else "score-low"
        price_c = "text-bull" if w['change'] >= 0 else "text-bear"
        
        with cols[idx % 3]:
            st.markdown(f"""
                <div class="wl-card {alert_c}">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <b style="font-size:1.1rem;">{item}</b>
                        <span class="badge {badge_c}">{w['signal']}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-top:12px;">
                        <span class="{price_c}" style="font-family:monospace; font-weight:bold;">${w['price']:.2f}</span>
                        <span style="color:#8b949e; font-size:0.8rem;">Score: <b class="{sw_c}">{w['score']}</b></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            b1, b2 = st.columns(2)
            if b1.button("VIEW", key=f"v_{item}"): 
                st.session_state.current_ticker = item
                st.rerun()
            if b2.button("DEL", key=f"d_{item}"): 
                st.session_state.watchlist.remove(item)
                st.rerun()










































