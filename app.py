import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas_ta as ta
import json

# 1. Pagina Configuratie
st.set_page_config(page_title="SST SMART TERMINAL (YFINANCE)", layout="wide")

# 2. Functie om data op te halen via Yahoo Finance (Python)
def get_indicator_data(ticker):
    try:
        df = yf.download(ticker, period="1y", interval="1d", progress=False)
        if df.empty: return None
        
        # Bereken Indicatoren met pandas_ta
        df['RSI'] = ta.rsi(df['Close'], length=14)
        stoch = ta.stoch(df['High'], df['Low'], df['Close'], k=14, d=3, smooth_k=3)
        df['STOCH_K'] = stoch['STOCHk_14_3_3']
        df['STOCH_D'] = stoch['STOCHd_14_3_3']
        macd = ta.macd(df['Close'])
        df['MACD'] = macd['MACD_12_26_9']
        df['MACD_S'] = macd['MACDs_12_26_9']
        df['EMA20'] = ta.ema(df['Close'], length=20)
        df['EMA50'] = ta.ema(df['Close'], length=50)
        df['EMA200'] = ta.ema(df['Close'], length=200)
        bb = ta.bbands(df['Close'], length=20)
        df['BBU'] = bb['BBU_20_2.0']
        
        last = df.iloc[-1]
        prev = df.iloc[-2]
        
        # Logica checks
        return {
            "price": float(last['Close']),
            "change": float(((last['Close'] - prev['Close']) / prev['Close']) * 100),
            "rsi": float(last['RSI']),
            "stoch_k": float(last['STOCH_K']),
            "stoch_prev_k": float(prev['STOCH_K']),
            "stoch_d": float(last['STOCH_D']),
            "macd": float(last['MACD']),
            "macd_s": float(last['MACD_S']),
            "ema20": float(last['EMA20']),
            "ema50": float(last['EMA50']),
            "ema200": float(last['EMA200']),
            "bb_upper": float(last['BBU'])
        }
    except:
        return None

# Sidebar voor input
ticker = st.sidebar.text_input("Voer Ticker in (bijv. NVDA, TSLA)", value="NVDA").upper()
data = get_indicator_data(ticker)

# 3. HTML & JavaScript Deel
if data:
    # Bereken de score in Python
    green_count = 0
    if 30 <= data['rsi'] <= 65: green_count += 1
    if data['stoch_k'] > data['stoch_d'] and data['stoch_k'] > data['stoch_prev_k']: green_count += 1
    if data['macd'] > data['macd_s']: green_count += 1
    if data['price'] > data['ema20'] and data['price'] > data['ema50'] and data['price'] > data['ema200']: green_count += 1
    if data['price'] > data['bb_upper']: green_count += 1
    
    score = int(50 + (data['change'] * 12))
    score = max(min(score, 99), 5)

    terminal_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
        <style>
            body {{ background-color: #050608; color: white; font-family: 'Inter', sans-serif; margin: 0; padding: 10px; }}
            .card {{ background: #0d1117; border: 1px solid #30363d; padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 20px; }}
            .indicator-panel {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin-bottom: 20px; }}
            .ind-card {{ background: #0d1117; border: 2px solid #30363d; padding: 10px; border-radius: 8px; text-align: center; font-size: 0.8rem; font-weight: bold; }}
            .status-green {{ border-color: #3fb950; color: #3fb950; background: rgba(63, 185, 80, 0.1); }}
            .status-blue {{ border-color: #2563eb; color: #2563eb; background: rgba(37, 99, 235, 0.1); }}
            .status-red {{ border-color: #f85149; color: #f85149; background: rgba(248, 81, 73, 0.1); }}
            #superSignal {{ display: {"block" if green_count == 5 else "none"}; background: linear-gradient(90deg, #d29922, #f1e05a); color: black; padding: 15px; border-radius: 10px; text-align: center; font-weight: 900; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div id="superSignal">🚀 CONFLUENCE DETECTED: ALL INDICATORS BULLISH 🚀</div>
        
        <div class="card">
            <div style="color: #8b949e; font-size: 0.8rem;">AI MOMENTUM SCORE voor {ticker}</div>
            <div style="font-size: 3.5rem; font-weight: 900; color: {'#3fb950' if score > 60 else '#f85149' if score < 40 else '#d29922'}">{score}</div>
        </div>

        <div class="indicator-panel">
            <div class="ind-card {"status-green" if 30 <= data['rsi'] <= 65 else ""}">RSI: {data['rsi']:.1f}</div>
            <div class="ind-card {"status-green" if data['stoch_k'] > data['stoch_d'] and data['stoch_k'] > data['stoch_prev_k'] else "status-blue" if data['stoch_k'] > data['stoch_d'] else "status-red"}">STOCH K: {data['stoch_k']:.1f}</div>
            <div class="ind-card {"status-green" if data['macd'] > data['macd_s'] else ""}">MACD: {'BULL' if data['macd'] > data['macd_s'] else 'BEAR'}</div>
            <div class="ind-card {"status-green" if data['price'] > data['ema20'] and data['price'] > data['ema50'] and data['price'] > data['ema200'] else ""}">EMA CLOUD</div>
            <div class="ind-card {"status-green" if data['price'] > data['bb_upper'] else ""}">BB BREAKOUT</div>
        </div>

        <div id="tv-chart" style="height: 600px; border-radius: 15px; overflow: hidden; border: 1px solid #30363d;"></div>

        <script src="https://s3.tradingview.com/tv.js"></script>
        <script>
            new TradingView.widget({{ "autosize": true, "symbol": "{ticker}", "interval": "D", "theme": "dark", "container_id": "tv-chart" }});
        </script>
    </body>
    </html>
    """
    components.html(terminal_html, height=900)
else:
    st.error("Data kon niet worden opgehaald. Controleer de ticker.")




































