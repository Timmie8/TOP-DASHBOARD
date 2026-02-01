import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="SST AI TRADER", layout="wide")

# CSS voor Streamlit Layout
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .block-container { padding: 0px; background-color: #050608; }
    .stTabs [data-baseweb="tab-list"] { background-color: #0d1117; padding: 10px; border-bottom: 1px solid #30363d; }
    .stTabs [data-baseweb="tab"] { color: #8b949e; }
    .stTabs [aria-selected="true"] { color: #2f81f7 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- TOOL 1: DE ORIGINELE SMART TERMINAL ---
tool1_html = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #050608; color: white; font-family: sans-serif; padding: 20px; }
        .data-strip { background: #11141b; border-radius: 1.5rem; border: 1px solid #1f2937; margin-bottom: 1rem; padding: 1.5rem; border-left: 8px solid #3b82f6; }
        .value { font-size: 2.5rem; font-weight: 900; }
        .label { color: #6b7280; text-transform: uppercase; font-size: 0.75rem; font-weight: 800; }
        #chart_box { height: 400px; border-radius: 1.5rem; overflow: hidden; border: 1px solid #1f2937; margin-top: 20px; }
        input { background: #11141b; border: 2px solid #1f2937; padding: 15px; border-radius: 1rem; color: white; width: 60%; font-size: 1.2rem; outline: none; }
        button { background: #2563eb; padding: 15px 30px; border-radius: 1rem; font-weight: 900; cursor: pointer; border: none; color: white; }
    </style>
</head>
<body>
    <div style="max-width: 800px; margin: auto;">
        <div style="display: flex; gap: 10px; margin-bottom: 20px;">
            <input id="tickerInput" type="text" value="NVDA">
            <button onclick="fetchAIData()">SCAN</button>
        </div>
        <div id="signalCard" style="background: #1e3a8a; padding: 20px; border-radius: 1.5rem; text-align: center; margin-bottom: 15px;">
            <p class="label">AI Decision</p>
            <div id="adviceVal" style="font-size: 2rem; font-weight: 900;">READY</div>
        </div>
        <div class="data-strip">
            <p class="label">Market Price</p>
            <div id="priceVal" class="value">--</div>
        </div>
        <div class="data-strip" style="border-left-color: #10b981;">
            <p class="label">AI Profit Target</p>
            <div id="targetVal" class="value" style="color: #10b981;">--</div>
        </div>
        <div id="chart_box"><div id="chart_container" style="height: 100%;"></div></div>
    </div>
    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>
        async function fetchAIData() {
            const ticker = document.getElementById('tickerInput').value.toUpperCase();
            try {
                const res = await fetch('https://finnhub.io/api/v1/quote?symbol='+ticker+'&token=d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0');
                const data = await res.json();
                document.getElementById('priceVal').innerText = '$' + data.c.toFixed(2);
                document.getElementById('targetVal').innerText = '$' + (data.c * 1.05).toFixed(2);
                document.getElementById('adviceVal').innerText = data.dp > 0 ? "STRONG BUY" : "HOLD / WATCH";
                document.getElementById('signalCard').style.backgroundColor = data.dp > 0 ? "#065f46" : "#1e3a8a";
                
                new TradingView.widget({
                    "autosize": true, "symbol": ticker, "interval": "D", "theme": "dark", 
                    "container_id": "chart_container", "style": "1", "hide_top_toolbar": true
                });
            } catch(e) { alert("Ticker niet gevonden"); }
        }
        window.onload = fetchAIData;
    </script>
</body>
</html>
"""

# --- TOOL 3: DE PRO SCANNER V5.7 (GEOPTIMALISEERD) ---
tool3_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { background: #0d1117; color: #e6edf3; font-family: sans-serif; padding: 20px; }
        .main-card { max-width: 1000px; margin: auto; background: #0d1117; border: 1px solid #30363d; padding: 30px; border-radius: 20px; }
        textarea { width: 100%; background: #010409; border: 1px solid #30363d; color: white; padding: 15px; border-radius: 12px; margin-bottom: 10px; height: 60px; }
        .btn-scan { background: #238636; color: white; border: none; padding: 15px 30px; border-radius: 10px; font-weight: 900; cursor: pointer; width: 100%; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th { text-align: left; padding: 15px; color: #8b949e; border-bottom: 1px solid #30363d; }
        td { padding: 15px; border-bottom: 1px solid #21262d; cursor: pointer; }
        .badge { padding: 5px 10px; border-radius: 6px; font-weight: bold; font-size: 12px; }
        #modal { display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.9); z-index:100; justify-content:center; align-items:center; }
        .modal-content { background:#0d1117; border:1px solid #30363d; padding:40px; border-radius:24px; width:400px; text-align:center; }
    </style>
</head>
<body>
    <div class="main-card">
        <h2 style="margin-top:0;">SST <span style="color:#2f81f7;">TERMINAL</span> v5.7</h2>
        <textarea id="listIn" placeholder="AAPL, NVDA, TSLA..."></textarea>
        <button class="btn-scan" onclick="runScanner()">RUN AI SCANNER</button>
        
        <div id="loader" style="display:none; text-align:center; margin:20px; color:#58a6ff;">Analysing market data... <span id="prog">0/0</span></div>
        
        <table id="resTable" style="display:none;">
            <thead><tr><th>Rank</th><th>Symbol</th><th>AI Score</th><th>Signal</th></tr></thead>
            <tbody id="resBody"></tbody>
        </table>
    </div>

    <div id="modal" onclick="this.style.display='none'">
        <div class="modal-content" onclick="event.stopPropagation()">
            <h1 id="mSym" style="margin:0;">--</h1>
            <p id="mPrice" style="color:#8b949e;"></p>
            <div style="background:#161b22; padding:20px; border-radius:15px; margin-top:20px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:10px;"><span>AI Target</span><b id="mTarg" style="color:#3fb950;">--</b></div>
                <div style="display:flex; justify-content:space-between;"><span>AI Stop</span><b id="mStop" style="color:#f85149;">--</b></div>
            </div>
            <button onclick="document.getElementById('modal').style.display='none'" style="margin-top:20px; background:#30363d; color:white; border:none; padding:10px 20px; border-radius:8px; cursor:pointer;">Close</button>
        </div>
    </div>

    <script>
        const API_KEY = "d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0";
        async function runScanner() {
            const input = document.getElementById('listIn').value || "AAPL,NVDA,TSLA,AMD,MSFT";
            const tickers = input.split(/[,\s\\n]+/).filter(t => t.trim() !== "");
            
            document.getElementById('loader').style.display = 'block';
            document.getElementById('resTable').style.display = 'none';
            const body = document.getElementById('resBody');
            body.innerHTML = '';
            
            let dataList = [];
            for(let i=0; i<tickers.length; i++) {
                const t = tickers[i].trim().toUpperCase();
                document.getElementById('prog').innerText = (i+1) + "/" + tickers.length;
                try {
                    const r = await fetch(`https://finnhub.io/api/v1/quote?symbol=${t}&token=${API_KEY}`);
                    const d = await r.json();
                    if(d.c) {
                        dataList.push({t: t, p: d.c, s: Math.round(50 + (d.dp * 7))});
                    }
                } catch(e) {}
                await new Promise(r => setTimeout(r, 200));
            }

            dataList.sort((a,b) => b.s - a.s).forEach((item, idx) => {
                const row = `<tr onclick="openModal('${item.t}', ${item.p})">
                    <td>#${idx+1}</td><td><b>${item.t}</b></td><td>${item.s}</td>
                    <td><span class="badge" style="background:${item.s > 55 ? '#238636' : '#2f81f7'}">${item.s > 55 ? 'BUY' : 'HOLD'}</span></td>
                </tr>`;
                body.insertAdjacentHTML('beforeend', row);
            });
            document.getElementById('loader').style.display = 'none';
            document.getElementById('resTable').style.display = 'table';
        }

        function openModal(t, p) {
            document.getElementById('mSym').innerText = t;
            document.getElementById('mPrice').innerText = "Current Price: $" + p.toFixed(2);
            document.getElementById('mTarg').innerText = "$" + (p * 1.08).toFixed(2);
            document.getElementById('mStop').innerText = "$" + (p * 0.95).toFixed(2);
            document.getElementById('modal').style.display = 'flex';
        }
    </script>
</body>
</html>
"""

# --- TABS RENDEREN ---
tab1, tab3 = st.tabs(["🚀 SMART TERMINAL", "📊 PRO SCANNER v5.7"])

with tab1:
    components.html(tool1_html, height=900, scrolling=True)

with tab3:
    components.html(tool3_html, height=900, scrolling=True)





















