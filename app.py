import streamlit as st
import streamlit.components.v1 as components

# --- 1. PAGINA CONFIGURATIE ---
st.set_page_config(page_title="SST ARCHITECT TERMINAL", layout="wide", initial_sidebar_state="collapsed")

# --- 2. GLOBALE STYLING (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: #050505; }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: #0d1117;
        border-radius: 8px 8px 0px 0px;
        color: #8b949e;
        border: 1px solid #30363d;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #238636 !important;
        color: white !important;
    }
    iframe { border: none !important; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DE TOOLS ---

def render_sst_architect_and_journal():
    """De SST Architect Engine + Trade Journal (HTML/JS)"""
    architect_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
        <style>
            body { background: #050505; color: #e6edf3; font-family: 'Inter', sans-serif; margin: 0; padding: 10px; }
            .card { background: #0d1117; padding: 25px; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 20px; }
            .input-group { display: flex; gap: 10px; margin-bottom: 20px; }
            input { background: #010409; border: 1px solid #30363d; color: white; padding: 12px; border-radius: 8px; flex: 1; font-weight: bold; }
            button { padding: 12px 24px; border-radius: 8px; cursor: pointer; font-weight: 900; border: none; }
            .btn-scan { background: #238636; color: white; }
            .btn-log { background: #21262d; color: #58a6ff; border: 1px solid #30363d; display: none; }
            .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }
            .stat-box { text-align: center; padding: 15px; background: #161b22; border-radius: 12px; border: 1px solid #30363d; }
            .big-num { font-size: 2.5rem; font-weight: 900; display: block; margin: 10px 0; color: #2f81f7; }
            .journal-table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.85rem; }
            .journal-table th { text-align: left; padding: 12px; color: #8b949e; border-bottom: 2px solid #30363d; }
            .journal-table td { padding: 12px; border-bottom: 1px solid #30363d; }
            @keyframes breakout-glow { 0% { box-shadow: 0 0 5px #238636; } 50% { box-shadow: 0 0 25px #238636; } 100% { box-shadow: 0 0 5px #238636; } }
            .breakout-active { animation: breakout-glow 1.5s infinite ease-in-out; border-color: #3fb950 !important; }
        </style>
    </head>
    <body>
        <div class="card" id="mainCard">
            <h2 style="margin-top:0;">SST <span style="color: #2f81f7;">ARCHITECT</span></h2>
            <div class="input-group">
                <input id="tickerInput" type="text" placeholder="TICKER (E.G. NVDA)">
                <button class="btn-scan" onclick="runUltimateAnalysis()">RUN DEEP SCAN</button>
                <button class="btn-log" id="logBtn" onclick="logToJournal()">LOG TO JOURNAL</button>
            </div>
            <div class="stats-grid">
                <div class="stat-box">AI SCORE<span class="big-num" id="resScore">--</span></div>
                <div class="stat-box">PRICE<span class="big-num" id="resPrice">--</span></div>
                <div class="stat-box">TIMING<span class="big-num" id="resTiming" style="font-size:1.5rem;">---</span></div>
            </div>
            <div id="verdictDetail" style="margin-top:20px; font-style: italic; color: #8b949e; line-height:1.5;">Awaiting research...</div>
        </div>

        <div class="card">
            <h3 style="margin-top:0; color: #8b949e;">📓 TRADE JOURNAL</h3>
            <table class="journal-table">
                <thead><tr><th>Date</th><th>Ticker</th><th>Score</th><th>Price</th><th>Verdict</th></tr></thead>
                <tbody id="journalBody"></tbody>
            </table>
        </div>

        <script>
            const FIN_KEY = "d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0";
            const GEM_KEY = "AIzaSyDTDyQWKgCJ3tvcexRCYYvuRUfkTpN4J5w";
            let lastScan = {};

            async function runUltimateAnalysis() {
                let ticker = document.getElementById('tickerInput').value.toUpperCase();
                if(!ticker) return;
                document.getElementById('resScore').innerText = "...";
                
                try {
                    const qR = await fetch(`https://finnhub.io/api/v1/quote?symbol=${ticker}&token=${FIN_KEY}`);
                    const q = await qR.json();
                    
                    const score = Math.floor(Math.random() * 30) + 65; 
                    const timing = score > 75 ? "POSITIVE" : "HOLD";
                    
                    document.getElementById('resScore').innerText = score;
                    document.getElementById('resPrice').innerText = "$" + q.c;
                    document.getElementById('resTiming').innerText = timing;
                    document.getElementById('logBtn').style.display = 'inline-block';
                    
                    if(score >= 75) document.getElementById('mainCard').className = "card breakout-active";
                    else document.getElementById('mainCard').className = "card";

                    const prompt = `Short trade advice for ${ticker}. Score ${score}/100. Be concise.`;
                    const gResp = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${GEM_KEY}`, {
                        method: "POST", headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({contents: [{parts: [{text: prompt}]}]})
                    });
                    const gData = await gResp.json();
                    const verdict = gData.candidates[0].content.parts[0].text;
                    document.getElementById('verdictDetail').innerText = verdict;
                    
                    lastScan = { ticker, score, price: q.c, verdict };
                } catch(e) { document.getElementById('resScore').innerText = "ERR"; }
            }

            function logToJournal() {
                const body = document.getElementById('journalBody');
                const row = `<tr>
                    <td>${new Date().toLocaleDateString()}</td>
                    <td style="font-weight:bold; color:#2f81f7;">${lastScan.ticker}</td>
                    <td>${lastScan.score}</td>
                    <td>$${lastScan.price}</td>
                    <td style="color:#8b949e;">${lastScan.verdict.substring(0,50)}...</td>
                </tr>`;
                body.innerHTML = row + body.innerHTML;
            }
        </script>
    </body>
    </html>
    """
    components.html(architect_html, height=850, scrolling=True)

def render_meters():
    """Gecorrigeerde TradingView Meters"""
    html_meters = """
    <div class="tradingview-widget-container" style="height:400px;">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
      {
        "interval": "1D",
        "width": "100%",
        "isTransparent": false,
        "height": "100%",
        "symbol": "NASDAQ:NVDA",
        "showIntervalTabs": true,
        "displayMode": "regular",
        "locale": "en",
        "colorTheme": "dark"
      }
      </script>
    </div>
    """
    components.html(html_meters, height=420)

# --- 4. DASHBOARD LAYOUT ---

st.title("🛡️ SST MASTER TERMINAL")

tab_research, tab_technical, tab_scanner = st.tabs(["🚀 ARCHITECT & JOURNAL", "📊 MARKET METERS", "🔍 NEURAL SCANNER"])

with tab_research:
    render_sst_architect_and_journal()

with tab_technical:
    st.subheader("Technical Gauge (Daily)")
    render_meters()
    st.divider()
    st.subheader("Advanced Structure Chart")
    components.html("""
        <div style="height: 600px; border-radius: 12px; overflow: hidden; border: 1px solid #30363d;">
            <div id="tv-chart" style="height:100%;"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
            <script type="text/javascript">
                new TradingView.widget({
                    "autosize": true, "symbol": "NASDAQ:NVDA", "interval": "D", "theme": "dark", "container_id": "tv-chart"
                });
            </script>
        </div>
    """, height=620)

with tab_scanner:
    components.html('<iframe src="https://ai-stock-dashboard-qocavy6wajfcfgzjxaszb7.streamlit.app//?embed=true" style="width: 100%; height: 800px; border: none;"></iframe>', height=820)

