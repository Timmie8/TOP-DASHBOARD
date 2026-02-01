import streamlit as st
import streamlit.components.v1 as components

# 1. Pagina instellingen
st.set_page_config(page_title="SST AI TRADING SUITE", layout="wide")

# Globale Styling
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .block-container { padding: 0px; background-color: #050608; }
    .stTabs [data-baseweb="tab-list"] { background-color: #0d1117; padding: 10px; border-bottom: 1px solid #30363d; gap: 15px; }
    .stTabs [data-baseweb="tab"] { color: #8b949e; font-weight: bold; font-size: 14px; }
    .stTabs [aria-selected="true"] { color: #2f81f7 !important; border-bottom-color: #2f81f7 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- TOOL 1: SMART TERMINAL ---
tool1_html = """
<div style="background-color: #050608; color: white; font-family: sans-serif; padding: 20px;">
    <div style="max-width: 800px; margin: auto;">
        <div style="display: flex; gap: 10px; margin-bottom: 20px;">
            <input id="t1Input" type="text" value="NVDA" style="background: #11141b; border: 2px solid #1f2937; padding: 15px; border-radius: 1rem; color: white; width: 60%;">
            <button onclick="fetchT1()" style="background: #2563eb; padding: 15px 30px; border-radius: 1rem; font-weight: 900; color: white; border:none; cursor:pointer;">SCAN</button>
        </div>
        <div id="t1Price" style="font-size: 2.5rem; font-weight: 900; margin-bottom:10px;">--</div>
        <div id="t1Chart" style="height: 400px; border-radius: 1.5rem; overflow: hidden; border: 1px solid #1f2937;"></div>
    </div>
</div>
<script src="https://s3.tradingview.com/tv.js"></script>
<script>
    async function fetchT1() {
        const t = document.getElementById('t1Input').value.toUpperCase();
        const r = await fetch('https://finnhub.io/api/v1/quote?symbol='+t+'&token=d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0');
        const d = await r.json();
        document.getElementById('t1Price').innerText = '$' + d.c.toFixed(2);
        new TradingView.widget({"autosize": true, "symbol": t, "interval": "D", "theme": "dark", "container_id": "t1Chart", "style": "1"});
    }
    window.onload = fetchT1;
</script>
"""

# --- TOOL 2: RISK & TIER ---
tool2_html = """
<div style="background:#0d1117; color:#c9d1d9; font-family:sans-serif; padding:20px;">
    <input id="t2Input" type="text" placeholder="TICKER" style="background:#161b22; border:1px solid #30363d; color:white; padding:12px; border-radius:8px;">
    <button onclick="calcRisk()" style="background:#1f6feb; color:white; border:none; padding:12px 20px; border-radius:8px; cursor:pointer;">ANALYSE RISK</button>
    <div id="t2Out" style="margin-top:20px; padding:20px; border-radius:10px; background:#161b22; border:1px solid #30363d;">Voer een ticker in...</div>
</div>
<script>
async function calcRisk() {
    const t = document.getElementById('t2Input').value.toUpperCase();
    const r = await fetch('https://finnhub.io/api/v1/quote?symbol='+t+'&token=d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0');
    const d = await r.json();
    document.getElementById('t2Out').innerHTML = `<h3>${t}</h3>Entry: $${d.c}<br>Stop Loss: $${(d.c*0.96).toFixed(2)}<br>Target: $${(d.c*1.08).toFixed(2)}`;
}
</script>
"""

# --- TOOL 3: PRO SCANNER ---
tool3_html = """
<div style="background: #0d1117; color: white; font-family: sans-serif; padding: 20px;">
    <textarea id="t3List" style="width: 100%; height: 60px; background: #010409; color: white; border: 1px solid #30363d;">AAPL,NVDA,TSLA,AMD</textarea>
    <button onclick="scanT3()" style="width: 100%; padding: 15px; background: #238636; color: white; border:none; margin-top:10px; cursor:pointer;">RUN BATCH SCAN</button>
    <div id="t3Res" style="margin-top:20px;"></div>
</div>
<script>
async function scanT3() {
    const tickers = document.getElementById('t3List').value.split(',');
    let html = '<table>';
    for(let t of tickers) {
        const r = await fetch('https://finnhub.io/api/v1/quote?symbol='+t.trim().toUpperCase()+'&token=d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0');
        const d = await r.json();
        html += `<tr><td style="padding:10px;">${t}</td><td style="color:${d.dp>0?'#3fb950':'#f85149'}">${d.dp}%</td></tr>`;
    }
    document.getElementById('t3Res').innerHTML = html + '</table>';
}
</script>
"""

# --- TOOL 4: SIGNAL ANALYZER (FULL TECHNICALS) ---
tool4_html = """
<div style="background:#050505; color:white; font-family:Arial; padding:20px;">
    <input id="t4Sym" value="AAPL" style="background:#1c1c1c; border:none; color:white; padding:10px; border-radius:5px;">
    <button onclick="loadT4()" style="background:#2ecc71; padding:10px; border:none; border-radius:5px; cursor:pointer;">LOAD INDICATORS</button>
    <table id="t4Table" style="width:100%; margin-top:20px; border-collapse:collapse;"></table>
</div>
<script>
async function loadT4() {
    const s = document.getElementById('t4Sym').value.toUpperCase();
    const r = await fetch(`https://api.allorigins.win/get?url=${encodeURIComponent('https://query1.finance.yahoo.com/v8/finance/chart/'+s+'?interval=1d&range=1y')}`);
    const j = await r.json(); const d = JSON.parse(j.contents);
    const close = d.chart.result[0].indicators.quote[0].close.filter(v=>v);
    const last = close.at(-1);
    const sma20 = close.slice(-20).reduce((a,b)=>a+b)/20;
    document.getElementById('t4Table').innerHTML = `
        <tr style="border-bottom:1px solid #333"><td>Price</td><td>${last.toFixed(2)}</td></tr>
        <tr style="border-bottom:1px solid #333"><td>SMA 20</td><td style="color:${last>sma20?'#3fb950':'#f85149'}">${last>sma20?'BULLISH':'BEARISH'}</td></tr>
    `;
}
</script>
"""

# --- TOOL 5: TECHANALYSIS PRO ---
tool5_html = """
<div style="background:#050608; color:white; padding:20px; font-family:sans-serif;">
    <h3>Active Portfolio Monitor</h3>
    <button onclick="addT5()" style="padding:10px; background:#2563eb; color:white; border:none; border-radius:5px;">+ Add Ticker</button>
    <div id="t5List" style="margin-top:20px; display:grid; gap:10px;"></div>
</div>
<script>
function addT5() {
    const t = prompt("Ticker?").toUpperCase();
    const el = document.createElement('div');
    el.style = "background:#111; padding:15px; border-left:5px solid #2f81f7; display:flex; justify-content:space-between;";
    el.innerHTML = `<span>${t}</span><span style="color:#2f81f7;">TRACKING...</span>`;
    document.getElementById('t5List').appendChild(el);
}
</script>
"""

# --- TOOL 6: SST ARCHITECT (THE NEW ONE) ---
tool6_html = """
<div id="sst-terminal-final" style="font-family: 'Inter', sans-serif; color: #e6edf3; max-width: 1200px; margin: 0 auto; background: #0d1117; padding: 30px; border-radius: 20px; border: 1px solid #30363d;">
    <div style="display: flex; flex-wrap: wrap; gap: 20px; align-items: center; border-bottom: 1px solid #30363d; padding-bottom: 30px; margin-bottom: 20px;">
        <div style="flex: 1; min-width: 250px;">
            <h2 style="margin: 0; font-size: 1.8rem; font-weight: 900; color: #fff;">SST <span style="color: #2f81f7;">ARCHITECT</span></h2>
            <p style="margin: 5px 0 0; font-size: 0.75rem; color: #8b949e; text-transform: uppercase; font-weight: 800;">Deep Research Engine</p>
        </div>
        <div style="display: flex; gap: 12px; flex-wrap: wrap;">
            <input id="tickerInput6" type="text" placeholder="TICKER" style="background: #010409; border: 1px solid #2f81f7; color: #fff; padding: 15px; border-radius: 12px; font-weight: 800; width: 130px; outline: none;">
            <button onclick="runUltimateAnalysis()" style="background: #238636; color: #fff; border: none; padding: 15px 30px; border-radius: 12px; font-weight: 900; cursor: pointer;">RUN DEEP SCAN</button>
            <button onclick="addToWatchlist()" style="background: transparent; color: #8b949e; border: 1px solid #30363d; padding: 15px; border-radius: 12px; font-weight: 800; cursor: pointer;">+ WATCH</button>
        </div>
    </div>
    <div id="watchlistBar" style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 30px;"></div>
    <div id="scannerDashboard" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 25px;">
        <div id="totalScoreCard" style="background: #161b22; padding: 30px; border-radius: 18px; border: 2px solid #30363d; text-align: center;">
            <span style="font-size: 0.7rem; font-weight: 800; color: #8b949e; text-transform: uppercase;">Aggregate AI Score</span>
            <div id="totalScore" style="font-size: 4rem; font-weight: 900; margin: 15px 0; color: #fff;">--</div>
            <div style="margin-top: 10px; background: #0d1117; height: 30px; border-radius: 8px; border: 1px solid #30363d; overflow: hidden; position: relative;">
                <div id="riskBar" style="height: 100%; width: 0%; transition: 1s; background: #30363d;"></div>
                <div id="riskLabel" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-weight: 900; font-size: 0.7rem; color: #fff;">RISK: --</div>
            </div>
            <div style="margin-top: 10px; background: #0d1117; height: 30px; border-radius: 8px; border: 1px solid #30363d; overflow: hidden; position: relative;">
                <div id="timingBar" style="height: 100%; width: 0%; transition: 1s; background: #30363d;"></div>
                <div id="timingLabel" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-weight: 900; font-size: 0.7rem; color: #fff;">TIMING: --</div>
            </div>
        </div>
        <div style="background: #1c2128; padding: 30px; border-radius: 18px; border: 1px solid #444;">
            <h3 style="margin: 0 0 20px 0; font-size: 1rem; color: #fff;">AI SETUP</h3>
            <p style="font-size: 0.75rem; color: #8b949e; margin:0;">TARGET</p>
            <div id="targetPrice" style="font-size: 1.8rem; font-weight: 900; color: #3fb950;">$0.00</div>
            <p style="font-size: 0.75rem; color: #8b949e; margin: 15px 0 0 0;">STOP LOSS</p>
            <div id="supportPrice" style="font-size: 1.4rem; font-weight: 900; color: #f85149;">$0.00</div>
        </div>
        <div style="background: #161b22; padding: 30px; border-radius: 18px; border: 1px solid #30363d;">
            <h3 id="resSymbol" style="margin: 0; font-size: 2rem; font-weight: 900; color: #fff;">---</h3>
            <p id="verdictDetail" style="font-size: 0.85rem; color: #c9d1d9; line-height: 1.5; margin-top: 15px;">Klaar voor analyse...</p>
        </div>
    </div>
</div>
<script>
    const FIN_KEY = "d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0";
    const GEM_KEY = "AIzaSyDTDyQWKgCJ3tvcexRCYYvuRUfkTpN4J5w";
    let watchlist = JSON.parse(localStorage.getItem('sst_architect_wl')) || ['NVDA', 'AAPL'];

    function renderWatchlist() {
        const bar = document.getElementById('watchlistBar');
        bar.innerHTML = watchlist.map(t => `<div style="background:#21262d; border:1px solid #30363d; padding:8px 12px; border-radius:8px; display:flex; gap:10px; color:white; font-weight:700;">
            <span onclick="document.getElementById('tickerInput6').value='${t}'; runUltimateAnalysis()">${t}</span>
            <span onclick="removeFromWatchlist('${t}')" style="color:#f85149; cursor:pointer;">&times;</span>
        </div>`).join('');
    }

    function addToWatchlist() {
        const t = document.getElementById('tickerInput6').value.toUpperCase();
        if(t && !watchlist.includes(t)) { watchlist.push(t); localStorage.setItem('sst_architect_wl', JSON.stringify(watchlist)); renderWatchlist(); }
    }

    function removeFromWatchlist(t) {
        watchlist = watchlist.filter(item => item !== t); localStorage.setItem('sst_architect_wl', JSON.stringify(watchlist)); renderWatchlist();
    }

    async function runUltimateAnalysis() {
        const ticker = document.getElementById('tickerInput6').value.toUpperCase();
        if(!ticker) return;
        try {
            const qR = await fetch(`https://finnhub.io/api/v1/quote?symbol=${ticker}&token=${FIN_KEY}`);
            const q = await qR.json();
            const score = Math.min(Math.max(Math.round(50 + (q.dp * 8)), 10), 98);
            
            document.getElementById('totalScore').innerText = score;
            document.getElementById('resSymbol').innerText = ticker;
            document.getElementById('targetPrice').innerText = "$" + (q.c * 1.07).toFixed(2);
            document.getElementById('supportPrice').innerText = "$" + (q.c * 0.96).toFixed(2);

            const rBar = document.getElementById('riskBar');
            rBar.style.width = (100-score) + "%";
            rBar.style.background = (100-score) > 60 ? "#f85149" : "#238636";
            document.getElementById('riskLabel').innerText = "RISK: " + ((100-score) > 60 ? "HIGH" : "LOW");

            const tBar = document.getElementById('timingBar');
            tBar.style.width = score + "%";
            tBar.style.background = score > 65 ? "#238636" : "#d29922";
            document.getElementById('timingLabel').innerText = "TIMING: " + (score > 65 ? "OPTIMAL" : "WAIT");

            const gemRes = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${GEM_KEY}`, {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ contents: [{ parts: [{ text: `Geef kort trading advies voor ${ticker} in het Nederlands.` }] }] })
            });
            const gemData = await gemRes.json();
            document.getElementById('verdictDetail').innerText = gemData.candidates[0].content.parts[0].text;
        } catch(e) { console.error(e); }
    }
    renderWatchlist();
</script>
"""

# --- TABS RENDEREN ---
tabs = st.tabs(["🚀 SMART TERMINAL", "🛡️ RISK & TIER", "📊 PRO SCANNER", "🔍 SIGNAL ANALYZER", "📈 TECHANALYSIS PRO", "🏛️ SST ARCHITECT"])

with tabs[0]: components.html(tool1_html, height=850)
with tabs[1]: components.html(tool2_html, height=800)
with tabs[2]: components.html(tool3_html, height=800)
with tabs[3]: components.html(tool4_html, height=800)
with tabs[4]: components.html(tool5_html, height=1000)
with tabs[5]: components.html(tool6_html, height=1000, scrolling=True)




























