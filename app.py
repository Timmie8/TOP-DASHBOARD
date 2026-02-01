import streamlit as st
import streamlit.components.v1 as components
import requests
import json

# --- 1. CONFIG ---
st.set_page_config(page_title="SST MASTER TERMINAL", layout="wide")

st.sidebar.header("🕹️ TERMINAL CONTROLS")
ticker = st.sidebar.text_input("SET GLOBAL TICKER", "NVDA").upper()
tv_ticker = f"NASDAQ:{ticker}" if ":" not in ticker else ticker

# --- 2. RAW DATA FETCH (The Engine) ---
@st.cache_data(ttl=30)
def get_raw_market_data(symbol):
    try:
        # We halen een volledige dataset op zodat jouw indicatoren (SMA/RSI) kunnen rekenen
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1y"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=5)
        return r.text # We geven de RUWE tekst door aan jouw JS
    except:
        return None

raw_json_data = get_raw_market_data(ticker)

# --- 3. STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    [data-baseweb="tab-list"] { background-color: #050505; border-bottom: 1px solid #333; gap: 10px; }
    [data-baseweb="tab"] { height: 50px; background-color: #0d1117; color: #8b949e; border-radius: 8px 8px 0 0; }
    [aria-selected="true"] { background-color: #2ecc71 !important; color: black !important; font-weight: bold; }
    iframe { border: none !important; width: 100% !important; }
    </style>
    """, unsafe_allow_html=True)

tabs = st.tabs(["🚀 ARCHITECT AI", "📊 MARKET METERS", "🛡️ RISK SCANNER", "🔍 DEEP SCANNER", "⚡ PRO DASHBOARD", "🎯 SIGNAL ANALYZER"])

# --- TABS 1-4 (Standardized Widgets) ---
with tabs[1]:
    components.html(f'<script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>{{ "interval": "1D", "width": "100%", "height": 450, "symbol": "{tv_ticker}", "showIntervalTabs": true, "colorTheme": "dark", "locale": "en" }}</script>', height=470)

with tabs[3]:
    components.html(f'<div id="tv_chart"></div><script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script><script type="text/javascript">new TradingView.widget({{ "width": "100%", "height": 500, "symbol": "{tv_ticker}", "interval": "D", "theme": "dark", "style": "1", "locale": "en", "container_id": "tv_chart" }});</script>', height=520)

# --- TAB 5: PRO DASHBOARD (JOUW ORIGINELE LOGICA) ---
with tabs[4]:
    if raw_json_data:
        # Hier injecteren we de ruwe data direct in jouw originele script-structuur
        code_pro = f"""
        <div id="pro-root" style="background:#050505; color:white; font-family:sans-serif;">
            <div id="display-area"></div>
        </div>
        <script>
            const rawData = {raw_json_data};
            const res = rawData.chart.result[0];
            const quotes = res.indicators.quote[0];
            const close = quotes.close.filter(v => v != null);
            
            // JOUW ORIGINELE BEREKENINGEN
            const last = close[close.length - 1];
            const target = last * 1.05;
            const stop = last * 0.97;
            
            document.getElementById('display-area').innerHTML = `
                <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:15px; margin-top:20px;">
                    <div style="background:#111; padding:20px; border-radius:12px; border:1px solid #333; text-align:center;">
                        <p style="color:#888;">PRICE</p><h2>$${{last.toFixed(2)}}</h2>
                    </div>
                    <div style="background:#111; padding:20px; border-radius:12px; border:1px solid #333; text-align:center;">
                        <p style="color:#2ecc71;">TARGET</p><h2>$${{target.toFixed(2)}}</h2>
                    </div>
                    <div style="background:#111; padding:20px; border-radius:12px; border:1px solid #333; text-align:center;">
                        <p style="color:#ff4d4f;">STOP</p><h2>$${{stop.toFixed(2)}}</h2>
                    </div>
                </div>
            `;
        </script>
        """
        components.html(code_pro, height=500)

# --- TAB 6: SIGNAL ANALYZER (JOUW ORIGINELE MATRIX) ---
with tabs[5]:
    if raw_json_data:
        code_sig = f"""
        <style>
            .matrix {{ width: 100%; border-collapse: collapse; background: #0c0c0c; border: 1px solid #333; color: white; }}
            .matrix td, .matrix th {{ padding: 15px; border-bottom: 1px solid #222; }}
            .bullish {{ color: #2ecc71; font-weight: bold; }}
            .bearish {{ color: #ff4d4f; font-weight: bold; }}
        </style>
        <table class="matrix">
            <thead><tr><th>Indicator</th><th>Signal</th></tr></thead>
            <tbody id="matrix-body"></tbody>
        </table>
        <script>
            const rawData = {raw_json_data};
            const res = rawData.chart.result[0];
            const quotes = res.indicators.quote[0];
            const close = quotes.close.filter(v => v != null);
            const high = quotes.high.filter(v => v != null);
            const low = quotes.low.filter(v => v != null);

            const last = close[close.length - 1];
            
            // BEREKENINGEN UIT JOUW CODE
            const sma20 = close.slice(-20).reduce((a,b)=>a+b,0)/20;
            const hh = Math.max(...high.slice(-14));
            const ll = Math.min(...low.slice(-14));
            const willR = ((hh - last) / (hh - ll)) * -100;

            const results = [
                {{ n: "Trend (SMA20)", v: last > sma20 }},
                {{ n: "Momentum (Williams %R)", v: willR > -50 }},
                {{ n: "Institutional Flow", v: last > close[close.length-5] }}
            ];

            document.getElementById('matrix-body').innerHTML = results.map(r => `
                <tr><td>${{r.n}}</td><td class="${{r.v ? 'bullish' : 'bearish'}}">${{r.v ? 'BULLISH' : 'BEARISH'}}</td></tr>
            `).join('');
        </script>
        """
        components.html(code_sig, height=500)















