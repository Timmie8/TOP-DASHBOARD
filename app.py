import streamlit as st
import streamlit.components.v1 as components

# 1. Pagina instellingen
st.set_page_config(page_title="SST ULTRA TERMINAL", layout="wide")

# Verberg Streamlit balken en styling voor de tabs
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

# --- DEFINITIES VAN DE TOOLS ---

# TOOL 1: AI SMART TERMINAL (BLAUW)
tool_smart_terminal = """
<!DOCTYPE html>
<html lang="en">
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #050608; color: white; font-family: sans-serif; padding: 20px; }
        .data-strip { background: #11141b; border-radius: 1.5rem; border: 1px solid #1f2937; margin-bottom: 1rem; padding: 1.5rem; border-left: 8px solid #3b82f6; }
        .value { font-size: 2.5rem; font-weight: 900; }
        .label { color: #6b7280; text-transform: uppercase; font-size: 0.75rem; font-weight: 800; }
        #chart_box { height: 400px; border-radius: 1.5rem; overflow: hidden; border: 1px solid #1f2937; }
        input { background: #11141b; border: 2px solid #1f2937; padding: 15px; border-radius: 1rem; color: white; width: 60%; font-size: 1.5rem; outline: none; }
        button { background: #2563eb; padding: 15px 30px; border-radius: 1rem; font-weight: 900; cursor: pointer; border: none; color: white; }
    </style>
</head>
<body>
    <div style="max-width: 600px; margin: auto;">
        <div style="display: flex; gap: 10px; margin-bottom: 20px;">
            <input id="tickerInput" type="text" value="NVDA">
            <button onclick="fetchAIData()">SCAN</button>
        </div>
        <div id="signalCard" style="background: #1e3a8a; padding: 20px; border-radius: 1.5rem; text-align: center; margin-bottom: 15px;"><p class="label">AI Decision</p><div id="adviceVal" style="font-size: 2rem; font-weight: 900;">--</div></div>
        <div class="data-strip"><p class="label">Market Price</p><div id="priceVal" class="value">--</div></div>
        <div id="chart_box"><div id="chart_container" style="height: 100%;"></div></div>
    </div>
    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>
        async function fetchAIData() {
            const ticker = document.getElementById('tickerInput').value.toUpperCase();
            const res = await fetch('https://finnhub.io/api/v1/quote?symbol='+ticker+'&token=d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0');
            const data = await res.json();
            document.getElementById('priceVal').innerText = '$' + data.c.toFixed(2);
            document.getElementById('adviceVal').innerText = data.dp > 0 ? "STRONG BUY" : "HOLD";
            document.getElementById('signalCard').style.backgroundColor = data.dp > 0 ? "#065f46" : "#1e3a8a";
            new TradingView.widget({"autosize": true, "symbol": ticker, "interval": "D", "theme": "dark", "container_id": "chart_container", "hide_top_toolbar": true});
        }
        window.onload = fetchAIData;
    </script>
</body>
</html>
"""

