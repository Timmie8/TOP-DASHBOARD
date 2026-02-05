import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas_ta as ta
import pandas as pd

# 1. Pagina Configuratie
st.set_page_config(page_title="SST PRO TERMINAL", layout="wide")

# Uitgebreide CSS voor kleuren en layout
st.markdown("""
    <style>
    .block-container { padding: 15px !important; background-color: #050608; }
    .stMetric { background-color: #0d1117; border: 1px solid #30363d; padding: 15px; border-radius: 12px; }
    /* Kleur-logica voor de tekst in metrics */
    [data-testid="stMetricValue"] { font-size: 1.8rem !important; font-weight: 800; }
    
    /* Tabel styling */
    .watchlist-row { 
        display: flex; align-items: center; padding: 12px; border-radius: 10px; 
        margin-bottom: 8px; border: 1px solid #30363d; background-color: #0d1117;
    }
    .status-badge {
        padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: bold; text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. State Management
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = ["NVDA", "AAPL", "BTC-USD", "ETH-USD", "TSLA"]
if 'current_ticker' not in st.session_state:
    st.session_state.current_ticker = "NVDA"

# 3. Analyse Functie
def fetch_full_analysis(ticker_symbol):
    try:
        df = yf.download(ticker_symbol, period="1y", interval="1d", progress=False, auto_adjust=True)
        if df.empty or len(df) < 200: return None
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)

        # Berekeningen
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

        # Notificatie condities
        is_trend_green = (price > e20 and price > e50 and price > e200 and ml > sl and 40 <= rsi <= 60)
        is_breakout_blue = (price > upper_bb and ml > sl and price > e50 and vol_curr > vol_avg)

        signal = "NONE"
        if is_trend_green: signal = "TREND GREEN"
        elif is_breakout_blue: signal = "BREAKOUT BLUE"

        return {
            "symbol": ticker_symbol, "price": price, "change": ((price - prev_price)/prev_price)*100,
            "rsi": rsi, "macd_bull": ml > sl, "ema_ok": price > e20 and price > e50 and price > e200,
            "bb_break": price > upper_bb, "signal": signal
        }
    except: return None

# --- UI: TOP BAR ---
st.title("🚀 SST PRO SMART TERMINAL")
c_search, c_add = st.columns([4, 1])
quick_ticker = c_search.text_input("Voeg Ticker toe of zoek direct", placeholder="Bijv. MSFT, TSLA...").upper()

if c_add.button("➕ Toevoegen aan Lijst", use_container_width=True):
    if quick_ticker and quick_ticker not in st.session_state.watchlist:
        st.session_state.watchlist.append(quick_ticker)
        st.session_state.current_ticker = quick_ticker
        st.rerun()
elif quick_ticker:
    st.session_state.current_ticker = quick_ticker

# --- UI: MAIN DASHBOARD ---
active_ticker = st.session_state.current_ticker
data = fetch_full_analysis(active_ticker)

if data:
    # Gekleurde Indicatoren boven de chart
    m1, m2, m3, m4, m5 = st.columns(5)
    
    # Prijs met kleur
    m1.metric("Prijs", f"${data['price']:.2f}", f"{data['change']:.2f}%")
    
    # RSI Kleur (Groen tussen 40-60)
    rsi_color = "normal" if 40 <= data['rsi'] <= 60 else "inverse"
    m2.metric("RSI (14)", f"{data['rsi']:.1f}", delta="OPTimaal" if 40 <= data['rsi'] <= 60 else None)
    
    # MACD Kleur
    m3.metric("MACD", "BULLISH" if data['macd_bull'] else "BEARISH", 
              delta="KOOP" if data['macd_bull'] else "VERKOOP", 
              delta_color="normal" if data['macd_bull'] else "inverse")
    
    # EMA Cloud Kleur
    m4.metric("EMA Cloud", "BOVEN" if data['ema_ok'] else "ONDER", 
              delta="TREND OK" if data['ema_ok'] else "ZWAK",
              delta_color="normal" if data['ema_ok'] else "inverse")
    
    # Signaal Badge
    sig_label = data['signal']
    m5.metric("Signaal", sig_label, 
              delta="ACTIVE" if sig_label != "NONE" else None,
              delta_color="off" if sig_label == "NONE" else "normal")

    # TradingView Chart
    tv_html = f"""
    <div id="tv-chart" style="height: 520px; border: 1px solid #30363d; border-radius: 12px; margin-top: 10px;"></div>
    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>new TradingView.widget({{"autosize": true, "symbol": "{active_ticker}", "interval": "D", "theme": "dark", "container_id": "tv-chart"}});</script>
    """
    components.html(tv_html, height=540)

# --- UI: WATCHLIST ONDER CHART ---
st.write("---")
st.subheader("📋 Live Scanner & Watchlist")

# Tabel Header
h1, h2, h3, h4, h5, h6 = st.columns([1.5, 1, 1, 1, 2, 1])
h1.caption("AANDEEL")
h2.caption("PRIJS")
h3.caption("RSI")
h4.caption("MACD")
h5.caption("STRATEGIE STATUS")
h6.caption("ACTIE")

for item in st.session_state.watchlist:
    w_data = fetch_full_analysis(item)
    if w_data:
        # Rij Styling op basis van signaal
        border_color = "#30363d"
        glow = "transparent"
        if w_data['signal'] == "TREND GREEN": 
            border_color = "#3fb950"; glow = "rgba(63, 185, 80, 0.05)"
        elif w_data['signal'] == "BREAKOUT BLUE": 
            border_color = "#2563eb"; glow = "rgba(37, 99, 235, 0.05)"

        st.markdown(f"""
            <div style="display: flex; align-items: center; padding: 10px; border: 2px solid {border_color}; 
            background-color: {glow}; border-radius: 10px; margin-bottom: 8px;">
        """, unsafe_allow_html=True)
        
        r1, r2, r3, r4, r5, r6 = st.columns([1.5, 1, 1, 1, 2, 1])
        
        if r1.button(f"📊 {item}", key=f"v_{item}", use_container_width=True):
            st.session_state.current_ticker = item
            st.rerun()
            
        r2.write(f"**${w_data['price']:.2f}**")
        r3.write(f"{w_data['rsi']:.1f}")
        r4.write("🟢" if w_data['macd_bull'] else "🔴")
        
        # Status tekst met kleur
        status_txt = w_data['signal']
        if status_txt == "TREND GREEN":
            r5.markdown("<span style='color: #3fb950; font-weight: bold;'>✅ TREND CONFLUENCE</span>", unsafe_allow_html=True)
        elif status_txt == "BREAKOUT BLUE":
            r5.markdown("<span style='color: #2563eb; font-weight: bold;'>🚀 MOMENTUM BREAKOUT</span>", unsafe_allow_html=True)
        else:
            r5.write("Wachten op signaal...")

        if r6.button("🗑️", key=f"d_{item}"):
            st.session_state.watchlist.remove(item)
            st.rerun()
            
        st.markdown("</div>", unsafe_allow_html=True)





































