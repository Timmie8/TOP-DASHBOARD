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
    }
    .kpi-value { font-size: 1.6rem; font-weight: 800; }
    .kpi-label { font-size: 0.65rem; color: #8b949e; text-transform: uppercase; }

    /* Score Colors */
    .score-high { color: #3fb950 !important; text-shadow: 0 0 12px rgba(63, 185, 80, 0.6); }
    .score-mid { color: #d29922 !important; text-shadow: 0 0 12px rgba(210, 153, 34, 0.6); }
    .score-low { color: #f85149 !important; text-shadow: 0 0 12px rgba(248, 81, 73, 0.6); }
    .text-bull { color: #3fb950 !important; }
    .text-bear { color: #f85149 !important; }

    /* Watchlist Cards */
    .wl-card {
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 5px;
    }
    .wl-card b { 
        color: #ffffff !important; 
        text-shadow: 0px 0px 8px rgba(255,255,255,0.6);
        font-size: 1.2rem;
    }
    
    /* Watchlist Buttons - HERSTELD VOOR LEESBAARHEID */
    .stButton > button {
        background-color: #1c2128 !important;
        color: #ffffff !important;
        border: 1px solid #444c56 !important;
        font-size: 0.75rem !important;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        border-color: #8b949e !important;
        background-color: #30363d !important;
    }

    .alert-trend { border: 2px solid #3fb950 !important; }
    .alert-breakout { border: 2px solid #2563eb !important; }
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
        e20, e50 = ta.ema(df['Close'], 20).iloc[-1], ta.ema(df['Close'], 50).iloc[-1]
        
        score = max(min(int(50 + (change * 12) + (rsi - 50) * 0.5), 100), 0)
        signal = "BREAKOUT" if (price > e50 and ml > sl) else "TREND" if (price > e20 and ml > sl) else "NONE"
            
        return {"symbol": ticker_symbol, "price": price, "score": score, "signal": signal, 
                "macd_bull": ml > sl, "ema_ok": price > e50, "change": change}
    except: return None

# --- ALERTS GENERATOR (EENVOUDIGE LIJST) ---
active_alerts = []
for t in st.session_state.watchlist:
    res = get_analysis(t)
    if res:
        st.session_state.last_results[t] = res
        if res['score'] >= 85:
            active_alerts.append({"msg": f"🔥 {t}: Momentum ({res['score']})", "color": "#d29922"})
        if res['signal'] in ["BREAKOUT", "TREND"]:
            active_alerts.append({"msg": f"📈 {t}: {res['signal']}!", "color": "#3fb950"})

# --- UI: HEADER ---
st.title("SST ELITE TERMINAL")
c1, c2, c3 = st.columns([4, 1, 1.5])
input_tickers = c1.text_input("", placeholder="Ticker toevoegen...", key="ticker_input").upper()
if c2.button("➕ ADD", use_container_width=True):
    if input_tickers:
        for t in [x.strip() for x in input_tickers.split(',')]:
            if t not in st.session_state.watchlist: st.session_state.watchlist.append(t)
        st.rerun()
if c3.button("🔄 SYNC", use_container_width=True): st.rerun()

# --- UI: KPI BAR ---
active_data = st.session_state.last_results.get(st.session_state.current_ticker) or get_analysis(st.session_state.current_ticker)
if active_data:
    s_val = active_data["score"]
    s_class = "score-high" if s_val >= 60 else "score-mid" if s_val >= 40 else "score-low"
    p_class = "text-bull" if active_data["change"] >= 0 else "text-bear"

    k1, k2, k3, k4, k5 = st.columns(5)
    with k1: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Price</div><div class="kpi-value {p_class}">${active_data["price"]:.2f}</div></div>', unsafe_allow_html=True)
    with k2: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Score</div><div class="kpi-value {s_class}">{s_val}</div></div>', unsafe_allow_html=True)
    with k3: st.markdown(f'<div class="kpi-card"><div class="kpi-label">MACD</div><div class="kpi-value {"text-bull" if active_data["macd_bull"] else "text-bear"}">{"BULL" if active_data["macd_bull"] else "BEAR"}</div></div>', unsafe_allow_html=True)
    with k4: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Health</div><div class="kpi-value {"text-bull" if active_data["ema_ok"] else "text-bear"}">{"OK" if active_data["ema_ok"] else "WEAK"}</div></div>', unsafe_allow_html=True)
    with k5: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Signal</div><div class="kpi-value" style="color:white;">{active_data["signal"]}</div></div>', unsafe_allow_html=True)

    # --- MAIN ROW ---
    st.write("")
    col_chart, col_alerts = st.columns([3, 1])
    
    with col_chart:
        tv_html = f"""<div id="tv-chart" style="height: 500px; border: 1px solid #30363d; border-radius: 12px;"></div>
        <script src="https://s3.tradingview.com/tv.js"></script>
        <script>new TradingView.widget({{"autosize": true, "symbol": "{active_data['symbol']}", "interval": "D", "theme": "dark", "container_id": "tv-chart"}});</script>"""
        components.html(tv_html, height=510)
    
    with col_alerts:
        st.markdown('<p style="color:#8b949e; font-size:0.75rem; font-weight:bold; margin-bottom:10px;">LIVE SIGNALS</p>', unsafe_allow_html=True)
        alert_container = st.container(height=465, border=True)
        with alert_container:
            if not active_alerts:
                st.write("Scanning...")
            else:
                for a in active_alerts:
                    st.markdown(f'<div style="color:{a["color"]}; font-size:0.85rem; padding:8px 0; border-bottom:1px solid #30363d; font-weight:600;">{a["msg"]}</div>', unsafe_allow_html=True)

# --- WATCHLIST GRID ---
st.write("---")
cols = st.columns(3)
for idx, item in enumerate(st.session_state.watchlist):
    w = st.session_state.last_results.get(item)
    if w:
        sw_c = "score-high" if w['score'] >= 60 else "score-mid" if w['score'] >= 40 else "score-low"
        price_c = "text-bull" if w['change'] >= 0 else "text-bear"
        alert_c = "alert-trend" if w['signal'] == "TREND" else "alert-breakout" if w['signal'] == "BREAKOUT" else ""
        
        with cols[idx % 3]:
            st.markdown(f"""<div class="wl-card {alert_c}">
                <div style="display:flex; justify-content:space-between;"><b>{item}</b><span style="color:#8b949e; font-size:0.75rem;">{w['signal']}</span></div>
                <div style="display:flex; justify-content:space-between; margin-top:10px;">
                    <span class="{price_c}" style="font-weight:bold;">${w['price']:.2f}</span>
                    <span>Score: <b class="{sw_c}">{w['score']}</b></span>
                </div></div>""", unsafe_allow_html=True)
            b1, b2 = st.columns(2)
            if b1.button("VIEW", key=f"v_{item}", use_container_width=True): 
                st.session_state.current_ticker = item
                st.rerun()
            if b2.button("DEL", key=f"d_{item}", use_container_width=True): 
                st.session_state.watchlist.remove(item)
                st.rerun()











































