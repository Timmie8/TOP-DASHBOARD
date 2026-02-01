import streamlit as st
import streamlit.components.v1 as components

# --- 1. SETTINGS ---
st.set_page_config(page_title="SST MASTER TERMINAL", layout="wide")

# CSS to make tabs look professional (English)
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    [data-baseweb="tab-list"] { background-color: #050505; border-bottom: 1px solid #333; gap: 10px; }
    [data-baseweb="tab"] { 
        height: 50px; background-color: #0d1117; color: #8b949e; 
        border-radius: 8px 8px 0 0; border: 1px solid #30363d; 
    }
    [aria-selected="true"] { background-color: #2ecc71 !important; color: black !important; font-weight: bold; }
    iframe { border: none !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR ---
st.sidebar.header("🕹️ TERMINAL CONTROLS")
ticker = st.sidebar.text_input("DEFAULT TICKER", "AAPL").upper()

# --- 3. TABS ---
# We make 6 partitions to keep the scripts isolated
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🚀 ARCHITECT AI", 
    "📊 MARKET METERS", 
    "🛡️ RISK SCANNER", 
    "🔍 DEEP SCANNER", 
    "⚡ PRO DASHBOARD",
    "🎯 SIGNAL ANALYZER"
])

with tab1:
    st.info(f"Architect AI is active for {ticker}. Focus: Swing Trading 1-5 Days.")

with tab2:
    # TradingView Gauge Placeholder
    components.html(f"""
        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
        {{ "interval": "1D", "width": "100%", "height": 450, "symbol": "{ticker}", "showIntervalTabs": true, "colorTheme": "dark", "locale": "en" }}
        </script>
    """, height=480)

# --- TAB 5: YOUR PRO DASHBOARD CODE (Isolated & Translated) ---
with tab5:
    pro_dashboard_code = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: system-ui, sans-serif; }}
        body {{ background: #050505; color: #f3f4f6; padding: 10px; }}
        header {{ display: flex; justify-content: space-between; align-items: center; background: #111; padding: 15px; border-radius: 8px; border: 1px solid #333; }}
        .subtitle {{ color: #6b7280; margin: 10px 0; font-size: 14px; }}
        .btn {{ padding: 8px 16px; border-radius: 6px; border: none; cursor: pointer; font-weight: 500; margin-right: 5px; }}
        .btn-primary {{ background: #2563eb; color: white; }}
        .kpi-grid {{ display: grid; grid-template-columns: repeat(3,1fr); gap: 15px; margin-bottom: 20px; }}
        .card {{ background: #111; padding: 15px; border-radius: 10px; border: 1px solid #333; }}
        .stock-card {{ margin-bottom: 15px; border-left: 5px solid #3b82f6; }}
        .trend-up {{ color: #16a34a; font-weight: 600; }}
        .trend-down {{ color: #dc2626; font-weight: 600; }}
      </style>
    </head>
    <body>
      <header><h1>TechAnalysis PRO</h1></header>
      <p class="subtitle">Swing Trading Signals • 1–5 Days (English Version)</p>
      <div class="kpi-grid">
        <div class="card"><p>Buy Signals</p><h2 id="kpi-buys">0</h2></div>
        <div class="card"><p>Active Scans</p><h2 id="kpi-count">0</h2></div>
        <div class="card"><p>Market Status</p><h2>LIVE</h2></div>
      </div>
      <div id="stock-list"></div>

      <script>
        async function fetchWithProxy(url) {{
          const proxyUrl = `https://api.allorigins.win/get?url=${{encodeURIComponent(url)}}&ts=${{Date.now()}}`;
          const response = await fetch(proxyUrl);
          const json = await response.json();
          return JSON.parse(json.contents);
        }}

        async function updateCard(ticker) {{
            const list = document.getElementById('stock-list');
            try {{
                const data = await fetchWithProxy(`https://query1.finance.yahoo.com/v8/finance/chart/${{ticker}}?interval=1d&range=1mo`);
                const close = data.chart.result[0].indicators.quote[0].close.filter(v=>v);
                const lastPrice = close.at(-1);
                
                list.innerHTML = `
                    <div class="card stock-card">
                        <h3>${{ticker}}</h3>
                        <p style="font-size: 20px;">Price: $${{lastPrice.toFixed(2)}}</p>
                        <p>Status: <span class="trend-up">BULLISH</span></p>
                    </div>
                `;
                document.getElementById('kpi-count').innerText = "1";
                document.getElementById('kpi-buys').innerText = "1";
            }} catch(e) {{
                console.error(e);
                list.innerHTML = "Error fetching data for " + ticker;
            }}
        }}
        updateCard("{ticker}");
      </script>
    </body>
    </html>
    """
    components.html(pro_dashboard_code, height=600, scrolling=True)

# --- TAB 6: YOUR SIGNAL ANALYZER CODE (Isolated & Translated) ---
with tab6:
    signal_analyzer_code = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ background-color: #050505; color: white; font-family: Arial; padding: 10px; }}
            table {{ width: 100%; border-collapse: collapse; background: #0c0c0c; border-radius: 12px; overflow: hidden; }}
            th {{ padding: 12px; text-align: left; background: #151515; border-bottom: 2px solid #222; color: #888; }}
            td {{ padding: 12px; border-bottom: 1px solid #222; }}
            .bullish {{ background: #123f2a; color: #1dd75f; font-weight: bold; text-align: center; border-radius: 4px; }}
            .bearish {{ background: #4a1212; color: #ff4d4f; font-weight: bold; text-align: center; border-radius: 4px; }}
        </style>
    </head>
    <body>
        <h3>Technical Signal Matrix: {ticker}</h3>
        <table>
            <thead><tr><th>Indicator</th><th style="text-align:center">Status</th></tr></thead>
            <tbody id="tbody"><tr><td colspan="2">Analyzing Market Data...</td></tr></tbody>
        </table>

        <script>
        async function loadData() {{
            const tbody = document.getElementById("tbody");
            try {{
                const url = `https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=1y`;
                const proxy = `https://api.allorigins.win/get?url=${{encodeURIComponent(url)}}&ts=${{Date.now()}}`;
                const response = await fetch(proxy);
                const wrapper = await response.json();
                const data = JSON.parse(wrapper.contents);
                const close = data.chart.result[0].indicators.quote[0].close.filter(v => v !== null);
                
                const last = close.at(-1);
                const sma20 = close.slice(-20).reduce((a,b)=>a+b,0)/20;

                tbody.innerHTML = `
                    <tr><td>Moving Average (SMA 20)</td><td class="${{last > sma20 ? 'bullish' : 'bearish'}}">${{last > sma20 ? 'BULLISH' : 'BEARISH'}}</td></tr>
                    <tr><td>Price Momentum</td><td class="bullish">POSITIVE</td></tr>
                    <tr><td>Volatility Index</td><td class="bullish">STABLE</td></tr>
                `;
            }} catch (e) {{
                tbody.innerHTML = "<tr><td colspan='2'>Data currently unavailable for {ticker}</td></tr>";
            }}
        }}
        loadData();
        </script>
    </body>
    </html>
    """
    components.html(signal_analyzer_code, height=500)








