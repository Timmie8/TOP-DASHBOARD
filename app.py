import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas_ta as ta
import pandas as pd

# 1. Pagina Configuratie
st.set_page_config(page_title="SST SMART TERMINAL", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .block-container { padding: 0px !important; background-color: #050608; }
    iframe { border: none !important; width: 100% !important; }
    /* Styling voor de watchlist knoppen */
    .stButton button { border-radius: 8px; margin-bottom: 2px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Watchlist Initialisatie
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = ["NVDA", "AAPL", "BTC-USD", "TSLA"]
if 'current_ticker' not in st.session_state:
    st.session_state.current_ticker = "NVDA"

# 3. Indicator Functie voor de Watchlist Check
def check_signals(ticker_symbol):
    try:
        df = yf.download(ticker_symbol, period="1y", interval="1d", progress=False, auto_adjust=True)
        if df.empty or len(df) < 200: return "none"
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)

        # Nodige indicatoren
        rsi = ta.rsi(df['Close'], length=14).iloc[-1]
        macd = ta.macd(df['Close'])
        m_line, s_line = macd.iloc[-1, 0], macd.iloc[-1, 2]
        ema20 = ta.ema(df['Close'], 20).iloc[-1]
        ema50 = ta.ema(df['Close'], 50).iloc[-1]
        ema200 = ta.ema(df['Close'], 200).iloc[-1]
        bb = ta.bbands(df['Close'], length=20)
        upper_bb = bb.iloc[-1, 2]
        price = df['Close'].iloc[-1]
        
        # Volume check (huidig vs gemiddelde van 20 dagen)
        avg_volume = df['Volume'].rolling(20).mean().iloc[-1]
        curr_volume = df['Volume'].iloc[-1]

        # Conditie 1: GROEN (Trend)
        if (price > ema20 and price > ema50 and price > ema200 and 
            m_line > s_line and 40 <= rsi <= 60):
            return "green"
        
        # Conditie 2: BLAUW (Breakout)
        if (price > upper_bb and m_line > s_line and 
            price > ema50 and curr_volume > avg_volume):
            return "blue"
            
        return "none"
    except: return "none"

# --- SIDEBAR ---
st.sidebar.title("SST WATCHLIST")
new_t = st.sidebar.text_input("Nieuwe Ticker", placeholder="Bijv. MSFT").upper()
if st.sidebar.button("➕ Toevoegen"):
    if new_t and new_t not in st.session_state.watchlist:
        st.session_state.watchlist.append(new_t)
        st.rerun()

st.sidebar.write("---")

# Watchlist met visuele notificatie
for item in st.session_state.watchlist:
    signal = check_signals(item)
    
    # Bepaal de stijl op basis van het signaal
    border_style = "none"
    if signal == "green": border_style = "2px solid #3fb950"
    elif signal == "blue": border_style = "2px solid #2563eb"
    
    c1, c2 = st.sidebar.columns([4, 1])
    
    # Custom CSS Injectie voor de specifieke knop rand
    st.markdown(f"""
        <style>
        div[data-testid="stHorizontalBlock"] button[key="select_{item}"] {{
            border: {border_style} !important;
        }}
        </style>
    """, unsafe_allow_html=True)
    
    if c1.button(f"📊 {item}", key=f"select_{item}", use_container_width=True):
        st.session_state.current_ticker = item
    if c2.button("🗑️", key=f"remove_{item}"):
        st.session_state.watchlist.remove(item)
        st.rerun()

# --- HOOFD SCHERM ---
active_ticker = st.session_state.current_ticker
# Hier hergebruiken we de eerdere get_indicator_data() functie en terminal_html blok...
# (Zie vorige volledige code voor de data-berekening en TV widget integratie)




































