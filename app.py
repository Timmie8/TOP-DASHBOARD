import streamlit as st
import streamlit.components.v1 as components

# Pagina instellingen
st.set_page_config(page_title="SST AI TRADING SUITE", layout="wide")

# Globale Styling voor de tabs
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .block-container { padding: 0px; background-color: #050608; }
    .stTabs [data-baseweb="tab-list"] { background-color: #0d1117; padding: 10px; border-bottom: 1px solid #30363d; gap: 15px; }
    .stTabs [data-baseweb="tab"] { color: #8b949e; font-weight: bold; font-size: 14px; }
    .stTabs [aria-selected="true"] { color: #2f81f7 !important; border-bottom-color: #2f81f7 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DE OUDE TOOLS (Ik voeg hier alleen tool 6 volledig uit, de rest blijft zoals je had) ---
# Tip: Plak hier je eerdere HTML blokken van tool 1 t/m 5 weer in als je die lokaal hebt.

tool1_html = ""
tool2_html = ""
tool3_html = ""
tool4_html = ""
tool5_html = ""

# --- TOOL 6: SST ARCHITECT (VOLLEDIG GEFIXTE LOGICA) ---
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
            <p style="font-size: 0.75rem; color: #8b949e; margin:0;">SWING TARGET</p>
            <div id="targetPrice" style="font-size: 1.8rem; font-weight: 900; color: #3fb950;">$0.00</div>
            <p style="font-size: 0.75rem; color: #8b949e; margin: 15px 0 0 0;">STOP LOSS</p>
            <div id="supportPrice" style="font-size: 1.4rem; font-weight: 900; color: #f85149;">$0.00</div>
        </div>

        <div style="background: #161b22; padding: 30px; border-radius: 18px; border: 1px solid #30363d;">
            <h3 id="resSymbol" style="margin: 0; font-size: 2rem; font-weight: 900; color: #fff;">---</h3>
            <div id="resPrice" style="font-size: 1.5rem; font-weight: 700; color: #2f81f7;">$0.00</div>
            <p id="verdictDetail" style="font-size: 0.85rem; color: #c9d1d9; line-height: 1.5; margin-top: 15px; border-top: 1px solid #30363d; padding-top: 10px;">Voer ticker in...</p>
        </div>
    </div>

    <div id="scannerLoader" style="display: none; text-align: center; padding: 40px;">
        <div style="width: 30px; height: 30px; border: 3px solid #2f81f7; border-top: 3px solid transparent; border-radius: 50%; display: inline-block; animation: spin 1s linear infinite;"></div>
    </div>

    <style>
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .watchlist-pill { background: #21262d; border: 1px solid #30363d; padding: 8px 12px; border-radius: 8px; cursor: pointer; display: flex; gap: 8px; font-weight: 700; color: #fff; }
        .watchlist-pill:hover { border-color: #2f81f7; }
    </style>
</div>

<script>
    const FIN_KEY = "d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0";
    const GEM_KEY = "AIzaSyDTDyQWKgCJ3tvcexRCYYvuRUfkTpN4J5w";
    let watchlist = JSON.parse(localStorage.getItem('sst_architect_wl')) || ['NVDA', 'TSLA'];

    function renderWatchlist() {
        const bar = document.getElementById('watchlistBar');
        bar.innerHTML = '';
        watchlist.forEach(t => {
            const el = document.createElement('div');
            el.className = 'watchlist-pill';
            el.innerHTML = `<span onclick="document.getElementById('tickerInput6').value='${t}'; runUltimateAnalysis()">${t}</span>
                            <span onclick="removeFromWatchlist('${t}')" style="color:#f85149; margin-left:5px;">&times;</span>`;
            bar.appendChild(el);
        });
    }

    function addToWatchlist() {
        const t = document.getElementById('tickerInput6').value.toUpperCase();
        if(t && !watchlist.includes(t)) {
            watchlist.push(t);
            localStorage.setItem('sst_architect_wl', JSON.stringify(watchlist));
            renderWatchlist();
        }
    }

    function removeFromWatchlist(t) {
        watchlist = watchlist.filter(item => item !== t);
        localStorage.setItem('sst_architect_wl', JSON.stringify(watchlist));
        renderWatchlist();
    }

    async function runUltimateAnalysis() {
        const ticker = document.getElementById('tickerInput6').value.toUpperCase();
        if(!ticker) return;

        document.getElementById('scannerLoader').style.display = 'block';
        document.getElementById('verdictDetail').innerText = "Analyseert data...";

        try {
            const qR = await fetch(`https://finnhub.io/api/v1/quote?symbol=${ticker}&token=${FIN_KEY}`);
            const q = await qR.json();

            // Simpele maar effectieve scoring logica
            const score = Math.min(Math.max(Math.round(50 + (q.dp * 8)), 10), 98);
            const riskVal = 100 - score;
            const timingVal = score > 60 ? 85 : 40;

            // UI UPDATES
            document.getElementById('totalScore').innerText = score;
            document.getElementById('resSymbol').innerText = ticker;
            document.getElementById('resPrice').innerText = "$" + q.c.toFixed(2);
            document.getElementById('targetPrice').innerText = "$" + (q.c * 1.07).toFixed(2);
            document.getElementById('supportPrice').innerText = "$" + (q.c * 0.96).toFixed(2);

            // RISK BAR KLEUR & LENGTE
            const rBar = document.getElementById('riskBar');
            rBar.style.width = riskVal + "%";
            rBar.style.background = riskVal > 60 ? "#f85149" : (riskVal > 30 ? "#d29922" : "#238636");
            document.getElementById('riskLabel').innerText = "RISK: " + (riskVal > 60 ? "HIGH" : "LOW");

            // TIMING BAR KLEUR & LENGTE
            const tBar = document.getElementById('timingBar');
            tBar.style.width = timingVal + "%";
            tBar.style.background = timingVal > 70 ? "#238636" : "#d29922";
            document.getElementById('timingLabel').innerText = "TIMING: " + (timingVal > 70 ? "OPTIMAL" : "WAIT");

            // AI VERDICT (Gemini aanroep)
            const prompt = `Analyze ticker ${ticker}. Current price ${q.c}, daily change ${q.dp}%. Score is ${score}/100. Provide a 2-sentence swing trade advice in Dutch.`;
            const gemResponse = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${GEM_KEY}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] })
            });
            const gemData = await gemResponse.json();
            document.getElementById('verdictDetail').innerText = gemData.candidates[0].content.parts[0].text;

        } catch (e) {
            document.getElementById('verdictDetail').innerText = "Fout bij ophalen data. Check ticker.";
        }
        document.getElementById('scannerLoader').style.display = 'none';
    }

    renderWatchlist();
</script>
"""

# --- TABS RENDEREN ---
tabs = st.tabs(["🚀 SMART TERMINAL", "🛡️ RISK & TIER", "📊 PRO SCANNER", "🔍 SIGNAL ANALYZER", "📈 TECHANALYSIS PRO", "🏛️ SST ARCHITECT"])

# Vul de tabs (zorg dat je de variabelen tool1_html etc. gevuld hebt)
with tabs[0]: components.html(tool1_html, height=850)
with tabs[1]: components.html(tool2_html, height=800)
with tabs[2]: components.html(tool3_html, height=800)
with tabs[3]: components.html(tool4_html, height=800)
with tabs[4]: components.html(tool5_html, height=1000)
with tabs[5]: components.html(tool6_html, height=1000, scrolling=True)



























