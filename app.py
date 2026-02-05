import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas_ta as ta
import pandas as pd
import time

# 1. Page Configuration
st.set_page_config(page_title="SST ELITE TERMINAL", layout="wide")

st.markdown("""
    <style>
    .block-container { padding: 1.5rem !important; background-color: #050608; }
    
    /* KPI Cards */
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

    /* Watchlist Grid Cards */
    .wl-card {
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 5px;
        transition: transform 0.2s;
    }
    
    /* Alert Borders & Glow */
    .alert-trend { 
        border: 2px solid #3fb950 !important; 
        box-shadow: 0 0 15px rgba(63, 185, 80, 0.4); 
    }
    .alert-breakout { 
        border: 2px solid #2563eb !important; 
        box-shadow: 0 0 15px rgba(37, 99, 235, 0.4); 
    }

    .wl-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
    .wl-symbol { font-size: 1.2rem; font-weight: 900; color: #ffffff; }
    .wl-price { font-family: 'Courier New', monospace; font-weight: 700; font-size: 1.1rem; }
    
    /* Score Colors */
    .score-high { color: #3fb950 !important; text-shadow: 0 0 10px rgba(63, 185, 80, 0.4); }
    .score-mid { color: #d29922 !important; text-shadow: 0 0 10px rgba(210, 153, 34, 0.4); }
    .score-low { color: #f85149 !important; text-shadow: 0 0 10px rgba(248, 81, 73, 0.4); }
    
    /* Signal Badges */
    .badge {
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.65rem;
        font-weight: 900;
        text-transform: uppercase;
    }
    .badge-trend { background: rgba(63, 185, 80, 0.15); color: #3fb950; border: 1px solid #3fb950; }
    .badge-breakout { background: rgba(37, 99, 235, 0.15); color: #2563eb; border: 1px solid #2563eb; }
    .badge-none { background: rgba(139, 148, 158, 0.1); color: #8b949e; border: 1px solid #30363d; }
    
    .stButton button { 
        background-color: #21262d; border: 1px solid #30363d; color: #c9d1d9;
        font-size: 0.7rem; width: 100%; height: 30px;
    }
    .stButton button:hover { border-color: #58a6ff; color: #58a6ff; }
    </style>
    """, unsafe_allow_html=True)

# Audio helper
def play_notification_sound():
    sound_html = """
    <audio autoplay>
        <source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg">
    </audio>
    """
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

# --- SYNC DATA & ALERTS ---
active_alerts = []
trigger_sound = False

for t in st.session_state.watchlist:
    res = get_analysis(t)
    if res: 
        st.session_state.last_results[t] = res
        if res['score'] >= 90:
            active_alerts.append({"msg": f"🔥 {t}: Extreme Momentum ({res['score']})", "type": "warning"})
        if res['signal'] in ["BREAKOUT", "TREND"]:
            active_alerts.append({"msg": f"📈 {t}: {res['signal']} Signal Detected!", "type": "success"})
            trigger_sound = True

# --- UI: HEADER & LONG NOTIFICATIONS ---
st.title("SST ELITE TERMINAL")

# Deze banners blijven staan zolang de conditie waar is (veel langer dan 10 sec)
if active_alerts:
    for alert in active_alerts:
        if alert["type"] == "warning":
            st.warning(alert["msg"])
        else:
            st.success(alert["msg"])
    
    if trigger_sound:
        play_notification_sound()

# --- UI: CONTROLS ---
c1, c2, c3 = st.columns([4, 1, 1.5])
input_tickers = c1.text_input("", placeholder="Quick Add Tickers", key="ticker_input").upper()

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

# --- UI: MAIN KPI ---
active_data = st.session_state.last_results.get(st.session_state.current_ticker) or get_analysis(st.session_state.current_ticker)

if active_data:
    s_val = active_data["score"]
    s_class = "score-high" if s_val >= 60 else "score-mid" if s_val >= 40 else "score-low"
    
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Price</div><div class="kpi-value" style="color:{"#3fb950" if active_data["change"] >= 0 else "#f85149"}">${active_data["price"]:.2f}</div></div>', unsafe_allow_html=True)
    with k2: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Momentum Score</div><div class="kpi-value {s_class}">{s_val}</div></div>', unsafe_allow_html=True)
    with k3: st.markdown(f'<div class="kpi-card"><div class="kpi-label">MACD</div><div class="kpi-value" style="color:{"#3fb950" if active_data["macd_bull"] else "#f85149"}">{"BULL" if active_data["macd_bull"] else "BEAR"}</div></div>', unsafe_allow_html=True)
    with k4: st.markdown(f'<div class="kpi-card"><div class="kpi-label">EMA Stack</div><div class="kpi-value" style="color:{"#3fb950" if active_data["ema_ok"] else "#f85149"}">{"HEALTHY" if active_data["ema_ok"] else "WEAK"}</div></div>', unsafe_allow_html=True)
    with k5: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Signal</div><div class="kpi-value" style="color:{"#3fb950" if active_data["signal"] != "NONE" else "#8b949e"}">{active_data["signal"]}</div></div>', unsafe_allow_html=True)

    tv_html = f"""<div id="tv-chart" style="height: 480px; border: 1px solid #30363d; border-radius: 12px; margin-top: 15px;"></div>
    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>new TradingView.widget({{"autosize": true, "symbol": "{active_data['symbol']}", "interval": "D", "theme": "dark", "container_id": "tv-chart"}});</script>"""
    components.html(tv_html, height=500)

# --- UI: 3-COLUMN WATCHLIST GRID ---
st.write("---")
st.subheader("Market Monitor")

cols = st.columns(3)
for idx, item in enumerate(st.session_state.watchlist):
    w = st.session_state.last_results.get(item)
    if w:
        alert_class = ""
        if w['signal'] == "TREND": alert_class = "alert-trend"
        elif w['signal'] == "BREAKOUT": alert_class = "alert-breakout"
        
        b_class = "badge-trend" if w['signal'] == "TREND" else "badge-breakout" if w['signal'] == "BREAKOUT" else "badge-none"
        p_clr = "#3fb950" if w['change'] >= 0 else "#f85149"
        
        sw_val = w['score']
        sw_class = "score-high" if sw_val >= 60 else "score-mid" if sw_val >= 40 else "score-low"
        
        with cols[idx % 3]:
            st.markdown(f"""
                <div class="wl-card {alert_class}">
                    <div class="wl-header">
                        <span class="wl-symbol">{item}</span>
                        <span class="badge {b_class}">{w['signal']}</span>
                    </div>
                    <div class="wl-header">
                        <span class="wl-price" style="color:{p_clr};">${w['price']:.2f}</span>
                        <span style="font-size: 0.75rem; color:#8b949e;">Score: <b class="{sw_class}" style="font-size:1rem;">{sw_val}</b></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            btn1, btn2 = st.columns(2)
            if btn1.button("VIEW", key=f"v_{item}"):
                st.session_state.current_ticker = item
                st.rerun()
            if btn2.button("DEL", key=f"d_{item}"):
                st.session_state.watchlist.remove(item)
                st.rerun()









































