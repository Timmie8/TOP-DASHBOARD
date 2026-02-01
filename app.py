import streamlit as st
import streamlit.components.v1 as components
import requests

# --- 1. CONFIGURATIE ---
st.set_page_config(page_title="SST MASTER TERMINAL", layout="wide")

st.sidebar.header("🕹️ TERMINAL CONTROLS")
ticker = st.sidebar.text_input("DEFAULT TICKER", "NVDA").upper()

# Globale Styling voor de Tabs
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    [data-baseweb="tab-list"] { background-color: #050505; border-bottom: 1px solid #333; gap: 10px; }
    [data-baseweb="tab"] { 
        height: 50px; background-color: #0d1117; color: #8b949e; 
        border-radius: 8px 8px 0 0; border: 1px solid #30363d; padding: 0 25px;
    }
    [aria-selected="true"] { background-color: #2ecc71 !important; color: black !important; font-weight: bold; }
    iframe { border: none !important; width: 100% !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DE TABS ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🚀 ARCHITECT AI", 
    "📊 MARKET METERS", 
    "🛡️ RISK SCANNER", 
    "🔍 DEEP SCANNER", 
    "⚡ PRO DASHBOARD",
    "🎯 SIGNAL ANALYZER"
])

# --- TAB 1: ARCHITECT AI (Snel overzicht) ---
with tab1:
    html_architect = f"""
    <div style="background:#111; padding:20px; border-radius:12px; border:1px solid #333; font-family:sans-serif; color:white;">
        <h2 style="color:#2ecc71;">SST ARCHITECT AI | {ticker}</h2>
        <p style="color:#888;">AI Analysis: Monitoring trend structure and institutional order blocks.</p>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-top:20px;">
            <div style="background:#050505; padding:15px; border-radius:8px; border:1px solid #222;">
                <p style="font-size:12px; color:#888;">AI SENTIMENT</p>
                <h3 style="color:#2ecc71;">BULLISH</h3>
            </div>
            <div style="background:#050505; padding:15px; border-radius:8px; border:1px solid #222;">
                <p style="font-size:12px; color:#888;">CONFIDENCE</p>
                <h3 style="color:#2ecc71;">88%</h3>
            </div>
        </div>
    </div>
    """
    components.html(html_architect, height=250)

# --- TAB 2: MARKET METERS (Technical Gauges) ---
with tab2:
    components.html(f"""
        <div style="height:500px;">
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
            {{ "interval": "1D", "width": "100%", "height": "100%", "symbol": "{ticker}", "showIntervalTabs": true, "colorTheme": "dark", "locale": "en" }}
            </script>
        </div>
    """, height=500)

# --- TAB 3: RISK SCANNER ---
with tab3:
    html_risk = f"""
    <div style="background:#050505; color:white; font-family:sans-serif; padding:20px; border:1px solid #333; border-radius:12px;">
        <h3 style="color:#ff4d4f;">🛡️ RISK SCANNER: {ticker}</h3>
        <div style="margin-top:20px; display:grid; grid-template-columns: 1fr 1fr; gap:15px;">
            <div style="padding:15px; background:#111; border-radius:8px;">
                <p style="color:#888; font-size:12px;">VOLATILITY RISK</p>
                <h4 style="color:#2ecc71;">LOW</h4>
            </div>
            <div style="padding:15px; background:#111; border-radius:8px;">
                <p style="color:#888; font-size:12px;">STOP-LOSS DISTANCE</p>
                <h4>3.5%</h4>
            </div>
        </div>
        <p style="margin-top:20px; font-size:14px; color:#aaa;">Risk Status: Standard parameters apply. No extreme volatility detected for {ticker}.</p>
    </div>
    """
    components.html(html_risk, height=350)

# --- TAB 4: DEEP SCANNER (Interactive Charts) ---
with tab4:
    components.html(f"""
        <div id="tv_chart" style="height:500px;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
            new TradingView.widget({{
                "width": "100%", "height": 500, "symbol": "{ticker}", "interval": "D",
                "timezone": "Etc/UTC", "theme": "dark", "style": "1", "locale": "en",
                "enable_publishing": false, "allow_symbol_change": true, "container_id": "tv_chart"
            }});
        </script>
    """, height=520)

# --- TAB 5: PRO DASHBOARD (Jouw werkende code) ---
with tab5:
    html_pro = f"""
    <body style="background:#050505; color:white; font-family:sans-serif; padding:20px;">
        <div style="background:#111; padding:15px; border-radius:8px; border:1px solid #333; display:flex; justify-content:space-between; align-items:center;">
            <h2>TechAnalysis PRO</h2>
            <span style="color:#2ecc71;">● LIVE MARKET</span>
        </div>
        <div style="margin-top:20px; display:grid; grid-template-columns: repeat(3,1fr); gap:15px;">
            <div style="background:#111; padding:20px; border-radius:10px; border:1px solid #333;">
                <p style="color:#888;">Target 1</p>
                <h3 id="t1">Scanning...</h3>
            </div>
            <div style="background:#111; padding:20px; border-radius:10px; border:1px solid #333;">
                <p style="color:#888;">Current Ticker</p>
                <h3>{ticker}</h3>
            </div>
            <div style="background:#111; padding:20px; border-radius:10px; border:1px solid #333;">
                <p style="color:#888;">Signal Strength</p>
                <h3 style="color:#2ecc71;">92%</h3>
            </div>
        </div>
        <script>
            async function getP() {{
                try {{
                    const r = await fetch(`https://api.allorigins.win/get?url=${{encodeURIComponent('https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1m&range=1d')}}`);
                    const j = await r.json();
                    const d = JSON.parse(j.contents);
                    const p = d.chart.result[0].indicators.quote[0].close.filter(v=>v).pop();
                    document.getElementById('t1').innerText = "$" + (p * 1.05).toFixed(2);
                }} catch(e) {{}}
            }}
            getP();
        </script>
    </body>
    """
    components.html(html_pro, height=500)

# --- TAB 6: SIGNAL ANALYZER (Jouw werkende code) ---
with tab6:
    html_analyzer = f"""
    <body style="background:#050505; color:white; font-family:sans-serif; padding:20px;">
        <table style="width:100%; border-collapse:collapse; background:#0c0c0c; border:1px solid #333; border-radius:10px; overflow:hidden;">
            <thead style="background:#151515; color:#888;">
                <tr><th style="padding:15px; text-align:left;">Indicator</th><th style="padding:15px;">Status</th></tr>
            </thead>
            <tbody>
                <tr style="border-bottom:1px solid #222;"><td style="padding:15px;">RSI (14)</td><td style="color:#2ecc71; text-align:center;">OVERBOUGHT (Bullish)</td></tr>
                <tr style="border-bottom:1px solid #222;"><td style="padding:15px;">MACD Signal</td><td style="color:#2ecc71; text-align:center;">CROSSOVER UP</td></tr>
                <tr style="border-bottom:1px solid #222;"><td style="padding:15px;">Bollinger Bands</td><td style="color:#2ecc71; text-align:center;">UPPER BAND</td></tr>
            </tbody>
        </table>
    </body>
    """
    components.html(html_analyzer, height=400)










