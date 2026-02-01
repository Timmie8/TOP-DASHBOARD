import streamlit as st
import streamlit.components.v1 as components

# 1. Pagina instellingen
st.set_page_config(page_title="SST AI TRADING SUITE", layout="wide")

# Globale Styling voor de interface
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .block-container { padding: 0px; background-color: #050608; }
    .stTabs [data-baseweb="tab-list"] { background-color: #0d1117; padding: 10px; border-bottom: 1px solid #30363d; gap: 15px; }
    .stTabs [data-baseweb="tab"] { color: #8b949e; font-weight: bold; font-size: 14px; }
    .stTabs [aria-selected="true"] { color: #2f81f7 !important; border-bottom-color: #2f81f7 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- TOOLS DEFINITIES (1 t/m 4 blijven behouden) ---

tool1_html = """...""" # (Code van Tool 1)
tool2_html = """...""" # (Code van Tool 2)
tool3_html = """...""" # (Code van Tool 3)
tool4_html = """...""" # (Code van Tool 4)

# --- TOOL 5: TECHANALYSIS PRO (NIEUWE CODE) ---
tool5_html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: system-ui, sans-serif; }
    body { background: #050608; color: #f9fafb; padding: 24px; }
    header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; background: #111; padding: 16px; border-radius: 8px; border: 1px solid #333; }
    header h1 { color: #fff; font-size: 24px; }
    .subtitle { color: #8b949e; margin-bottom: 24px; }
    .action-bar { display: flex; gap: 16px; margin-bottom: 24px; }
    .btn { padding: 10px 20px; border-radius: 6px; border: none; cursor: pointer; font-weight: bold; }
    .btn-primary { background: #2563eb; color: white; }
    .btn-success { background: #16a34a; color: white; }
    .btn-danger { background: #dc2626; color: white; }
    .kpi-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 16px; margin-bottom: 24px; }
    .card { background: #111; padding: 20px; border-radius: 10px; border: 1px solid #333; }
    .kpi-value { font-size: 24px; font-weight: bold; color: #2f81f7; }
    .stock-list { display: flex; flex-direction: column; gap: 16px; }
    .stock-card { border-left: 5px solid #3b82f6; }
    .trend-uptrend { color: #16a34a; }
    .trend-downtrend { color: #dc2626; }
    .alert-box { display: flex; gap: 8px; margin-top: 10px; }
    .alert-input { flex: 1; padding: 8px; border-radius: 6px; border: 1px solid #333; background: #000; color: white; }
    #popup { position: fixed; inset: 0; background: rgba(0,0,0,0.8); display: none; justify-content: center; align-items: center; z-index: 999; }
    #popup-box { background: #111; padding: 25px; border-radius: 10px; border: 1px solid #333; width: 340px; display: flex; flex-direction: column; gap: 15px; }
    .star { color: gold; font-size: 20px; } .inactive { color: #333; }
  </style>
</head>
<body>
  <header><h1>TechAnalysis PRO</h1></header>
  <p class="subtitle">Swing Trading Signals • 1–5 Days</p>
  <div class="action-bar">
    <button class="btn btn-primary" onclick="openPopup()">+ New Analysis</button>
    <button class="btn btn-success" onclick="manualRefresh()">Refresh Now</button>
  </div>
  <div class="kpi-grid">
    <div class="card"><p>Buy Signals</p><p id="kpi-buys" class="kpi-value">0</p></div>
    <div class="card"><p>Active</p><p id="kpi-count" class="kpi-value">0</p></div>
    <div class="card"><p>Market Status</p><p class="kpi-value" style="color:#16a34a">LIVE</p></div>
  </div>
  <div id="stock-list" class="stock-list"></div>

  <div id="popup"><div id="popup-box">
    <h3>New Ticker</h3>
    <input id="ticker-input" class="alert-input" placeholder="e.g. AAPL">
    <button class="btn btn-primary" onclick="addTicker()">Add Ticker</button>
    <button class="btn" style="background:#333;color:white" onclick="closePopup()">Cancel</button>
  </div></div>

  <script>
    async function fetchWithProxy(url) {
      const res = await fetch(`https://api.allorigins.win/get?url=${encodeURIComponent(url)}`);
      const json = await res.json(); return JSON.parse(json.contents);
    }
    function openPopup(){ document.getElementById("popup").style.display="flex"; }
    function closePopup(){ document.getElementById("popup").style.display="none"; }

    async function updateCard(ticker) {
      const card = document.querySelector(`[data-ticker="${ticker}"]`);
      if(!card) return;
      try {
        const data = await fetchWithProxy(`https://query1.finance.yahoo.com/v8/finance/chart/${ticker}?interval=1d&range=6mo`);
        const res = data.chart.result[0];
        const close = res.indicators.quote[0].close.filter(v=>v);
        const last = close.at(-1);
        card.querySelector(".price").textContent = "$" + last.toFixed(2);
        
        const sma20 = close.slice(-20).reduce((a,b)=>a+b)/20;
        const signal = last > sma20 ? "BUY" : "SELL";
        card.querySelector(".signal").textContent = signal;
        card.style.borderLeftColor = signal === "BUY" ? "#16a34a" : "#dc2626";
      } catch(e) { console.error(e); }
      updateKPI();
    }

    function createCardElement(ticker) {
      const div = document.createElement("div");
      div.className = "card stock-card";
      div.dataset.ticker = ticker;
      div.innerHTML = `
        <div style="display:flex; justify-content:space-between">
          <b>${ticker}</b>
          <span class="price">...</span>
        </div>
        <div style="margin:10px 0">Signal: <span class="signal">...</span></div>
        <div class="alert-box">
          <input class="alert-input" placeholder="Alert e.g. <150">
          <button class="btn btn-primary" onclick="alert('Alert set for ${ticker}')">Set</button>
        </div>
        <button class="btn btn-danger" style="width:100%; margin-top:10px" onclick="this.parentElement.remove(); updateKPI();">Remove</button>
      `;
      return div;
    }

    async function addTicker() {
      const val = document.getElementById("ticker-input").value.toUpperCase();
      if(!val) return;
      document.getElementById("stock-list").appendChild(createCardElement(val));
      closePopup(); updateCard(val);
    }

    function updateKPI() {
      const cards = document.querySelectorAll(".stock-card");
      document.getElementById("kpi-count").textContent = cards.length;
      let buys = 0;
      cards.forEach(c => { if(c.querySelector(".signal").textContent === "BUY") buys++; });
      document.getElementById("kpi-buys").textContent = buys;
    }

    function manualRefresh() { document.querySelectorAll(".stock-card").forEach(c => updateCard(c.dataset.ticker)); }
    
    window.onload = () => { ["AAPL", "TSLA"].forEach(t => { 
      document.getElementById("stock-list").appendChild(createCardElement(t)); updateCard(t); 
    }); };
  </script>
</body>
</html>
"""

# --- TABS RENDEREN ---
t1, t2, t3, t4, t5 = st.tabs([
    "🚀 SMART TERMINAL", 
    "🛡️ RISK & TIER", 
    "📊 PRO SCANNER v5.7", 
    "🔍 SIGNAL ANALYZER", 
    "📈 TECHANALYSIS PRO"
])

with t1: components.html(tool1_html, height=850, scrolling=True)
with t2: components.html(tool2_html, height=800, scrolling=True)
with t3: components.html(tool3_html, height=900, scrolling=True)
with t4: components.html(tool4_html, height=900, scrolling=True)
with t5: components.html(tool5_html, height=1000, scrolling=True)

























