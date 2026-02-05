import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas_ta as ta
import pandas as pd

# 1. Pagina Configuratie
st.set_page_config(page_title="SST SMART TERMINAL", layout="wide")

# CSS voor styling en kleuren
st.markdown("""
    <style>
    .block-container { padding: 10px !important; background-color: #050608; }
    [data-testid="stSidebar"] { background-color: #0d1117; }
    .stButton button { border-radius: 8px; height: 60px; font-weight: bold; font-size: 1.1rem; }
    /* Signaal Kleuren voor de Watchlist */
    .signal-none { border: 1px solid #30363d !important; }
    .signal-green { border: 3px solid #3fb950 !important; background-color: rgba(63, 185, 80, 0.1) !important; }
    .signal-blue { border: 3px solid #2563eb !important; background-color: rgba(37, 99, 235, 0.1) !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. State Management
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = ["NVDA", "AAPL", "BTC-USD", "TSLA", "MSFT"]
if 'current_ticker' not in st.session_state:
    st.session_state.current_ticker = "NVDA"

# 3. Functie voor Data & Notificatie Check
def analyze_ticker(ticker_symbol):
    try:
        df = yf.download(ticker_symbol, period="1y", interval="1d", progress=False, auto_adjust=True)
        if df.empty or len(df) < 200: return None, "none"
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)

        # Indicatoren
        rsi = ta.rsi(df['Close'], length=14).iloc[-1]
        macd = ta.macd(df['Close'])
        m_l, s_l = macd.iloc[-1, 0], macd.iloc[-1, 2]
        e20, e50, e200 = ta.ema(df['Close'], 20).iloc[-1], ta.ema(df['Close'], 50).iloc[-1], ta.ema(df['Close'], 200).iloc[-1]
        bb = ta.bbands(df['Close'], length=20)
        upper_bb = bb.iloc[-1, 2]
        price = df['Close'].iloc[-1]
        avg_vol = df['Volume'].rolling(20).mean().iloc[-1]
        curr_vol = df['Volume'].iloc[-1]

        # Notificatie Logica
        signal = "none"
        # 1. Groen: Prijs > EMA 20,50,200 & MACD Bull & RSI 40-60
        if price > e20 and price > e50 and price > e200 and m_l > s_l and 40 <= rsi <= 60:
            signal = "green"
        # 2. Blauw: Prijs > Upper BB & MACD Bull & Prijs > EMA50 & Volume stijgt
        elif price > upper_bb and m_l > s_l and price > e50 and curr_vol > avg_vol:
            signal = "blue"

        # Basis data voor dashboard
        stoch = ta.stoch(df['High'], df['Low'], df['Close'], k=14, d=3, smooth_k=3)
        return {
            "price": price, "rsi": rsi, "macd_bull": m_l > s_l, 
            "stoch_k": stoch.iloc[-1, 0], "stoch_d": stoch.iloc[-1, 1],
            "stoch_prev_k": stoch.iloc[-2, 0], "ema_all": price > e20 and price > e50 and price > e200,
            "bb_break": price > upper_bb, "change": ((price - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100
        }, signal
    except: return None, "none"

# --- SIDEBAR (Alleen voor toevoegen) ---
with st.sidebar:
    st.title("SST CONTROL")
    new_t = st.text_input("Ticker Toevoegen").upper()
    if st.button("➕ Voeg toe"):
        if new_t and new_t not in st.session_state.watchlist:
            st.session_state.watchlist.append(new_t)
            st.rerun()

# --- HOOFDSCHERM ---
active_ticker = st.session_state.current_ticker
data, current_signal = analyze_ticker(active_ticker)

if data:
    # Score berekening
    score = max(min(int(50 + (data['change'] * 12)), 99), 5)
    
    # Dashboard HTML
    terminal_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@700;900&display=swap" rel="stylesheet">
        <style>
            body {{ background-color: #050608; color: white; font-family: 'Inter', sans-serif; margin: 0; }}
            .card {{ background: #0d1117; border: 1px solid #30363d; padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 10px; }}
            .indicator-panel {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin-bottom: 15px; }}
            .ind-card {{ background: #0d1117; border: 2px solid #30363d; padding: 10px; border-radius: 8px; text-align: center; font-size: 0.75rem; }}
            .status-green {{ border-color: #3fb950; color: #3fb950; }}
            #tv-chart {{ height: 500px; border-radius: 15px; border: 1px solid #30363d; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div style="font-size: 0.8rem; color: #8b949e;">MOMENTUM SCORE: {active_ticker}</div>
            <div style="font-size: 3rem; font-weight: 900; color: {'#3fb950' if score > 60 else '#f85149'}">{score}</div>
        </div>
        <div class="indicator-panel">
            <div class="ind-card {'status-green' if 30 <= data['rsi'] <= 65 else ''}">RSI<br>{data['rsi']:.1f}</div>
            <div class="ind-card {'status-green' if data['stoch_k'] > data['stoch_d'] else ''}">STOCH<br>{data['stoch_k']:.1f}</div>
            <div class="ind-card {'status-green' if data['macd_bull'] else ''}">MACD<br>{'BULL' if data['macd_bull'] else 'BEAR'}</div>
            <div class="ind-card {'status-green' if data['ema_all'] else ''}">EMA CLOUD</div>
            <div class="ind-card {'status-green' if data['bb_break'] else ''}">BOLLINGER</div>
        </div>
        <div id="tv-chart"></div>
        <script src="https://s3.tradingview.com/tv.js"></script>
        <script>new TradingView.widget({{"autosize": true, "symbol": "{active_ticker}", "interval": "D", "theme": "dark", "container_id": "tv-chart"}});</script>
    </body>
    </html>
    """
    components.html(terminal_html, height=720)

# --- WATCHLIST ONDER DE CHART ---
st.write("### 🖥️ Live Watchlist Scanners")
cols = st.columns(4) # 4 aandelen per rij

for index, item in enumerate(st.session_state.watchlist):
    _, signal = analyze_ticker(item)
    
    # CSS class toewijzen op basis van signaal
    btn_type = "signal-none"
    if signal == "green": btn_type = "signal-green"
    elif signal == "blue": btn_type = "signal-blue"
    
    with cols[index % 4]:
        # Unieke knoppen per aandeel
        if st.button(f"{item}", key=f"btn_{item}", use_container_width=True, help=f"Klik om {item} te bekijken"):
            st.session_state.current_ticker = item
            st.rerun()
        if st.button("Verwijder", key=f"del_{item}", use_container_width=True):
            st.session_state.watchlist.remove(item)
            st.rerun()




































