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

# --- HELPERS ---
def load_watchlist():
    if os.path.exists(WATCHLIST_FILE):
        try: return pd.read_csv(WATCHLIST_FILE)['ticker'].tolist()
        except: pass
    return ["NVDA", "AAPL", "TSLA"]

def save_watchlist(watchlist):
    pd.DataFrame({'ticker': watchlist}).to_csv(WATCHLIST_FILE, index=False)

# --- STYLING ---
st.markdown("""
    <style>
    .block-container { padding: 1rem !important; background-color: #050608; }
    .kpi-card { background: linear-gradient(145deg, #0d1117, #161b22); border: 1px solid #30363d; padding: 15px; border-radius: 12px; text-align: center; }
    .kpi-value { font-size: 1.6rem; font-weight: 800; }
    .kpi-label { font-size: 0.65rem; color: #8b949e; text-transform: uppercase; }
    .score-high { color: #3fb950 !important; text-shadow: 0 0 12px rgba(63, 185, 80, 0.6); }
    .score-mid { color: #d29922 !important; text-shadow: 0 0 10px rgba(210, 153, 34, 0.6); }
    .score-low { color: #f85149 !important; text-shadow: 0 0 10px rgba(248, 81, 73, 0.6); }
    .text-bull { color: #3fb950 !important; }
    .text-bear { color: #f85149 !important; }
    .earnings-imminent { 
        background: rgba(248, 81, 73, 0.15); border: 1px solid #f85149; color: #f85149; 
        padding: 12px; border-radius: 8px; font-weight: bold; text-align: center;
        animation: blink 2s infinite; margin-bottom: 15px;
    }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.6; } 100% { opacity: 1; } }
    .wl-card { background: #0d1117; border: 1px solid #30363d; border-radius: 12px; padding: 15px; margin-bottom: 5px; }
    .score-label-white { color: #ffffff !important; font-weight: bold; }
    .stButton > button { background-color: #1c2128 !important; color: #ffffff !important; border: 1px solid #444c56 !important; }
    
    /* Guide Styling */
    .guide-box { background: #0d1117; border: 1px solid #30363d; padding: 25px; border-radius: 15px; line-height: 1.6; }
    .guide-header { color: #2563eb; font-size: 1.5rem; font-weight: bold; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA FUNCTIES ---
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
        earn_date = get_earnings_info(ticker_symbol)
        return {"symbol": ticker_symbol, "price": price, "score": score, "signal": signal, 
                "macd_bull": ml > sl, "ema_ok": price > e50, "change": change, "earnings": earn_date}
    except: return None

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("SST NAVIGATION")
    page = st.radio("Go to:", ["Elite Terminal", "User Guide"])
    st.write("---")
    st.info("v2.1 - Powered by Team SST")

# --- PAGE 1: TERMINAL ---
if page == "Elite Terminal":
    # State & Sync
    if 'watchlist' not in st.session_state: st.session_state.watchlist = load_watchlist()
    if 'current_ticker' not in st.session_state: st.session_state.current_ticker = st.session_state.watchlist[0]
    if 'last_results' not in st.session_state: st.session_state.last_results = {}

    for t in st.session_state.watchlist:
        res = get_analysis(t)
        if res: st.session_state.last_results[t] = res

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
    if c3.button("🔄 SYNC", use_container_width=True): st.rerun()

    active_data = st.session_state.last_results.get(st.session_state.current_ticker)
    if active_data:
        today = datetime.now().date()
        earn_str = "N/A"
        raw_earn = active_data.get("earnings")
        if raw_earn:
            earn_date = raw_earn.date() if hasattr(raw_earn, 'date') else raw_earn
            earn_str = earn_date.strftime("%d %b")
            days_diff = (earn_date - today).days
            if 0 <= days_diff <= 2:
                st.markdown(f'<div class="earnings-imminent">⚠️ EARNINGS WAARSCHUWING: {active_data["symbol"]} over {days_diff} dag(en) ({earn_str})</div>', unsafe_allow_html=True)

        s_val = active_data["score"]
        s_class = "score-high" if s_val >= 60 else "score-mid" if s_val >= 40 else "score-low"
        p_class = "text-bull" if active_data["change"] >= 0 else "text-bear"
        
        k1, k2, k3, k4, k5 = st.columns(5)
        with k1: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Price</div><div class="kpi-value {p_class}">${active_data["price"]:.2f}</div></div>', unsafe_allow_html=True)
        with k2: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Score</div><div class="kpi-value {s_class}">{s_val}</div></div>', unsafe_allow_html=True)
        with k3: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Next Earnings</div><div class="kpi-value" style="font-size:1.2rem; color:white;">{earn_str}</div></div>', unsafe_allow_html=True)
        with k4: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Health</div><div class="kpi-value {"text-bull" if active_data["ema_ok"] else "text-bear"}">{"OK" if active_data["ema_ok"] else "WEAK"}</div></div>', unsafe_allow_html=True)
        with k5: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Signal</div><div class="kpi-value" style="color:white;">{active_data["signal"]}</div></div>', unsafe_allow_html=True)

        st.write("")
        col_chart, col_alerts = st.columns([3, 1])
        with col_chart:
            tv_html = f"""<div id="tv-chart" style="height: 500px; border: 1px solid #30363d; border-radius: 12px;"></div>
            <script src="https://s3.tradingview.com/tv.js"></script>
            <script>new TradingView.widget({{"autosize": true, "symbol": "{active_data['symbol']}", "interval": "D", "theme": "dark", "container_id": "tv-chart"}});</script>"""
            components.html(tv_html, height=510)
        
        with col_alerts:
            st.markdown('<p style="color:#8b949e; font-size:0.75rem; font-weight:bold; margin-bottom:10px;">SIGNALS & CALENDAR</p>', unsafe_allow_html=True)
            with st.container(height=465, border=True):
                for item in st.session_state.watchlist:
                    r = st.session_state.last_results.get(item)
                    if r:
                        if r.get("earnings"):
                            try:
                                ed = r["earnings"].date() if hasattr(r["earnings"], 'date') else r["earnings"]
                                if 0 <= (ed - today).days <= 2:
                                    st.markdown(f'<div style="color:#f85149; font-size:0.8rem; padding:5px; border:1px solid #f85149; border-radius:5px; margin-bottom:10px; font-weight:bold;">🚨 {item} EARNINGS: {ed.strftime("%d %b")}</div>', unsafe_allow_html=True)
                            except: pass
                        if r['score'] >= 85: st.markdown(f'<div style="color:#d29922; font-size:0.85rem; padding:8px 0; border-bottom:1px solid #30363d; font-weight:600;">🔥 {item}: Momentum ({r["score"]})</div>', unsafe_allow_html=True)
                        if r['signal'] == "BREAKOUT": st.markdown(f'<div style="color:#2563eb; font-size:0.85rem; padding:8px 0; border-bottom:1px solid #30363d; font-weight:600;">📈 {item}: BREAKOUT!</div>', unsafe_allow_html=True)

    st.write("---")
    cols = st.columns(3)
    for idx, item in enumerate(st.session_state.watchlist):
        w = st.session_state.last_results.get(item)
        if w:
            sw_c = "score-high" if w['score'] >= 60 else "score-mid" if w['score'] >= 40 else "score-low"
            price_c = "text-bull" if w['change'] >= 0 else "text-bear"
            sig_color = "color:#3fb950;" if w['signal'] == "TREND" else "color:#2563eb;" if w['signal'] == "BREAKOUT" else "color:#8b949e;"
            with cols[idx % 3]:
                st.markdown(f"""<div class="wl-card">
                    <div style="display:flex; justify-content:space-between;"><b>{item}</b><span style="{sig_color} font-size:0.75rem; font-weight:bold;">{w['signal']}</span></div>
                    <div style="font-size:0.7rem; color:#8b949e; margin-top:2px;">Next Earnings: {w.get("earnings").strftime("%d/%m") if w.get("earnings") and hasattr(w.get("earnings"), 'strftime') else "N/A"}</div>
                    <div style="display:flex; justify-content:space-between; margin-top:8px;">
                        <span class="{price_c}" style="font-weight:bold;">${w['price']:.2f}</span>
                        <span class="score-label-white">Score: <span class="{sw_c}">{w['score']}</span></span>
                    </div></div>""", unsafe_allow_html=True)
                b1, b2 = st.columns(2)
                if b1.button("VIEW", key=f"v_{item}", use_container_width=True): 
                    st.session_state.current_ticker = item
                    st.rerun()
                if b2.button("DEL", key=f"d_{item}", use_container_width=True): 
                    st.session_state.watchlist.remove(item)
                    save_watchlist(st.session_state.watchlist)
                    st.rerun()

# --- PAGE 2: USER GUIDE ---
elif page == "User Guide":
    st.title("SST USER GUIDE")
    
    st.markdown("""
    <div class="guide-box">
        <div class="guide-header">Explanation of the SST Elite Terminal</div>
        <p>At the top of the panel, you can select a stock of your choice. The system will then immediately analyze the stock and provide a score.</p>
        
        <p><strong>AI Score & Health:</strong><br>
        The first box shows the <b>AI Score</b>. The AI method behind this score evaluates the short-term potential of the stock. 
        The higher the score, the greater the chance that the stock will rise. 
        Under <b>Health</b>, you will find the strength of the overall technical analysis that supports this score.</p>
        
        <p><strong>Signals:</strong><br>
        Under <b>Signal</b>, you will see the active signal if one is available, for example a <b>Breakout</b>.</p>
        
        <p><strong>How to use:</strong><br>
        You can use the terminal in two ways:
        <ul>
            <li>By following the AI Score, or</li>
            <li>By using the Signal.</li>
        </ul>
        Of course, you can also choose to combine both.</p>
        
        <p><strong>Watchlist & Sync:</strong><br>
        When you press <b>Add</b>, the stock will be added to the watchlist below the chart. 
        When you press the <b>Sync</b> button, the latest score is retrieved, ensuring that you are always up to date.</p>
        
        <p><strong>Active Alerts:</strong><br>
        Next to the chart, you will also see the signals and earnings alerts that are currently active.</p>
        
        <p><i>Good luck with the terminal.</i><br>
        <strong>Team SST (Swingstocktraders)</strong></p>
    </div>
    """, unsafe_allow_html=True)











































