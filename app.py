import streamlit as st
import streamlit.components.v1 as components

# 1. Pagina configuratie
st.set_page_config(page_title="SST TRADING SUITE", layout="wide")

# Styling voor de interface en Tabs
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding: 0px; background-color: #050608; }
    .stTabs [data-baseweb="tab-list"] { background-color: #0d1117; border-bottom: 1px solid #30363d; gap: 10px; padding: 10px; }
    .stTabs [data-baseweb="tab"] { color: #8b949e; font-weight: bold; }
    .stTabs [aria-selected="true"] { color: #2f81f7 !important; border-bottom-color: #2f81f7 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- TOOL 1: SMART TERMINAL ---
tool1_html = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #050608; color: white; font-family: sans-serif; padding: 20px; }
        .data-strip { background: #11141b; border-radius: 1rem; border: 1px solid #1f2937; margin-bottom: 1rem; padding: 1.2rem; border-left: 6px solid #3b82f6; }
        input { background: #11141b; border: 1px solid #1f2937; padding: 10px; border-radius: 0.5rem; color: white; outline: none; }
        button { background: #2563eb; padding: 10px 20px; border-radius: 0.5rem; font-weight: bold; cursor: pointer; color: white; border:none; }
    </style>
</head>
<body>
    <div style="max-width: 500px; margin: auto;">
        <div style="display: flex; gap: 10px; margin-bottom: 20px;">
            <input id="tIn" type="text" value="NVDA" style="flex:1;">
            <button onclick="scan()">SCAN</button>
        </div>
        <div id="sig" style="background: #1e3a8a; padding: 15px; border-radius: 1rem; text-align: center; margin-bottom: 10px; font-weight: bold;">--</div>
        <div class="data-strip">Price: <span id="prc">--</span></div>
        <div id="tv-chart" style="height: 300px; border-radius: 1rem; overflow: hidden; border: 1px solid #1f2937;"></div>
    </div>
    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>
        async function scan() {
            const t = document.getElementById('tIn').value.toUpperCase();
            const r = await fetch('https://finnhub.io/api/v1/quote?symbol='+t+'&token=d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0');
            const d = await r.json();
            document.getElementById('prc').innerText = '$' + d.c;
            document.getElementById('sig').innerText = d.dp > 0 ? "BUY SIGNAL" : "HOLD";
            new TradingView.widget({"autosize": true, "symbol": t, "interval": "D", "theme": "dark", "container_id": "tv-chart", "hide_top_toolbar": true});
        }
        window.onload = scan;
    </script>
</body>
</html>
"""

# --- TOOL 2: RISK SYSTEM ---
tool2_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: sans-serif; background: #0d1117; color: #c9d1d9; padding: 20px; }
        .card { background: #161b22; padding: 20px; border-radius: 12px; border: 1px solid #30363d; border-left: 8px solid #39d353; margin-top: 10px; }
        input { background: #0d1117; border: 1px solid #30363d; color: white; padding: 10px; border-radius: 6px; }
        button { background: #1f6feb; color: white; border: none; padding: 10px; border-radius: 6px; cursor: pointer; }
    </style>
</head>
<body>
    <input type="text" id="rIn" placeholder="TICKER...">
    <button onclick="risk()">ANALYSE RISK</button>
    <div id="rOut"></div>
    <script>
        async function risk() {
            const t = document.getElementById('rIn').value.toUpperCase();
            const r = await fetch('https://finnhub.io/api/v1/quote?symbol='+t+'&token=d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0');
            const d = await r.json();
            document.getElementById('rOut').innerHTML = `<div class="card"><h3>${t}</h3><p>Entry: $${d.c}</p><p style="color:#39d353">Target: $${(d.c*1.07).toFixed(2)}</p><p style="color:#f85149">Stop: $${(d.c*0.95).toFixed(2)}</p></div>`;
        }
    </script>
</body>
</html>
"""

# --- TOOL 3: PRO SCANNER v5.7 ---
tool3_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { background: #0d1117; color: #e6edf3; font-family: sans-serif; padding: 20px; }
        .spinner { border: 3px solid rgba(47, 129, 247, 0.2); border-top: 3px solid #2f81f7; border-radius: 50%; width: 20px; height: 20px; display: inline-block; animation: spin 0.8s linear infinite; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th { text-align: left; color: #8b949e; font-size: 12px; padding: 10px; border-bottom: 1px solid #30363d; }
        td { padding: 12px 10px; border-bottom: 1px solid #21262d; }
        .badge { padding: 4px 8px; border-radius: 4px; font-size: 10px; font-weight: bold; color: white; }
    </style>
</head>
<body>
    <div style="display: flex; gap: 10px;">
        <textarea id="listIn" style="flex:1; background:#010409; color:white; border:1px solid #30363d; border-radius:8px; padding:10px;">AAPL,NVDA,TSLA,AMD,MSFT</textarea>
        <button onclick="run()" style="background:#238636; color:white; border:none; border-radius:8px; padding:0 20px; cursor:pointer; font-weight:bold;">RUN SCAN</button>
    </div>
    <div id="stat" style="display:none; margin-top:20px; color:#58a6ff;"><div class="spinner"></div> Scanning...</div>
    <table id="tbl" style="display:none;">
        <thead><tr><th>Symbol</th><th>Price</th><th>AI Score</th><th>Signal</th></tr></thead>
        <tbody id="tbody"></tbody>
    </table>
    <script>
        async function run() {
            const tickers = document.getElementById('listIn').value.split(/[,\s\n]+/);
            document.getElementById('stat').style.display = 'block';
            document.getElementById('tbl').style.display = 'none';
            const body = document.getElementById('tbody');
            body.innerHTML = '';
            for (let t of tickers) {
                t = t.trim().toUpperCase();
                if(!t) continue;
                try {
                    const r = await fetch('https://finnhub.io/api/v1/quote?symbol='+t+'&token=d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0');
                    const d = await r.json();
                    if(d.c) {
                        const score = Math.round(50 + (d.dp * 5));
                        const row = `<tr><td><b>${t}</b></td><td>$${d.c}</td><td>${score}</td><td><span class="badge" style="background:${score > 55 ? '#238636' : '#2f81f7'}">${score > 55 ? 'BUY' : 'HOLD'}</span></td></tr>`;
                        body.insertAdjacentHTML('beforeend', row);
                    }
                } catch(e) {}
            }
            document.getElementById('stat').style.display = 'none';
            document.getElementById('tbl').style.display = 'table';
        }
    </script>
</body>
</html>
"""

# --- STREAMLIT TABS RENDEREN ---
t1, t2, t3 = st.tabs(["🚀 SMART TERMINAL", "🛡️ RISK SYSTEM", "📊 PRO SCANNER v5.7"])

with t1:
    components.html(tool1_html, height=700)
with t2:
    components.html(tool2_html, height=700)
with t3:
    components.html(tool3_html, height=800, scrolling=True)





















