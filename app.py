import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas_ta as ta
import pandas as pd

# 1. Pagina Configuratie
st.set_page_config(page_title="SST PRO TERMINAL", layout="wide")

st.markdown("""
    <style>
    .block-container { padding: 10px !important; background-color: #050608; }
    .stButton button { border-radius: 4px; height: auto; padding: 5px 10px; }
    /* Signaal Kleuren voor de Tabel */
    .row-green { border: 2px solid #3fb950 !important; background-color: rgba(63, 185, 80, 0.1); }
    .row-blue { border: 2px solid #2563eb !important; background-color: rgba(37, 99, 235, 0.1); }
    div[data-testid="stMetric"] { background-color: #0d1117; border: 1px solid #30363d; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. State Management
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = ["NVDA", "AAPL", "BTC-USD", "ETH-USD"]
if 'current_ticker' not in st.session_state:
    st.session_state.current_ticker = "NVDA"

# 3. Analyse Functie
def fetch_full_analysis(ticker_symbol):
    try:
        df = yf.download(ticker_symbol, period="1y", interval="1d", progress=False, auto_adjust=True)
        if df.empty or len(df) < 200: return None
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)

        # Indicatoren berekenen
        rsi = ta.rsi(df['Close'], length=14).iloc[-1]
        macd = ta.macd(df['Close'])
        ml, sl = macd.iloc[-1, 0], macd.iloc[-1, 2]
        e20, e50, e200 = ta.ema(df['Close'], 20).iloc[-1], ta.ema(df['Close'], 50).iloc[-1], ta.ema(df['Close'], 200).iloc[-1]
        bb = ta.bbands(df['Close'], length=20)
        upper_bb = bb.iloc[-1, 2]
        price = df['Close'].iloc[-1]
        prev_price = df['Close'].iloc[-2]
        vol_avg = df['Volume'].rolling(20).mean().iloc[-1]
        vol_curr = df['Volume'].iloc[-1]

        # Notificatie checks
        signal = "None"
        if price > e20 and price > e50 and price > e200 and ml > sl and 40 <= rsi <= 60:
            signal = "Trend Green"
        elif price > upper_bb and ml > sl and price > e50 and vol_curr > vol_avg:
            signal = "Breakout Blue"

        return {
            "symbol": ticker_symbol, "price": price, "change": ((price - prev_price)/prev_price)*100,
            "rsi": rsi, "macd_bull": ml > sl, "ema_ok": price > e20 and price > e50 and price > e200,
            "bb_break": price > upper_bb, "signal": signal
        }
    except: return None

# --- UI: TOP BAR (Search & Add) ---
st.title("🚀 SST SMART TERMINAL")
c_search, c_add, _ = st.columns([3, 1, 4])
quick_ticker = c_search.text_input("Snelzoeken / Ticker invoegen", placeholder="Bijv. TSLA, MSFT, BTC-USD").upper()

if c_add.button("➕ Zet in Watchlist"):
    if quick_ticker and quick_ticker not in st.session_state.watchlist:
        st.session_state.watchlist.append(quick_ticker)
        st.session_state.current_ticker = quick_ticker
        st.rerun()
elif quick_ticker: # Direct chart updaten bij typen zonder per se toe te voegen
    st.session_state.current_ticker = quick_ticker

# --- UI: MAIN DASHBOARD ---
active_ticker = st.session_state.current_ticker
main_data = fetch_full_analysis(active_ticker)

if main_data:
    # Metrics Rij
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Prijs", f"${main_data['price']:.2f}", f"{main_data['change']:.2f}%")
    m2.metric("RSI", f"{main_data['rsi']:.1f}")
    m3.metric("MACD", "BULL" if main_data['macd_bull'] else "BEAR")
    m4.metric("EMA Cloud", "BOVEN" if main_data['ema_ok'] else "ONDER")
    m5.metric("Signaal", main_data['signal'])

    # TradingView Chart
    terminal_html = f"""
    <div id="tv-chart" style="height: 500px; border: 1px solid #30363d; border-radius: 12px;"></div>
    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>new TradingView.widget({{"autosize": true, "symbol": "{active_ticker}", "interval": "D", "theme": "dark", "container_id": "tv-chart"}});</script>
    """
    components.html(terminal_html, height=520)

# --- UI: LIVE WATCHLIST GRID ---
st.write("### 📋 Watchlist Scanner")
st.write("Klik op een ticker om de grafiek te laden.")

# Header voor de lijst
h1, h2, h3, h4, h5, h6 = st.columns([1, 1, 1, 1, 2, 1])
h1.caption("TICKER")
h2.caption("PRIJS")
h3.caption("RSI")
h4.caption("MACD")
h5.caption("STATUS")
h6.caption("ACTIE")

for item in st.session_state.watchlist:
    w_data = fetch_full_analysis(item)
    if w_data:
        # Bepaal kleur op basis van signaal
        bg_color = "transparent"
        border = "1px solid #30363d"
        if w_data['signal'] == "Trend Green": 
            bg_color = "rgba(63, 185, 80, 0.1)"; border = "2px solid #3fb950"
        elif w_data['signal'] == "Breakout Blue": 
            bg_color = "rgba(37, 99, 235, 0.1)"; border = "2px solid #2563eb"

        # Maak een container voor de rij
        with st.container():
            st.markdown(f'<div style="background-color: {bg_color}; border: {border}; padding: 10px; border-radius: 8px; margin-bottom: 5px;">', unsafe_allow_html=True)
            r1, r2, r3, r4, r5, r6 = st.columns([1, 1, 1, 1, 2, 1])
            if r1.button(f"📊 {item}", key=f"sel_{item}"):
                st.session_state.current_ticker = item
                st.rerun()
            r2.write(f"${w_data['price']:.2f}")
            r3.write(f"{w_data['rsi']:.1f}")
            r4.write("✅" if w_data['macd_bull'] else "❌")
            r5.write(f"**{w_data['signal']}**")
            if r6.button("🗑️", key=f"del_{item}"):
                st.session_state.watchlist.remove(item)
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)





































