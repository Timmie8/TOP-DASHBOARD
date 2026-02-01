import streamlit as st
import streamlit.components.v1 as components

# 1. Pagina instellingen
st.set_page_config(page_title="SST ULTRA TERMINAL", layout="wide")

# Verberg Streamlit decoratie
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

# --- DE TOOLS ---

# TOOL 1 & 2 blijven hetzelfde als in je vorige werkende versies.
# Hieronder de gerepareerde TOOL 3 (PRO SCANNER v5.7)

tool_pro_v57 = """
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body { background: #0d1117; color: #e6edf3; font-family: 'Inter', sans-serif; padding: 20px; margin: 0; }
        #sst-terminal-pro { max-width: 1000px; margin: 0 auto; background: #0d1117; padding: 20px; border-radius: 20px; border: 1px solid #30363d; }
        .watchlist-pill { background: #21262d; border: 1px solid #30363d; color: #c9d1d9; padding: 5px 10px; border-radius: 6px; display: inline-flex; align-items: center; gap: 8px; font-weight: 700; font-size: 0.8rem; margin: 2px; }
        .rank-row { border-bottom: 1px solid #21262d; transition: 0.2s; cursor: pointer; }
        .rank-row:hover { background: #1f242c; }
        .badge { padding: 5px 10px; border-radius: 6px; font-size: 0.65rem; font-weight: 900; text-transform: uppercase; width: 85px; display: inline-block; text-align: center; color: white; }
        .spinner { border: 3px solid rgba(47, 129, 247, 0.2); border-top: 3px solid #2f81f7; border-radius: 50%; width: 20px; height: 20px; display: inline-block; animation: spin 0.8s linear infinite; vertical-align: middle; margin-right: 10px; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        #modalOverlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); z-index: 1000; justify-content: center; align-items: center; }
        #modalContent { background: #0d1117; width: 90%; max-width: 400px; padding: 30px; border-radius: 24px; border: 1px solid #30363d; box-shadow: 0 20px 50px rgba(0,0,0,0.5); }
        textarea { width: 100%; background: #010409; border: 1px solid #30363d; color: white; border-radius: 8px; padding: 10px; height: 40px; resize: none; outline: none; }
        button { cursor: pointer; border: none; border-radius: 8px; font-weight: bold; }
    </style>
</head>
<body>
<div id="sst-terminal-pro">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; gap: 15px;">
        <div style="flex: 1;"><h2 style="margin:0; font-size: 1.5rem;">SST <span style="color: #2f81f7;">PRO</span> v5.7</h2></div>
        <div style="flex: 2; display: flex; gap: 8px;">
            <textarea id="tickerInput" placeholder="AAPL, TSLA, NVDA..."></textarea>
            <button onclick="addTickers()" style="background:#30363d; color:white; padding: 0 15px;">ADD</button>
            <button onclick="runScanner()" style="background:#238636; color:white; padding: 0 20px; min-width: 100px;">RUN SCAN</button>
        </div>
    </div>

    <div id="watchlistBar" style="margin-bottom: 20px; min-height: 40px; padding: 10px; background: rgba(255,255,255,0.03); border-radius: 10px;"></div>
    
    <div id="statusDiv" style="display:none; text-align:center; padding: 20px; background: #161b22; border-radius: 12px; margin-bottom: 20px;">
        <div class="spinner"></div> <span id="progressLabel" style="color:#58a6ff; font-weight:bold;">ANALYZING...</span>
    </div>

    <div id="tableDiv" style="display:none;">
        <table style="width:100%; border-collapse:collapse;">
            <thead><tr style="color:#8b949e; font-size:12px; text-transform:uppercase; border-bottom:1px solid #30363d;"><th align="left" style="padding:10px;">Symbol</th><th align="left">Price</th><th align="left">AI Score</th><th align="left">Action</th></tr></thead>
            <tbody id="rankingBody"></tbody>
        </table>
    </div>
</div>

<div id="modalOverlay" onclick="closeModal()">
    <div id="modalContent" onclick="event.stopPropagation()">
        <h2 id="mSym" style="margin:0; font-size: 2rem;"></h2>
        <p id="mPrice" style="color:#8b949e; margin: 5px 0 20px 0;"></p>
        <div style="background:#161b22; padding:20px; border-radius:15px; border:1px solid #30363d;">
            <div style="display:flex; justify-content:space-between; margin-bottom:10px;"><span>AI Target</span><b id="mTarget" style="color:#3fb950;"></b></div>
            <div style="display:flex; justify-content:space-between;"><span>AI Stoploss</span><b id="mStop" style="color:#f85149;"></b></div>
        </div>
        <button onclick="closeModal()" style="width:100%; margin-top:20px; padding:12px; background:#2f81f7; color:white;">SLUITEN</button>
    </div>
</div>

<script>
    const KEY = "d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0";
    let list = ['NVDA', 'TSLA', 'AAPL', 'AMD', 'MSFT'];

    function renderList() {
        const b = document.getElementById('watchlistBar');
        b.innerHTML = list.map(t => `<div class="watchlist-pill"><span>${t}</span><span onclick="remove('${t}')" style="color:#f85149; cursor:pointer;">&times;</span></div>`).join('');
    }

    function addTickers() {
        const val = document.getElementById('tickerInput').value;
        val.split(/[,\s\n]+/).forEach(t => {
            t = t.trim().toUpperCase();
            if(t && !list.includes(t)) list.push(t);
        });
        document.getElementById('tickerInput').value = '';
        renderList();
    }

    function remove(t) { list = list.filter(i => i !== t); renderList(); }

    async function runScanner() {
        if(list.length === 0) return alert("Voeg eerst tickers toe.");
        document.getElementById('statusDiv').style.display = 'block';
        document.getElementById('tableDiv').style.display = 'none';
        const body = document.getElementById('rankingBody');
        body.innerHTML = '';
        let results = [];

        for(let i=0; i < list.length; i++) {
            document.getElementById('progressLabel').innerText = `SCANNING: ${i+1}/${list.length} (${list[i]})`;
            try {
                const r = await fetch(`https://finnhub.io/api/v1/quote?symbol=${list[i]}&token=${KEY}`);
                const d = await r.json();
                if(d.c && d.c !== 0) {
                    const score = Math.min(Math.max(Math.round(50 + (d.dp * 8)), 10), 99);
                    results.push({t: list[i], p: d.c, s: score, dp: d.dp});
                }
            } catch(e) { console.log("Fout bij "+list[i]); }
            await new Promise(r => setTimeout(r, 200)); 
        }

        results.sort((a,b) => b.s - a.s);
        results.forEach(res => {
            const tr = document.createElement('tr');
            tr.className = 'rank-row';
            tr.onclick = () => showDetail(res);
            tr.innerHTML = `<td style="padding:15px;"><b>${res.t}</b></td><td>$${res.p.toFixed(2)}</td><td>${res.s}</td><td><span class="badge" style="background:${res.s > 60 ? '#238636' : (res.s < 40 ? '#f85149' : '#2f81f7')}">${res.s > 60 ? 'BUY' : (res.s < 40 ? 'AVOID' : 'HOLD')}</span></td>`;
            body.appendChild(tr);
        });

        document.getElementById('statusDiv').style.display = 'none';
        document.getElementById('tableDiv').style.display = 'block';
    }

    function showDetail(res) {
        document.getElementById('mSym').innerText = res.t;
        document.getElementById('mPrice').innerText = `Huidige Prijs: $${res.p.toFixed(2)}`;
        document.getElementById('mTarget').innerText = `$${(res.p * (1 + (res.s/1000))).toFixed(2)}`;
        document.getElementById('mStop').innerText = `$${(res.p * 0.95).toFixed(2)}`;
        document.getElementById('modalOverlay').style.display = 'flex';
    }

    function closeModal() { document.getElementById('modalOverlay').style.display = 'none'; }
    renderList();
</script>
</body>
</html>
"""

# --- RENDER TABS ---
# Ik gebruik hier alleen even de nieuwe scanner in tab 3 om te testen of deze werkt.
tab1, tab2, tab3 = st.tabs(["🚀 SMART TERMINAL", "🛡️ RISK SYSTEM", "📊 PRO SCANNER v5.7"])

with tab1:
    st.info("Eerste tool hier...") # Je kunt hier de tool_smart_terminal code van eerder plakken

with tab3:
    components.html(tool_pro_v57, height=1000, scrolling=True)




















