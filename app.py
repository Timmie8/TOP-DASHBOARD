import streamlit as st
import streamlit.components.v1 as components
import requests
import json

# --- 1. CONFIG ---
st.set_page_config(page_title="SST MASTER TERMINAL", layout="wide")

st.sidebar.header("🕹️ TERMINAL CONTROLS")
ticker = st.sidebar.text_input("SET GLOBAL TICKER", "NVDA").upper()

# --- 2. DATA ENGINE (Python side - No blocking) ---
def fetch_raw_data(symbol):
    try:
        # We halen 1 jaar aan data op voor alle berekeningen (SMA, RSI, etc)
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1y"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers)
        return r.text # We sturen de ruwe tekst door naar JS
    except:
        return None

raw_json = fetch_raw_data(ticker)

# --- 3. TABS ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🚀 ARCHITECT AI", "📊 MARKET METERS", "🛡️ RISK SCANNER", 
    "🔍 DEEP SCANNER", "⚡ PRO DASHBOARD", "🎯 SIGNAL ANALYZER"
])

# --- TAB 5: PRO DASHBOARD (Your Original Code Logic) ---
with tab5:
    if raw_json:
        code_tab_5 = f"""
        <div id="sst-pro-root" style="background:#050505; color:white; font-family:sans-serif; padding:20px; border-radius:15px; border:1px solid #333;">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #222; padding-bottom:15px; margin-bottom:20px;">
                <h2 style="margin:0; color:#2ecc71;">SST PRO DASHBOARD</h2>
                <span style="background:#111; padding:5px 12px; border-radius:20px; font-size:12px; border:1px solid #2ecc71;">LIVE: {ticker}</span>
            </div>
            
            <div id="pro-grid" style="display:grid; grid-template-columns: repeat(3, 1fr); gap:20px;">
                </div>
        </div>

        <script>
            (function() {{
                const data = {raw_json};
                const res = data.chart.result[0];
                const close = res.indicators.quote[0].close.filter(v => v != null);
                const lastPrice = close[close.length - 1];
                const prevPrice = close[close.length - 2];
                const change = ((lastPrice - prevPrice) / prevPrice * 100).toFixed(2);

                const grid = document.getElementById('pro-grid');
                grid.innerHTML = `
                    <div style="background:#111; padding:20px; border-radius:10px; border:1px solid #222; text-align:center;">
                        <p style="color:#888; font-size:12px; margin:0;">CURRENT PRICE</p>
                        <h2 style="margin:10px 0;">$${{lastPrice.toFixed(2)}}</h2>
                        <span style="color:${{change >= 0 ? '#2ecc71' : '#ff4d4f'}}">${{change}}%</span>
                    </div>
                    <div style="background:#111; padding:20px; border-radius:10px; border:1px solid #222; text-align:center;">
                        <p style="color:#888; font-size:12px; margin:0;">PROFIT TARGET (5%)</p>
                        <h2 style="margin:10px 0; color:#2ecc71;">$${{(lastPrice * 1.05).toFixed(2)}}</h2>
                    </div>
                    <div style="background:#111; padding:20px; border-radius:10px; border:1px solid #222; text-align:center;">
                        <p style="color:#888; font-size:12px; margin:0;">STOP LOSS (3%)</p>
                        <h2 style="margin:10px 0; color:#ff4d4f;">$${{(lastPrice * 0.97).toFixed(2)}}</h2>
                    </div>
                `;
            }})();
        </script>
        """
        components.html(code_tab_5, height=400)
    else:
        st.error("Data could not be loaded. Please check the ticker symbol.")

# --- TAB 6: SIGNAL ANALYZER (Your Original Logic) ---
with tab6:
    if raw_json:
        code_tab_6 = f"""
        <style>
            .sig-table {{ width: 100%; border-collapse: collapse; font-family: sans-serif; color: white; }}
            .sig-table th {{ text-align: left; color: #888; padding: 12px; border-bottom: 2px solid #333; }}
            .sig-table td {{ padding: 12px; border-bottom: 1px solid #222; }}
            .status-pill {{ padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 12px; }}
            .bullish {{ background: #123f2a; color: #1dd75f; }}
            .bearish {{ background: #4a1212; color: #ff4d4f; }}
        </style>
        <table class="sig-table">
            <thead>
                <tr><th>INDICATOR</th><th>VALUE</th><th>SIGNAL</th></tr>
            </thead>
            <tbody id="sig-tbody"></tbody>
        </table>

        <script>
            (function() {{
                const data = {raw_json};
                const res = data.chart.result[0];
                const close = res.indicators.quote[0].close.filter(v => v != null);
                const last = close[close.length - 1];
                
                // Example Math Logic from your codes
                const sma20 = close.slice(-20).reduce((a,b) => a+b, 0) / 20;
                const isBullish = last > sma20;

                const tbody = document.getElementById('sig-tbody');
                tbody.innerHTML = `
                    <tr>
                        <td>Moving Average (20 Day)</td>
                        <td>$${{sma20.toFixed(2)}}</td>
                        <td><span class="status-pill ${{isBullish ? 'bullish' : 'bearish'}}">${{isBullish ? 'BULLISH' : 'BEARISH'}}</span></td>
                    </tr>
                    <tr>
                        <td>Price Momentum</td>
                        <td>${{last > close[close.length-10] ? 'Positive' : 'Negative'}}</td>
                        <td><span class="status-pill ${{last > close[close.length-10] ? 'bullish' : 'bearish'}}">${{last > close[close.length-10] ? 'BUY' : 'WAIT'}}</span></td>
                    </tr>
                `;
            }})();
        </script>
        """
        components.html(code_tab_6, height=400)














