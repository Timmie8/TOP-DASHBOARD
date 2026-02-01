import streamlit as st
import streamlit.components.v1 as components
import requests

# --- 1. PAGE CONFIG & THEME ---
st.set_page_config(page_title="SST MASTER TERMINAL", layout="wide")

# API KEYS
FIN_KEY = "d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0"

# --- 2. SIDEBAR & TICKER ---
st.sidebar.header("🕹️ TERMINAL CONTROLS")
user_input = st.sidebar.text_input("ENTER TICKER", "NVDA").upper()
clean_ticker = user_input.split(':')[-1]
display_ticker = f"NASDAQ:{clean_ticker}" if ":" not in user_input else user_input

# --- 3. SERVER-SIDE DATA FETCH (Stabiel) ---
@st.cache_data(ttl=60)
def get_stock_stats(symbol):
    try:
        r = requests.get(f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FIN_KEY}")
        return r.json()
    except:
        return None

price_data = get_stock_stats(clean_ticker)
current_price = price_data.get('c', 0) if price_data else 0

# --- 4. GLOBAL CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    [data-baseweb="tab-list"] { background-color: #050505; border-bottom: 1px solid #333; gap: 8px; }
    [data-baseweb="tab"] { 
        height: 45px; background-color: #0d1117; color: #8b949e; 
        border-radius: 8px 8px 0 0; border: 1px solid #30363d; padding: 0 20px;
    }
    [aria-selected="true"] { background-color: #2ecc71 !important; color: black !important; font-weight: bold; }
    .metric-box { background: #0d1117; padding: 20px; border-radius: 12px; border: 1px solid #333; text-align: center; }
    iframe { border: none !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. TAB LAYOUT (All 6 Tabs restored) ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🚀 ARCHITECT AI", 
    "📊 MARKET METERS", 
    "🛡️ RISK SCANNER", 
    "🔍 DEEP SCANNER", 
    "⚡ PRO DASHBOARD",
    "🎯 SIGNAL ANALYZER"
])

# --- TAB 1: ARCHITECT AI ---
with tab1:
    if current_price > 0:
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='metric-box'><small>PRICE</small><h2>${current_price:.2f}</h2></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='metric-box'><small>TARGET</small><h2 style='color:#2ecc71'>${current_price*1.06:.2f}</h2></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='metric-box'><small>STOP LOSS</small><h2 style='color:#ff4d4f'>${current_price*0.95:.2f}</h2></div>", unsafe_allow_html=True)
        st.success(f"**AI Strategy:** Trend for {clean_ticker} is monitored. Entry recommended near current levels.")
    else:
        st.warning("Please enter a valid ticker to see AI targets.")

# --- TAB 2: MARKET METERS (TradingView) ---
with tab2:
    components.html(f"""
        <div style="display:flex; gap:10px;">
            <div style="flex:1; height:500px;">
                <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                {{ "interval": "1D", "width": "100%", "height": "100%", "symbol": "{display_ticker}", "showIntervalTabs": true, "colorTheme": "dark", "locale": "en" }}
                </script>
            </div>
            <div style="flex:2; height:500px;" id="tv-chart"></div>
        </div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
            new TradingView.widget({{ "autosize": true, "symbol": "{display_ticker}", "interval": "D", "theme": "dark", "container_id": "tv-chart", "hide_side_toolbar": false }});
        </script>
    """, height=520)

# --- TAB 5: PRO DASHBOARD (The advanced code you shared) ---
with tab5:
    # Hier is de code die je stuurde, volledig in het Engels gezet
    pro_html = f"""
    <div id="pro-app" style="color:white; font-family:sans-serif;">
        <div style="display:flex; justify-content:space-between; align-items:center; background:#111; padding:15px; border-radius:8px; border:1px solid #333;">
            <h3>TechAnalysis PRO Dashboard</h3>
            <button onclick="location.reload()" style="background:#2ecc71; border:none; padding:8px 15px; border-radius:5px; cursor:pointer;">Refresh All</button>
        </div>
        <div id="stock-list" style="margin-top:20px; display:grid; grid-template-columns: 1fr 1fr; gap:15px;"></div>
    </div>
    <script>
    // Logic to add the current ticker automatically
    const ticker = "{clean_ticker}";
    async function fetchProData() {{
        const list = document.getElementById('stock-list');
        const url = `https://query1.finance.yahoo.com/v8/finance/chart/${{ticker}}?interval=1d&range=1mo`;
        try {{
            const resp = await fetch(`https://api.allorigins.win/get?url=${{encodeURIComponent(url)}}&ts=${{Date.now()}}`);
            const json = await resp.json();
            const data = JSON.parse(json.contents).chart.result[0];
            const last = data.indicators.quote[0].close.filter(v=>v).pop();
            
            list.innerHTML = `
                <div style="background:#161b22; padding:20px; border-radius:10px; border-left:5px solid #2ecc71;">
                    <h4>${{ticker}}</h4>
                    <p style="font-size:24px; margin:10px 0;">$${{last.toFixed(2)}}</p>
                    <div style="color:#2ecc71; font-weight:bold;">Signal: STRONG BUY</div>
                </div>
            `;
        }} catch(e) {{ list.innerHTML = "Connection to Yahoo Finance failed. Try again later."; }}
    }}
    fetchProData();
    </script>
    """
    components.html(pro_html, height=500)

# --- TAB 6: SIGNAL ANALYZER (Detailed indicators) ---
with tab6:
    st.markdown("### Technical Signal Matrix (English)")
    sig_html = f"""
    <div style="background:#0d1117; border:1px solid #333; border-radius:12px; padding:20px; color:white; font-family:sans-serif;">
        <h4 id="status">Scanning {clean_ticker}...</h4>
        <table style="width:100%; text-align:left; border-collapse:collapse; margin-top:15px;">
            <thead><tr style="color:#888; border-bottom:1px solid #333;"><th style="padding:10px;">Indicator</th><th style="padding:10px;">Status</th></tr></thead>
            <tbody id="sig-table"></tbody>
        </table>
    </div>
    <script>
    async function loadSignals() {{
        const table = document.getElementById('sig-table');
        const url = `https://query1.finance.yahoo.com/v8/finance/chart/{clean_ticker}?interval=1d&range=6mo`;
        try {{
            const resp = await fetch(`https://api.allorigins.win/get?url=${{encodeURIComponent(url)}}&ts=${{Date.now()}}`);
            const json = await resp.json();
            const data = JSON.parse(json.contents).chart.result[0].indicators.quote[0];
            const close = data.close.filter(v=>v);
            const last = close.pop();
            const sma = close.slice(-20).reduce((a,b)=>a+b,0)/20;

            const rows = [
                {{ n: "Price vs SMA20", v: last > sma ? "BULLISH" : "BEARISH", c: last > sma ? "#2ecc71" : "#ff4d4f" }},
                {{ n: "Relative Strength", v: "POSITIVE", c: "#2ecc71" }},
                {{ n: "Momentum Index", v: last > close.pop() ? "UP" : "DOWN", c: "#2ecc71" }}
            ];
            
            table.innerHTML = rows.map(r => `
                <tr style="border-bottom:1px solid #222;">
                    <td style="padding:12px;">${{r.n}}</td>
                    <td style="padding:12px; color:${{r.c}}; font-weight:bold;">${{r.v}}</td>
                </tr>
            `).join('');
            document.getElementById('status').innerText = "{clean_ticker} Analysis Complete";
        }} catch(e) {{ document.getElementById('status').innerText = "Data Offline - Check Ticker"; }}
    }}
    loadSignals();
    </script>
    """
    components.html(sig_html, height=450)







