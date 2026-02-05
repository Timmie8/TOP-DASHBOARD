import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas_ta as ta
import pandas as pd

# 1. Pagina Configuratie
st.set_page_config(page_title="SST SMART TERMINAL", layout="wide")

# CSS om de Streamlit interface te minimaliseren voor een dashboard look
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .block-container { padding: 0px !important; background-color: #050608; }
    iframe { border: none !important; width: 100% !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Python Functie voor Data & Indicatoren
def get_indicator_data(ticker_symbol):
    try:
        # Haal data op (1 jaar historie nodig voor EMA200)
        df = yf.download(ticker_symbol, period="1y", interval="1d", progress=False, auto_adjust=True)
        
        if df.empty or len(df) < 200:
            return None

        # Fix voor yfinance MultiIndex kolommen
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # RSI 14
        df['RSI'] = ta.rsi(df['Close'], length=14)
        
        # Stochastic (14, 3, 3)
        stoch = ta.stoch(df['High'], df['Low'], df['Close'], k=14, d=3, smooth_k=3)
        df['STOCH_K'] = stoch.iloc[:, 0]
        df['STOCH_D'] = stoch.iloc[:, 1]
        
        # MACD (12, 26, 9)
        macd = ta.macd(df['Close'])
        df['MACD_L'] = macd.iloc[:, 0]
        df['MACD_S'] = macd.iloc[:, 2]
        
        # EMA's
        df['EMA20'] = ta.ema(df['Close'], length=20)
        df['EMA50'] = ta.ema(df['Close'], length=50)
        df['EMA200'] = ta.ema(df['Close'], length=200)
        
        # Bollinger Bands
        bb = ta.bbands(df['Close'], length=20)
        df['BBU'] = bb.iloc[:, 2]
        
        last = df.iloc[-1]
        prev = df.iloc[-2]
        
        return {
            "price": float(last['Close']),
            "change": float(((last['Close'] - prev['Close']) / prev['Close']) * 100),
            "rsi": float(last['RSI']),
            "stoch_k": float(last['STOCH_K']),
            "stoch_prev_k": float(prev['STOCH_K']),
            "stoch_d": float(last['STOCH_D']),
            "macd": float(last['MACD_L']),
            "macd_s": float(last['MACD_S']),
            "ema20": float(last['EMA20']),
            "ema50": float(last['EMA50']),
            "ema200": float(last['EMA200']),
            "bb_upper": float(last['BBU'])
        }
    except Exception as e:
        return None

# 3. Sidebar Input
st.sidebar.title("SST SETTINGS")
ticker = st.sidebar.text_input("Ticker (Yahoo format)", value="NVDA").upper()
st.sidebar.info("Gebruik BTC-USD voor crypto, NVDA voor aandelen.")

data = get_indicator_data(ticker)

# 4. Dashboard Weergave
if data:
    # Condities voor kleuren (Backend logica)
    rsi_green = 30 <= data['rsi'] <= 65
    
    # Stochastic logica: Groen als boven D en stijgend, Blauw als boven D maar niet stijgend, anders Rood
    if data['stoch_k'] > data['stoch_d'] and data['stoch_k'] > data['stoch_prev_k']:
        stoch_class = "status-green"
    elif data['stoch_k'] > data['stoch_d']:
        stoch_class = "status-blue"
    else:
        stoch_class = "status-red"

    macd_green = data['macd'] > data['macd_s']
    ema_green = data['price'] > data['ema20'] and data['price'] > data['ema50'] and data['price'] > data['ema200']
    bb_green = data['price'] > data['bb_upper']
    
    # Check voor Confluence (5/5 groen)
    # Let op: voor stoch_green tellen we alleen de 'echte' groene status
    green_count = sum([rsi_green, (stoch_class == "status-green"), macd_green, ema_green, bb_green])
    
    score = int(50 + (data['change'] * 12))
    score = max(min(score, 99), 5)

    terminal_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
        <style>
            body {{ background-color: #050608; color: white; font-family: 'Inter', sans-serif; margin: 0; padding: 20px; }}
            .card {{ background: #0d1117; border: 1px solid #30363d; padding: 20px; border-radius: 12px; text-align: center; }}
            .indicator-panel {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin-top: 20px; margin-bottom: 20px; }}
            .ind-card {{ background: #0d1117; border: 2px solid #30363d; padding: 15px; border-radius: 8px; text-align: center; font-size: 0.8rem; font-weight: bold; }}
            
            .status-green {{ border-color: #3fb950 !important; color: #3fb950; background: rgba(63, 185, 80, 0.1); }}
            .status-blue {{ border-color: #2563eb !important; color: #2563eb; background: rgba(37, 99, 235, 0.1); }}
            .status-red {{ border-color: #f85149 !important; color: #f85149; background: rgba(248, 81, 73, 0.1); }}
            
            #superSignal {{ 
                display: {"block" if green_count == 5 else "none"}; 
                background: linear-gradient(90deg, #d29922, #f1e05a); 
                color: black; padding: 15px; border-radius: 10px; text-align: center; 
                font-weight: 900; margin-bottom: 20px; font-size: 1.2rem;
            }}
            #tv-chart {{ height: 500px; border-radius: 15px; overflow: hidden; border: 1px solid #30363d; }}
        </style>
    </head>
    <body>
        <div id="superSignal">🚀 CONFLUENCE DETECTED: ALL INDICATORS BULLISH 🚀</div>
        
        <div class="card">
            <div style="color: #8b949e; font-size: 0.8rem; font-weight: bold;">AI MOMENTUM SCORE: {ticker}</div>
            <div style="font-size: 4rem; font-weight: 900; color: {'#3fb950' if score > 60 else '#f85149' if score < 40 else '#d29922'}">{score}</div>
            <div style="font-size: 1.2rem; font-weight: bold; color: #8b949e;">{"BULLISH" if score > 60 else "BEARISH" if score < 40 else "NEUTRAL"}</div>
        </div>

        <div class="indicator-panel">
            <div class="ind-card {"status-green" if rsi_green else ""}">RSI (14)<br>{data['rsi']:.1f}</div>
            <div class="ind-card {stoch_class}">STOCH (14,3,3)<br>{data['stoch_k']:.1f}</div>
            <div class="ind-card {"status-green" if macd_green else ""}">MACD<br>{'BULL' if macd_green else 'BEAR'}</div>
            <div class="ind-card {"status-green" if ema_green else ""}">EMA CLOUD<br>{'SUPPORT' if ema_green else 'RESISTANCE'}</div>
            <div class="ind-card {"status-green" if bb_green else ""}">BOLLINGER<br>{'BREAKOUT' if bb_green else 'INSIDE'}</div>
        </div>

        <div id="tv-chart"></div>

        <script src="https://s3.tradingview.com/tv.js"></script>
        <script>
            new TradingView.widget({{
                "autosize": true,
                "symbol": "{ticker}",
                "interval": "D",
                "timezone": "Etc/UTC",
                "theme": "dark",
                "style": "1",
                "locale": "nl",
                "container_id": "tv-chart",
                "hide_side_toolbar": false,
                "allow_symbol_change": true,
                "details": true
            }});
        </script>
    </body>
    </html>
    """
    components.html(terminal_html, height=1000)
else:
    st.error(f"Geen data gevonden voor {ticker}. Controleer of de ticker correct is (bijv. AAPL of BTC-USD).")





































