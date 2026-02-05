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
    
    /* KPI Cards Redesign */
    .kpi-card {
        background: linear-gradient(145deg, #0d1117, #161b22);
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .kpi-value { font-size: 1.8rem; font-weight: 800; letter-spacing: -1px; }
    .kpi-label { font-size: 0.7rem; color: #8b949e; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }

    /* Professional Watchlist Table */
    .wl-container {
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 12px;
        overflow: hidden;
        margin-top: 10px;
    }
    .wl-row {
        display: flex;
        align-items: center;
        padding: 12px 20px;
        border-bottom: 1px solid #21262d;
        transition: background 0.2s ease;
    }
    .wl-row:hover { background: #161b22; }
    .wl-col-sym { flex: 1; font-weight: 700; color: #ffffff; font-size: 1.1rem; }
    .wl-col-price { flex: 1; text-align: right; font-family: 'Courier New', monospace; font-weight: 600; }
    .wl-col-score { flex: 1; text-align: center; }
    .wl-col-sig { flex: 1; text-align: right; }
    
    /* Signal Badges */
    .badge {
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.7rem;
        font-weight: 900;
        text-transform: uppercase;
    }
    .badge-trend { background: rgba(63, 185, 80, 0.15); color: #3fb950; border: 1px solid #3fb950; }
    .badge-breakout { background: rgba(37, 99, 235, 0.15); color: #2563eb; border: 1px solid #2563eb; }
    .badge-none { background: rgba(139, 148, 158, 0.1); color: #8b949e; border: 1px solid #30363d; }
    
    /* Score Indicator dots */
    .dot { height: 8px; width: 8px; border-radius: 50%; display: inline-block; margin-right: 5px; }
    
    .stButton button { 
        background-color: #21262d; border: 1px solid #30363d; color: #c9d1d9;
        font-size: 0.7rem; height: 28px; transition: 0.2s;
    }
    .stButton button:hover { border-color: #8b949e; background: #30363d; }
    </style>
    """, unsafe_allow_html=True)

def play_sound():
    sound_html = """<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg"></audio>"""
    st.markdown(sound_html, unsafe_allow_html=True)

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

# --- REFRESH DATA ---
alerts = []
play_alert = False
for t in st.session_state.watchlist:
    res = get_analysis(t)
    if res: 
        st.session_state.last_results[t] = res
        if res['score'] >= 90: alerts.append(f"🔥 **{t}**: Extreme Momentum ({res['score']})")
        if res['signal'] in ["BREAKOUT", "TREND"]:
            alerts.append(f"📈 **{t}**: {res['signal']} Alert!")
            play_alert = True

# --- UI: HEADER ---
st.title("SST ELITE TERMINAL")
if alerts:
    for alert in alerts: st.toast(alert)
if play_alert: play_sound()

c1, c2, c3 = st.columns([4, 1, 1.5])
input_tickers = c1.text_input("", placeholder="Quick Add (e.g. MSFT, AMZN, GOOGL)", key="ticker_input").upper()

if c2.button("➕ ADD", use_container_width=True):
    if input_tickers:
        new_tickers = [t.strip() for t in input_tickers.split(',') if t.strip()]
        for t in new_tickers:
            if t not in st.session_state.watchlist: st.session_state.watchlist.append(t)
        st.session_state.current_ticker = new_tickers[0]
        st.rerun()

if c3.button("🔄 SYNC & SORT", use_container_width=True):
    st.session_state.watchlist.sort(key=lambda x: (st.session_state.last_results.get(x, {}).get('priority', 0), 
                                                 st.session_state.last_results.get(x, {}).get('score', 0)), reverse=True)
    st.rerun()

# --- UI: MAIN CHART ---
active_data = st.session_state.last_results.get(st.session_state.current_ticker) or get_analysis(st.session_state.current_ticker)

if active_data:
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Price</div><div class="kpi-value" style="color:{"#3fb950" if active_data["change"] >= 0 else "#f85149"}">${active_data["price"]:.2f}</div></div>', unsafe_allow_html=True)
    with k2: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Momentum Score</div><div class="kpi-value">{active_data["score"]}</div></div>', unsafe_allow_html=True)
    with k3: st.markdown(f'<div class="kpi-card"><div class="kpi-label">MACD</div><div class="kpi-value" style="color:{"#3fb950" if active_data["macd_bull"] else "#f85149"}">{"BULL" if active_data["macd_bull"] else "BEAR"}</div></div>', unsafe_allow_html=True)
    with k4: st.markdown(f'<div class="kpi-card"><div class="kpi-label">EMA Stack</div><div class="kpi-value" style="color:{"#3fb950" if active_data["ema_ok"] else "#f85149"}">{"HEALTHY" if active_data["ema_ok"] else "WEAK"}</div></div>', unsafe_allow_html=True)
    with k5: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Signal</div><div class="kpi-value" style="color:{"#3fb950" if active_data["signal"] != "NONE" else "#8b949e"}">{active_data["signal"]}</div></div>', unsafe_allow_html=True)

    tv_html = f"""<div id="tv-chart" style="height: 480px; border: 1px solid #30363d; border-radius: 12px; margin-top: 15px;"></div>
    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>new TradingView.widget({{"autosize": true, "symbol": "{active_data['symbol']}", "interval": "D", "theme": "dark", "container_id": "tv-chart"}});</script>"""
    components.html(tv_html, height=500)

# --- UI: PROFESSIONAL WATCHLIST ---
st.write("---")
st.subheader("Market Monitor")

# Table Header
st.markdown("""
    <div style="display: flex; padding: 10px 20px; color: #8b949e; font-size: 0.7rem; text-transform: uppercase; font-weight: bold; border-bottom: 1px solid #30363d;">
        <span style="flex: 1;">Ticker</span>
        <span style="flex: 1; text-align: right;">Price</span>
        <span style="flex: 1; text-align: center;">Score</span>
        <span style="flex: 1; text-align: right;">Status</span>
        <span style="flex: 1; text-align: right;">Actions</span>
    </div>
""", unsafe_allow_html=True)

for item in st.session_state.watchlist:
    w = st.session_state.last_results.get(item)
    if w:
        b_class = "badge-trend" if w['signal'] == "TREND" else "badge-breakout" if w['signal'] == "BREAKOUT" else "badge-none"
        p_clr = "#3fb950" if w['change'] >= 0 else "#f85149"
        dot_clr = "#3fb950" if w['score'] > 60 else "#d29922" if w['score'] > 40 else "#f85149"
        
        # Row Layout
        row_html = f"""
            <div class="wl-row">
                <div class="wl-col-sym">{item}</div>
                <div class="wl-col-price" style="color:{p_clr};">${w['price']:.2f}</div>
                <div class="wl-col-score"><span class="dot" style="background:{dot_clr};"></span>{w['score']}</div>
                <div class="wl-col-sig"><span class="badge {b_class}">{w['signal']}</span></div>
                <div style="flex: 1; display: flex; justify-content: flex-end; gap: 5px;" id="btn-{item}"></div>
            </div>
        """
        st.markdown(row_html, unsafe_allow_html=True)
        
        # Buttons positioned under the row using columns for alignment
        bc1, bc2, bc3, bc4, bc5 = st.columns([1,1,1,1,1])
        with bc5:
            bt1, bt2 = st.columns(2)
            if bt1.button("VIEW", key=f"v_{item}"):
                st.session_state.current_ticker = item
                st.rerun()
            if bt2.button("DEL", key=f"d_{item}"):
                st.session_state.watchlist.remove(item)
                st.rerun()









































