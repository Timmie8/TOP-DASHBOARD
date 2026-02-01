import streamlit as st
import streamlit.components.v1 as components

# 1. Pagina instellingen
st.set_page_config(page_title="SST AI TRADING SUITE v6.3", layout="wide")

# Globale Styling voor de interface
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .block-container { padding: 0px; background-color: #050608; }
    .stTabs [data-baseweb="tab-list"] { background-color: #0d1117; padding: 10px; border-bottom: 1px solid #30363d; gap: 15px; }
    .stTabs [data-baseweb="tab"] { color: #8b949e; font-weight: bold; font-size: 14px; }
    .stTabs [aria-selected="true"] { color: #2f81f7 !important; border-bottom-color: #2f81f7 !important; }
    iframe { border: none !important; }
    </style>
    """, unsafe_allow_html=True)

# --- TOOL 1: SMART TERMINAL ---
tool1_html = """
<div style="background-color: #050608; color: white; font-family: sans-serif; padding: 20px; min-height: 850px;">
    <div style="max-width: 900px; margin: auto;">
        <div style="display: flex; gap: 10px; margin-bottom: 20px;">
            <input id="t1Input" type="text" value="NVDA" style="background: #11141b; border: 2px solid #1f2937; padding: 15px; border-radius: 1rem; color: white; width: 70%; outline: none;">
            <button onclick="fetchT1()" style="background: #2563eb; padding: 15px 30px; border-radius: 1rem; font-weight: 900; color: white; border:none; cursor:pointer; flex:1;">SCAN TICKER</button>
        </div>
        <div id="t1Signal" style="background: #1e3a8a; padding: 20px; border-radius: 1.5rem; text-align: center; margin-bottom: 15px;">
            <div id="t1Advice" style="font-size: 2rem; font-weight: 900;">INITIALIZING...</div>
        </div>
        <div id="t1Chart" style="height: 500px; border-radius: 1.5rem; overflow: hidden; border: 1px solid #1f2937;"></div>
    </div>
</div>
<script src="https://s3.tradingview.com/tv.js"></script>
<script>
    async function fetchT1() {
        const t = document.getElementById('t1Input').value.toUpperCase();
        const r = await fetch('https://finnhub.io/api/v1/quote?symbol='+t+'&token=d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0');
        const d = await r.json();
        document.getElementById('t1Advice').innerText = d.dp > 0 ? "BULLISH SIGNAL" : "WATCH / NEUTRAL";
        document.getElementById('t1Signal').style.background = d.dp > 0 ? "#065f46" : "#1e3a8a";
        new TradingView.widget({"autosize": true, "symbol": t, "interval": "D", "theme": "dark", "container_id": "t1Chart", "style": "1"});
    }
    window.onload = fetchT1;
</script>
"""

# --- TOOL 2: RISK & TIER ---
tool2_html = """
<div style="background:#0d1117; color:#c9d1d9; font-family:sans-serif; padding:30px; min-height:800px;">
    <div style="max-width:800px; margin:auto;">
        <h2 style="color:white;">🛡️ Risk & Tier System</h2>
        <div style="display:flex; gap:10px; margin:20px 0;">
            <input id="t2Input" type="text" placeholder="TICKER" style="background:#161b22; border:1px solid #30363d; color:white; padding:12px; border-radius:8px; flex:1;">
            <button onclick="calcRisk()" style="background:#1f6feb; color:white; border:none; padding:12px 25px; border-radius:8px; cursor:pointer; font-weight:bold;">ANALYSE RISK</button>
        </div>
        <div id="t2Out"></div>
    </div>
</div>
<script>
async function calcRisk() {
    const t = document.getElementById('t2Input').value.toUpperCase();
    const r = await fetch('https://finnhub.io/api/v1/quote?symbol='+t+'&token=d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0');
    const d = await r.json();
    document.getElementById('t2Out').innerHTML = `
        <div style="background:#161b22; border:1px solid #30363d; padding:25px; border-radius:15px; border-left:10px solid #2f81f7;">
            <h1 style="color:white; margin:0;">${t}</h1>
            <p>Entry: <b>$${d.c}</b></p>
            <p style="color:#f85149;">Stop Loss (4%): $${(d.c*0.96).toFixed(2)}</p>
            <p style="color:#39d353;">Target (8%): $${(d.c*1.08).toFixed(2)}</p>
        </div>`;
}
</script>
"""

# --- TOOL 3: PRO SCANNER v5.7 ---
tool3_html = """
<div style="background: #0d1117; color: white; font-family: sans-serif; padding: 20px;">
    <div style="max-width: 1000px; margin: auto;">
        <h3>Batch AI Scanner</h3>
        <textarea id="t3List" style="width: 100%; height: 80px; background: #010409; color: #3fb950; border: 1px solid #30363d; padding: 10px; font-family: monospace;">AAPL, NVDA, TSLA, AMD, MSFT, META</textarea>
        <button onclick="scanT3()" style="width: 100%; padding: 15px; background: #238636; color: white; border:none; margin-top:10px; cursor:pointer; font-weight:bold;">START MULTI-SCAN</button>
        <table style="width:100%; margin-top:20px; border-collapse: collapse;">
            <thead><tr style="border-bottom: 2px solid #30363d; color: #8b949e; text-align: left;"><th>SYMBOL</th><th>CHANGE</th><th>AI SCORE</th></tr></thead>
            <tbody id="t3Body"></tbody>
        </table>
    </div>
</div>
<script>
async function scanT3() {
    const tickers = document.getElementById('t3List').value.split(/[,\\s\\n]+/).filter(x => x);
    const body = document.getElementById('t3Body'); body.innerHTML = '';
    for(let t of tickers) {
        const r = await fetch('https://finnhub.io/api/v1/quote?symbol='+t.trim().toUpperCase()+'&token=d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0');
        const d = await r.json();
        if(d.c) {
            const score = Math.round(50 + (d.dp * 5));
            body.innerHTML += `<tr style="border-bottom: 1px solid #21262d;"><td style="padding:12px;">${t.toUpperCase()}</td><td style="color:${d.dp>0?'#3fb950':'#f85149'}">${d.dp.toFixed(2)}%</td><td>${score}/100</td></tr>`;
        }
    }
}
</script>
"""

# --- TOOL 4: SIGNAL ANALYZER ---
tool4_html = """
<div style="background:#050505; color:white; font-family:Arial; padding:20px;">
    <div style="max-width:900px; margin:auto;">
        <input id="t4Sym" value="TSLA" style="background:#1c1c1c; border:1px solid #333; color:white; padding:10px; border-radius:5px;">
        <button onclick="loadT4()" style="background:#2ecc71; padding:10px 20px; border:none; border-radius:5px; cursor:pointer; font-weight:bold;">GET INDICATORS</button>
        <div id="t4Res" style="margin-top:20px;"></div>
    </div>
</div>
<script>
async function loadT4() {
    const s = document.getElementById('t4Sym').value.toUpperCase();
    const r = await fetch(`https://api.allorigins.win/get?url=${encodeURIComponent('https://query1.finance.yahoo.com/v8/finance/chart/'+s+'?interval=1d&range=1mo')}`);
    const j = await r.json(); const data = JSON.parse(j.contents);
    const close = data.chart.result[0].indicators.quote[0].close.filter(x => x);
    const last = close.at(-1);
    const sma = close.slice(-20).reduce((a,b)=>a+b)/20;
    document.getElementById('t4Res').innerHTML = `
        <div style="background:#111; padding:20px; border-radius:10px; border:1px solid #222;">
            <h2 style="margin:0;">${s} Analysis</h2>
            <hr style="border:0; border-top:1px solid #333; margin:15px 0;">
            <p>SMA(20): ${sma.toFixed(2)} | Status: <b style="color:${last>sma?'#3fb950':'#f85149'}">${last>sma?'BULLISH':'BEARISH'}</b></p>
        </div>`;
}
</script>
"""

# --- TOOL 5: TECHANALYSIS PRO (VOLLEDIG HERSTELD) ---
tool5_html = """
<div style="background: #050608; color: white; padding: 25px; font-family: sans-serif; min-height: 800px;">
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #30363d; padding-bottom: 20px; margin-bottom: 25px;">
        <div>
            <h2 style="margin: 0; color: #fff;">TechAnalysis <span style="color: #2f81f7;">PRO</span></h2>
            <p style="margin: 5px 0 0; color: #8b949e; font-size: 0.8rem;">Live Portfolio Monitoring</p>
        </div>
        <div style="display: flex; gap: 10px;">
            <input id="t5Input" type="text" placeholder="TICKER" style="background: #0d1117; border: 1px solid #30363d; color: white; padding: 10px; border-radius: 8px; width: 120px; outline: none;">
            <button onclick="addTicker5()" style="background: #2f81f7; color: white; border: none; padding: 10px 20px; border-radius: 8px; font-weight: bold; cursor: pointer;">+ ANALYSE</button>
        </div>
    </div>
    <div id="t5Grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px;"></div>
    <div id="t5Empty" style="text-align: center; padding: 100px; color: #8b949e; border: 2px dashed #30363d; border-radius: 20px; margin-top: 20px;">Voeg een ticker toe om te beginnen.</div>
</div>
<script>
    async function addTicker5() {
        const t = document.getElementById('t5Input').value.toUpperCase();
        if(!t) return;
        document.getElementById('t5Empty').style.display = 'none';
        const r = await fetch('https://finnhub.io/api/v1/quote?symbol='+t+'&token=d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0');
        const d = await r.json();
        const card = document.createElement('div');
        card.style = "background:#161b22; border:1px solid #30363d; padding:20px; border-radius:15px; position:relative;";
        card.innerHTML = `
            <div style="display:flex; justify-content:space-between;">
                <b>${t}</b> <span style="color:${d.dp>0?'#3fb950':'#f85149'}">${d.dp.toFixed(2)}%</span>
            </div>
            <div style="font-size:1.5rem; margin:10px 0;">$${d.c.toFixed(2)}</div>
            <div style="font-size:0.7rem; color:#8b949e;">H: ${d.h} | L: ${d.l}</div>
            <button onclick="this.parentElement.remove()" style="position:absolute; top:5px; right:5px; background:none; border:none; color:#f85149; cursor:pointer;">&times;</button>
        `;
        document.getElementById('t5Grid').prepend(card);
        document.getElementById('t5Input').value = '';
    }
</script>
"""

# --- TOOL 6: SST ARCHITECT ---
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
                <div id="riskBar6" style="height: 100%; width: 0%; transition: 1s; background: #30363d;"></div>
                <div id="riskLabel6" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-weight: 900; font-size: 0.7rem; color: #fff;">RISK: --</div>
            </div>
            <div style="margin-top: 10px; background: #0d1117; height: 30px; border-radius: 8px; border: 1px solid #30363d; overflow: hidden; position: relative;">
                <div id="timingBar6" style="height: 100%; width: 0%; transition: 1s; background: #30363d;"></div>
                <div id="timingLabel6" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-weight: 900; font-size: 0.7rem; color: #fff;">TIMING: --</div>
            </div>
        </div>
        <div style="background: #1c2128; padding: 30px; border-radius: 18px; border: 1px solid #444;">
            <h3 style="margin: 0 0 20px 0; font-size: 1rem; color: #fff;">AI SETUP</h3>
            <div id="targetPrice6" style="font-size: 1.8rem; font-weight: 900; color: #3fb950;">$0.00</div>
            <div id="supportPrice6" style="font-size: 1.4rem; font-weight: 900; color: #f85149;">$0.00</div>
        </div>
        <div style="background: #161b22; padding: 30px; border-radius: 18px; border: 1px solid #30363d;">
            <h3 id="resSymbol6" style="margin: 0; font-size: 2rem; font-weight: 900; color: #fff;">---</h3>
            <p id="verdictDetail6" style="font-size: 0.85rem; color: #c9d1d9; line-height: 1.5; margin-top: 15px; border-top: 1px solid #30363d; padding-top: 10px;">Voer ticker in...</p>
        </div>
    </div>
</div>
<script>
    const FIN_KEY = "d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0";
    const GEM_KEY = "AIzaSyDTDyQWKgCJ3tvcexRCYYvuRUfkTpN4J5w";
    let watchlist6 = JSON.parse(localStorage.getItem('sst_arch_wl')) || ['NVDA', 'AAPL'];

    function renderWatchlist6() {
        const bar = document.getElementById('watchlistBar'); bar.innerHTML = '';
        watchlist6.forEach(t => {
            const el = document.createElement('div');
            el.style = "background:#21262d; border:1px solid #30363d; padding:8px 12px; border-radius:8px; color:white; font-weight:700; display:flex; gap:10px; cursor:pointer;";
            el.innerHTML = `<span onclick="document.getElementById('tickerInput6').value='${t}'; runUltimateAnalysis()">${t}</span><span onclick="removeFromWatchlist6('${t}')" style="color:#f85149;">&times;</span>`;
            bar.appendChild(el);
        });
    }

    function addToWatchlist() {
        const t = document.getElementById('tickerInput6').value.toUpperCase();
        if(t && !watchlist6.includes(t)) { watchlist6.push(t); localStorage.setItem('sst_arch_wl', JSON.stringify(watchlist6)); renderWatchlist6(); }
    }

    function removeFromWatchlist6(t) {
        watchlist6 = watchlist6.filter(item => item !== t); localStorage.setItem('sst_arch_wl', JSON.stringify(watchlist6)); renderWatchlist6();
    }

    async function runUltimateAnalysis() {
        const ticker = document.getElementById('tickerInput6').value.toUpperCase();
        if(!ticker) return;
        try {
            const qR = await fetch(`https://finnhub.io/api/v1/quote?symbol=${ticker}&token=${FIN_KEY}`);
            const q = await qR.json();
            const score = Math.min(Math.max(Math.round(50 + (q.dp * 8)), 10), 98);
            
            document.getElementById('totalScore').innerText = score;
            document.getElementById('resSymbol6').innerText = ticker;
            document.getElementById('targetPrice6').innerText = "Target: $" + (q.c * 1.07).toFixed(2);
            document.getElementById('supportPrice6').innerText = "Stop: $" + (q.c * 0.96).toFixed(2);

            const riskVal = (100 - score);
            document.getElementById('riskBar6').style.width = riskVal + "%";
            document.getElementById('riskBar6').style.background = riskVal > 60 ? "#f85149" : "#238636";
            document.getElementById('riskLabel6').innerText = "RISK: " + (riskVal > 60 ? "HIGH" : "LOW");

            document.getElementById('timingBar6').style.width = score + "%";
            document.getElementById('timingBar6').style.background = score > 65 ? "#238636" : "#d29922";
            document.getElementById('timingLabel6').innerText = "TIMING: " + (score > 65 ? "OPTIMAL" : "WAIT");

            const gemRes = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${GEM_KEY}`, {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ contents: [{ parts: [{ text: `Geef zeer kort trading advies voor ${ticker} in het Nederlands.` }] }] })
            });
            const gemData = await gemRes.json();
            document.getElementById('verdictDetail6').innerText = gemData.candidates[0].content.parts[0].text;
        } catch(e) {}
    }
    renderWatchlist6();
</script>
"""

# --- TABS RENDERING ---
tabs = st.tabs([
    "🚀 SMART TERMINAL", 
    "🛡️ RISK & TIER", 
    "📊 PRO SCANNER", 
    "🔍 SIGNAL ANALYZER", 
    "📈 TECHANALYSIS PRO", 
    "🏛️ SST ARCHITECT"
])

with tabs[0]: components.html(tool1_html, height=850, scrolling=True)
with tabs[1]: components.html(tool2_html, height=800, scrolling=True)
with tabs[2]: components.html(tool3_html, height=900, scrolling=True)
with tabs[3]: components.html(tool4_html, height=900, scrolling=True)
with tabs[4]: components.html(tool5_html, height=1000, scrolling=True)
with tabs[5]: components.html(tool6_html, height=1000, scrolling=True)






