# TOOL 2: RISK & TIER SYSTEM
tool_risk_tier = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: sans-serif; background: #0d1117; color: #c9d1d9; padding: 20px; }
        .container { max-width: 850px; margin: auto; background: #161b22; padding: 25px; border-radius: 12px; border: 1px solid #30363d; }
        .search-group { display: flex; gap: 10px; margin-bottom: 15px; }
        input { flex: 1; background: #0d1117; border: 1px solid #30363d; color: white; padding: 12px; border-radius: 6px; }
        button { border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-weight: bold; background: #1f6feb; color: white; }
        .card { position: relative; background: #0d1117; border: 2px solid #30363d; padding: 20px; border-radius: 10px; margin-bottom: 15px; border-left: 8px solid #39d353; }
        .levels { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-top: 15px; }
        .level { background: #161b22; padding: 10px; border-radius: 6px; text-align: center; border: 1px solid #30363d; }
    </style>
</head>
<body>
<div class="container">
    <div class="search-group"><input type="text" id="manualInput" placeholder="TICKER..."><button onclick="manualSearch()">AI ANALYSE</button></div>
    <div id="display"></div>
</div>
<script>
async function manualSearch() {
    const t = document.getElementById("manualInput").value.toUpperCase();
    const res = await fetch('https://finnhub.io/api/v1/quote?symbol='+t+'&token=d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0');
    const d = await res.json();
    const html = `<div class="card"><strong>${t}</strong><div class="levels"><div class="level">$${(d.c*0.96).toFixed(2)}<br><small>STOP</small></div><div class="level">$${d.c.toFixed(2)}<br><small>ENTRY</small></div><div class="level">$${(d.c*1.08).toFixed(2)}<br><small>TARGET</small></div></div></div>`;
    document.getElementById("display").insertAdjacentHTML('afterbegin', html);
}
</script>
</body>
</html>
"""

# TOOL 3: SST TERMINAL PRO v5.7 (JOUW NIEUWE CODE)
tool_pro_v57 = """
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body { background: #0d1117; color: #e6edf3; font-family: 'Inter', sans-serif; padding: 20px; margin: 0; }
        #sst-terminal-pro { max-width: 1100px; margin: 0 auto; background: #0d1117; padding: 20px; border-radius: 20px; border: 1px solid #30363d; }
        .watchlist-pill { background: #21262d; border: 1px solid #30363d; color: #c9d1d9; padding: 6px 12px; border-radius: 6px; display: flex; align-items: center; gap: 8px; font-weight: 700; font-size: 0.8rem; margin-bottom: 5px; }
        .rank-row { border-bottom: 1px solid #21262d; transition: 0.2s; cursor: pointer; }
        .rank-row:hover { background: #1f242c; }
        .badge { padding: 5px 10px; border-radius: 6px; font-size: 0.65rem; font-weight: 900; text-transform: uppercase; width: 85px; display: inline-block; text-align: center; }
        .spinner { border: 3px solid rgba(47, 129, 247, 0.2); border-top: 3px solid #2f81f7; border-radius: 50%; width: 20px; height: 20px; display: inline-block; animation: spin 0.8s linear infinite; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        /* Modal simple style */
        #modalOverlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); z-index: 1000; justify-content: center; align-items: center; }
        #modalContent { background: #0d1117; width: 90%; max-width: 450px; padding: 30px; border-radius: 20px; border: 1px solid #30363d; }
    </style>
</head>
<body>
<div id="sst-terminal-pro">
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #30363d; padding-bottom: 20px; margin-bottom: 20px;">
        <div><h2 style="margin:0;">SST <span style="color: #2f81f7;">TERMINAL</span> v5.7</h2></div>
        <div style="display: flex; gap: 10px;">
            <textarea id="tickerInput" placeholder="AAPL, NVDA..." style="background:#010409; border:1px solid #30363d; color:white; border-radius:8px; padding:10px;"></textarea>
            <button onclick="addMultipleTickers()" style="background:#30363d; color:white; border:none; padding:10px; border-radius:8px; cursor:pointer;">ADD</button>
            <button onclick="startAutoScanner()" style="background:#238636; color:white; border:none; padding:10px; border-radius:8px; font-weight:bold; cursor:pointer;">SCAN</button>
        </div>
    </div>
    <div id="watchlistBar" style="display:flex; flex-wrap:wrap; gap:5px; margin-bottom:20px;"></div>
    <div id="scannerStatus" style="display:none; text-align:center; padding:10px; color:#58a6ff;"><div class="spinner"></div> SCANNING: <span id="scanProgress">0/0</span></div>
    <div id="rankingContainer" style="display:none;">
        <table style="width:100%; border-collapse:collapse;">
            <thead><tr style="color:#8b949e; font-size:12px; border-bottom:1px solid #30363d;"><th align="left" style="padding:10px;">Rank</th><th align="left">Symbol</th><th align="left">Score</th><th align="left">Signal</th></tr></thead>
            <tbody id="rankingBody"></tbody>
        </table>
    </div>
</div>

<div id="modalOverlay" onclick="closeModal()">
    <div id="modalContent" onclick="event.stopPropagation()">
        <h2 id="modalSymbol" style="margin:0 0 10px 0;"></h2>
        <div id="modalPrice" style="color:#8b949e; margin-bottom:20px;"></div>
        <div style="background:#161b22; padding:15px; border-radius:12px; border:1px solid #30363d;">
            <div style="display:flex; justify-content:space-between;"><span>Target:</span><b id="modalTarget" style="color:#3fb950;"></b></div>
            <div style="display:flex; justify-content:space-between; margin-top:10px;"><span>Stop:</span><b id="modalStop" style="color:#f85149;"></b></div>
        </div>
        <button onclick="closeModal()" style="width:100%; margin-top:20px; padding:10px; background:#30363d; color:white; border:none; border-radius:8px; cursor:pointer;">CLOSE</button>
    </div>
</div>

<script>
    const SST_KEY = "d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0";
    let watchlist = ['NVDA', 'TSLA', 'AAPL', 'AMD'];

    function renderWatchlist() {
        const bar = document.getElementById('watchlistBar');
        bar.innerHTML = '';
        watchlist.forEach(t => {
            const el = document.createElement('div'); el.className = 'watchlist-pill';
            el.innerHTML = `<span>${t}</span><span onclick="removeFromWatchlist('${t}')" style="cursor:pointer;">&times;</span>`;
            bar.appendChild(el);
        });
    }

    function addMultipleTickers() {
        const val = document.getElementById('tickerInput').value;
        val.split(/[,\s\n]+/).forEach(raw => {
            const t = raw.trim().toUpperCase();
            if(t && !watchlist.includes(t)) watchlist.push(t);
        });
        renderWatchlist();
        document.getElementById('tickerInput').value = '';
    }

    function removeFromWatchlist(t) { watchlist = watchlist.filter(i => i !== t); renderWatchlist(); }

    async function startAutoScanner() {
        const statusDiv = document.getElementById('scannerStatus');
        const rankingBody = document.getElementById('rankingBody');
        statusDiv.style.display = 'block';
        document.getElementById('rankingContainer').style.display = 'none';
        let results = [];
        for(let i=0; i<watchlist.length; i++) {
            document.getElementById('scanProgress').innerText = `${i+1}/${watchlist.length}`;
            try {
                const r = await fetch(`https://finnhub.io/api/v1/quote?symbol=${watchlist[i]}&token=${SST_KEY}`);
                const d = await r.json();
                if(d.c) results.push({ticker: watchlist[i], price: d.c, score: Math.round(50 + (d.dp * 5))});
            } catch(e) {}
            await new Promise(r => setTimeout(r, 150));
        }
        results.sort((a,b) => b.score - a.score);
        rankingBody.innerHTML = '';
        results.forEach((res, idx) => {
            const row = document.createElement('tr'); row.className = 'rank-row';
            row.onclick = () => showDetails(res);
            row.innerHTML = `<td style="padding:15px;">#${idx+1}</td><td><b>${res.ticker}</b></td><td>${res.score}</td><td><span class="badge" style="background:${res.score > 60 ? '#238636' : '#2f81f7'}">${res.score > 60 ? 'BUY' : 'HOLD'}</span></td>`;
            rankingBody.appendChild(row);
        });
        statusDiv.style.display = 'none';
        document.getElementById('rankingContainer').style.display = 'block';
    }

    function showDetails(d) {
        document.getElementById('modalSymbol').innerText = d.ticker;
        document.getElementById('modalPrice').innerText = `Entry: $${d.price.toFixed(2)}`;
        document.getElementById('modalTarget').innerText = `$${(d.price*1.06).toFixed(2)}`;
        document.getElementById('modalStop').innerText = `$${(d.price*0.96).toFixed(2)}`;
        document.getElementById('modalOverlay').style.display = 'flex';
    }
    function closeModal() { document.getElementById('modalOverlay').style.display = 'none'; }
    renderWatchlist();
</script>
</body>
</html>
"""

# --- RENDEREN VAN DE TABS ---
tab1, tab2, tab3 = st.tabs(["🚀 SMART TERMINAL", "🛡️ RISK SYSTEM", "📊 PRO SCANNER v5.7"])

with tab1:
    components.html(tool_smart_terminal, height=800, scrolling=True)

with tab2:
    components.html(tool_risk_tier, height=800, scrolling=True)

with tab3:
    components.html(tool_pro_v57, height=1000, scrolling=True)



















