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
    
    /* KPI Kaarten */
    .kpi-card {
        background: linear-gradient(145deg, #0d1117, #161b22);
        border: 1px solid #30363d;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
    }
    .kpi-value { font-size: 1.6rem; font-weight: 900; color: #ffffff; }
    .kpi-label { font-size: 0.75rem; color: #8b949e; text-transform: uppercase; }
    
    /* Watchlist Grid Blokken */
    .wl-box {
        background-color: #0d1117;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
        transition: 0.3s;
    }
    
    /* Oplichtende Randen (Glow effect) */
    .glow-green {
        border: 2px solid #3fb950 !important;
        box-shadow: 0 0 10px rgba(63, 185, 80, 0.4);
        animation: pulse-green 2s infinite;
    }
    .glow-blue {
        border: 2px solid #2563eb !important;
        box-shadow: 0 0 10px rgba(37, 99, 235, 0.4);
        animation: pulse-blue 2s infinite;
    }
    
    @keyframes pulse-green {
        0% { box-shadow: 0 0 5px rgba(63, 185, 80, 0.2); }
        50% { box-shadow: 0 0 15px rgba(63, 185, 80, 0.6); }
        100% { box-shadow: 0 0 5px rgba(63, 185, 80, 0.2); }
    }
    @keyframes pulse-blue {
        0% { box-shadow: 0 0 5px rgba(37, 99, 235, 0.2); }
        50% { box-shadow: 0 0 15px rgba(37, 99, 235, 0.6); }
        100% { box-shadow: 0 0 5px rgba(37, 99, 235, 0.2); }
    }

    .stButton button { 
        border-radius: 4px; padding: 0px 5px; font-size: 0.7rem; height: 26px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. State Management
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = ["NVDA", "AAPL", "BTC-USD", "ETH-USD", "TSLA", "MSFT", "AMZN"]
if 'current_ticker' not in st.session_state:
    st.session_state.current_ticker = "NVDA"

# 3. Analyse Functie
def get_analysis(ticker_symbol):
    try:
        df = yf.download(ticker_symbol, period="1y", interval="1d", progress=False, auto_adjust=True)
        if df.empty or len(df) < 200: return None
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)

        price = df['Close'].iloc[-1]
        change = ((price - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100
        rsi = ta.rsi(df['Close'], length=14).iloc[-1]
        macd = ta.macd(df['Close'])
        ml, sl = macd.iloc[-1, 0], macd.iloc[-1, 2]
        e20, e50, e200 = ta.ema(df['Close'], 20).iloc[-1], ta.ema(df['Close'], 50).iloc[-1], ta.ema(df['Close'], 200).iloc[-1]
        upper_bb = ta.bbands(df['Close'], length=20).iloc[-1, 2]
        vol_avg = df['Volume'].rolling(20).mean().iloc[-1]
        vol_curr = df['Volume'].iloc[-1]

        score = max(min(int(50 + (change * 12)), 99), 5)
        
        signal_val = 0
        signal_text = "NONE"
        if price > upper_bb and ml > sl and price > e50 and vol_curr > vol_avg:
            signal_text = "BREAKOUT"; signal_val = 2
        elif price > e20 and price > e50 and price > e200 and ml > sl and 40 <= rsi <= 60:
            signal_text = "TREND"; signal_val = 1

        return {
            "symbol": ticker_symbol, "price": price, "score": score, "signal": signal_text, 
            "priority": signal_val, "macd_bull": ml > sl, "ema_ok": price > e20 and price > e50 and price > e200, "change": change
        }
    except: return None

# --- UI: TOP BAR ---
st.title("🚀 SST ELITE DASHBOARD")
c1, c2, c3 = st.columns([4, 1, 1.5])
quick_t = c1.text_input("", placeholder="Ticker toevoegen...", label_visibility="collapsed").upper()

if c2.button("➕ ADD", use_container_width=True):
    if quick_t and quick_t not in st.session_state.watchlist:
        st.session_state.watchlist.append(quick_t)
        st.rerun()

if c3.button("🔍 SCAN & SORTEER", use_container_width=True):
    with st.spinner('Scanning...'):
        results = [get_analysis(t) for t in st.session_state.watchlist if get_analysis(t)]
        results.sort(key=lambda x: (x['priority'], x['score']), reverse=True)
        st.session_state.watchlist = [x['symbol'] for x in results]
        st.rerun()

# --- UI: KPI & CHART ---
active_data = get_analysis(st.session_state.current_ticker)
if active_data:
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Price</div><div class="kpi-value">${active_data["price"]:.2f}</div></div>', unsafe_allow_html=True)
    with k2: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Score</div><div class="kpi-value">{active_data["score"]}</div></div>', unsafe_allow_html=True)
    with k3: st.markdown(f'<div class="kpi-card"><div class="kpi-label">MACD</div><div class="kpi-value">{"BULL" if active_data["macd_bull"] else "BEAR"}</div></div>', unsafe_allow_html=True)
    with k4: st.markdown(f'<div class="kpi-card"><div class="kpi-label">EMA</div><div class="kpi-value">{"OK" if active_data["ema_ok"] else "ZWAK"}</div></div>', unsafe_allow_html=True)
    with k5: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Signal</div><div class="kpi-value">{active_data["signal"]}</div></div>', unsafe_allow_html=True)

    tv_html = f"""<div id="tv-chart" style="height: 450px; border: 1px solid #30363d; border-radius: 12px; margin-top: 15px;"></div>
    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>new TradingView.widget({{"autosize": true, "symbol": "{active_data['symbol']}", "interval": "D", "theme": "dark", "container_id": "tv-chart"}});</script>"""
    components.html(tv_html, height=470)

# --- UI: GRID WATCHLIST ---
st.write("### 📋 Watchlist Scanner")
cols = st.columns(3) # Drie kolommen naast elkaar

for idx, item in enumerate(st.session_state.watchlist):
    w = get_analysis(item)
    if w:
        glow_class = ""
        status_color = "#8b949e"
        if w['signal'] == "TREND": 
            glow_class = "glow-green"; status_color = "#3fb950"
        elif w['signal'] == "BREAKOUT": 
            glow_class = "glow-blue"; status_color = "#2563eb"
        
        with cols[idx % 3]:
            st.markdown(f"""
                <div class="wl-box {glow_class}">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color:white; font-weight:900; font-size:1.1rem;">{item}</span>
                        <span style="color:{status_color}; font-weight:bold; font-size:0.8rem;">{w['signal']}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top:5px;">
                        <span style="color:#8b949e; font-size:0.8rem;">Score: <b>{w['score']}</b></span>
                        <span style="color:#8b949e; font-size:0.8rem;">Price: <b>${w['price']:.2f}</b></span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Knoppen onder het blok
            btn_col1, btn_col2 = st.columns([1, 1])
            if btn_col1.button(f"Bekijk {item}", key=f"v_{item}", use_container_width=True):
                st.session_state.current_ticker = item
                st.rerun()
            if btn_col2.button(f"Wis {item}", key=f"d_{item}", use_container_width=True):
                st.session_state.watchlist.remove(item)
                st.rerun()






































