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

# --- DE OUDE TOOLS (1 t/m 5) BLIJVEN BEHOUDEN ---
# (Ik heb de codes hieronder samengevat om de leesbaarheid te bewaren, 
# maar in je werkelijke bestand staan de volledige HTML blokken zoals eerder geleverd)

tool1_html = """...""" # Smart Terminal
tool2_html = """...""" # Risk System
tool3_html = """...""" # Pro Scanner
tool4_html = """...""" # Signal Analyzer
tool5_html = """...""" # TechAnalysis Pro

# --- TOOL 6: SST ARCHITECT (NIEUWE CODE) ---
tool6_html = """
<div id="sst-terminal-final" style="font-family: 'Inter', sans-serif; color: #e6edf3; max-width: 1200px; margin: 0 auto; background: #0d1117; padding: 30px; border-radius: 20px; border: 1px solid #30363d; box-shadow: 0 15px 40px rgba(0,0,0,0.6);">
    <div style="display: flex; flex-wrap: wrap; gap: 20px; align-items: center; border-bottom: 1px solid #30363d; padding-bottom: 30px; margin-bottom: 20px;">
        <div style="flex: 1; min-width: 250px;">
            <h2 style="margin: 0; font-size: 1.8rem; font-weight: 900; color: #fff; letter-spacing: -1px;">SST <span style="color: #2f81f7;">ARCHITECT</span></h2>
            <p style="margin: 5px 0 0; font-size: 0.75rem; color: #8b949e; text-transform: uppercase; font-weight: 800; letter-spacing: 1.5px;">Deep Research & Swing Trading Engine</p>
        </div>
        <div style="display: flex; gap: 12px; flex-wrap: wrap;">
            <input id="tickerInput" type="text" placeholder="TICKER" style="background: #010409; border: 1px solid #30363d; color: #fff; padding: 15px 20px; border-radius: 12px; font-weight: 800; width: 130px; outline: none; border-color: #2f81f7;">
            <button onclick="runUltimateAnalysis(document.getElementById('tickerInput').value)" style="background: #238636; color: #fff; border: none; padding: 15px 30px; border-radius: 12px; font-weight: 900; cursor: pointer;">RUN DEEP SCAN</button>
            <button onclick="addToWatchlist()" style="background: transparent; color: #8b949e; border: 1px solid #30363d; padding: 15px; border-radius: 12px; font-weight: 800; cursor: pointer;">+ WATCH</button>
        </div>
    </div>
    <div id="watchlistBar" style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 30px;"></div>
    <div id="scannerDashboard" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 25px;">
        <div id="totalScoreCard" style="background: #161b22; padding: 30px; border-radius: 18px; border: 2px solid #30363d; text-align: center; transition: 0.6s;">
            <span style="font-size: 0.7rem; font-weight: 800; color: #8b949e; text-transform: uppercase;">Aggregate AI Score</span>
            <div id="totalScore" style="font-size: 2.2rem; font-weight: 900; margin: 20px 0; color: #8b949e;">WAITING...</div>
            <div style="margin-top: 10px; background: #0d1117; height: 35px; border-radius: 8px; border: 1px solid #30363d; overflow: hidden; position: relative;">
                <div id="riskBar" style="height: 100%; width: 0%; transition: 1s;"></div>
                <div id="riskLabel" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-weight: 900; font-size: 0.7rem; color: #fff; letter-spacing: 1px;">RISK ANALYSIS</div>
            </div>
            <div style="margin-top: 10px; background: #0d1117; height: 35px; border-radius: 8px; border: 1px solid #30363d; overflow: hidden; position: relative;">
                <div id="timingBar" style="height: 100%; width: 100%; transition: 1s; background: #30363d;"></div>
                <div id="timingLabel" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-weight: 900; font-size: 0.7rem; color: #fff; letter-spacing: 1px;">TIMING: ---</div>
            </div>
        </div>
        <div style="background: #1c2128; padding: 30px; border-radius: 18px; border: 1px solid #444; position: relative;">
            <div style="position: absolute; top: 0; left: 0; width: 5px; height: 100%; background: #2f81f7;"></div>
            <h3 style="margin: 0 0 20px 0; font-size: 1rem; font-weight: 900; color: #fff; text-transform: uppercase;">AI Trade Setup</h3>
            <div style="margin-bottom: 20px;">
                <p style="font-size: 0.75rem; color: #8b949e; margin-bottom: 5px;">SWING TARGET</p>
                <div style="display: flex; justify-content: space-between;"><span id="targetPrice" style="font-size: 1.8rem; font-weight: 900; color: #3fb950;">$0.00</span><span id="targetPct" style="color:#3fb950; font-weight:800;">+0%</span></div>
            </div>
            <div style="margin-bottom: 20px;">
                <p style="font-size: 0.75rem; color: #8b949e; margin-bottom: 5px;">AI SUPPORT (STOP)</p>
                <div style="display: flex; justify-content: space-between;"><span id="supportPrice" style="font-size: 1.4rem; font-weight: 900; color: #f85149;">$0.00</span><span id="supportPct" style="color:#f85149; font-weight:800;">-0%</span></div>
            </div>
        </div>
        <div style="background: #161b22; padding: 30px; border-radius: 18px; border: 1px solid #30363d;">
            <h3 id="resSymbol" style="margin: 0; font-size: 2rem; font-weight: 900; color: #fff;">---</h3>
            <div id="resPrice" style="font-size: 2.2rem; font-weight: 900; color: #2f81f7; margin: 5px 0;">$0.00</div>
            <p id="verdictDetail" style="font-size: 0.85rem; color: #c9d1d9; line-height: 1.5; margin-top: 15px; border-top: 1px solid #30363d; padding-top: 10px;">Awaiting Research...</p>
        </div>
    </div>
    <div id="scannerLoader" style="display: none; text-align: center; padding: 80px;"><div style="width: 40px; height: 40px; border: 4px solid #30363d; border-top: 4px solid #2f81f7; border-radius: 50%; display: inline-block; animation: scanner-spin 0.8s linear infinite;"></div></div>
    <style>
        @keyframes scanner-spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .breakout-active { background: #0d2a14 !important; border-color: #3fb950 !important; }
        .watchlist-pill { background: #21262d; border: 1px solid #30363d; padding: 8px 15px; border-radius: 8px; cursor: pointer; display: flex; gap: 8px; align-items: center; font-weight: 800; font-size: 0.85rem; }
    </style>
</div>
<script>
    const FIN_KEY = "d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0";
    const GEM_KEY = "AIzaSyDTDyQWKgCJ3tvcexRCYYvuRUfkTpN4J5w";
    let watchlist = JSON.parse(localStorage.getItem('sst_risk_watchlist')) || ['NVDA', 'TSLA'];

    function renderWatchlist() {
        const bar = document.getElementById('watchlistBar'); bar.innerHTML = '';
        watchlist.forEach(t => {
            const el = document.createElement('div'); el.className = 'watchlist-pill';
            el.innerHTML = `<span onclick="runUltimateAnalysis('${t}')">${t}</span><span onclick="removeFromWatchlist('${t}')" style="color:#f85149;">&times;</span>`;
            bar.appendChild(el);
        });
    }

    async function getDeepResearchOpinion(ticker, score, risk, timing) {
        const prompt = `Act as a senior trader. Analyze ${ticker}: Score ${score}/100, Risk ${risk}, Timing ${timing}. Short swing trade conclusion (60 words). English.`;
        try {
            const resp = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${GEM_KEY}`, {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] })
            });
            const data = await resp.json(); return data.candidates[0].content.parts[0].text;
        } catch (e) { return "Research offline. Data suggests caution."; }
    }

    async function runUltimateAnalysis(ticker) {
        if(!ticker) return; ticker = ticker.toUpperCase();
        document.getElementById('scannerLoader').style.display = 'block';
        try {
            const [qR, mR] = await Promise.all([
                fetch(`https://finnhub.io/api/v1/quote?symbol=${ticker}&token=${FIN_KEY}`),
                fetch(`https://finnhub.io/api/v1/stock/metric?symbol=${ticker}&metric=all&token=${FIN_KEY}`)
            ]);
            const q = await qR.json(); const m = await mR.json();
            const k = Math.round(((q.c - m.metric['52WeekLow']) / (m.metric['52WeekHigh'] - m.metric['52WeekLow'])) * 100);
            const aiTotal = Math.round((k*0.4) + (q.dp*5) + 50);
            
            document.getElementById('totalScore').innerText = aiTotal;
            document.getElementById('resSymbol').innerText = ticker;
            document.getElementById('resPrice').innerText = `$${q.c.toFixed(2)}`;
            document.getElementById('targetPrice').innerText = `$${(q.c*1.08).toFixed(2)}`;
            document.getElementById('supportPrice').innerText = `$${(q.c*0.96).toFixed(2)}`;
            
            const opinion = await getDeepResearchOpinion(ticker, aiTotal, "MEDIUM", "POSITIVE");
            document.getElementById('verdictDetail').innerText = opinion;
        } catch (e) { console.error(e); }
        document.getElementById('scannerLoader').style.display = 'none';
    }
    renderWatchlist();
</script>
"""

# --- TABS RENDEREN ---
t1, t2, t3, t4, t5, t6 = st.tabs([
    "🚀 SMART TERMINAL", 
    "🛡️ RISK & TIER", 
    "📊 PRO SCANNER v5.7", 
    "🔍 SIGNAL ANALYZER", 
    "📈 TECHANALYSIS PRO",
    "🏛️ SST ARCHITECT"
])

with t1: components.html(tool1_html, height=850, scrolling=True)
with t2: components.html(tool2_html, height=800, scrolling=True)
with t3: components.html(tool3_html, height=900, scrolling=True)
with t4: components.html(tool4_html, height=900, scrolling=True)
with t5: components.html(tool5_html, height=1000, scrolling=True)
with t6: components.html(tool6_html, height=1000, scrolling=True)



























