import streamlit as st
import streamlit.components.v1 as components

# 1. Pagina instellingen
st.set_page_config(page_title="SST AI TRADING SUITE v6.6", layout="wide")

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

# --- DE HTML BLOKKEN ---

# 1. SMART TERMINAL
html_tab1 = """
<div style="background:#050608; color:white; font-family:sans-serif; padding:20px; height:800px;">
    <div style="display:flex; gap:10px; margin-bottom:20px;">
        <input id="in1" value="NVDA" style="background:#111; border:1px solid #333; color:white; padding:12px; border-radius:8px; flex:1;">
        <button onclick="scan1()" style="background:#2563eb; color:white; padding:12px 25px; border:none; border-radius:8px; cursor:pointer;">SCAN</button>
    </div>
    <div id="chart1" style="height:600px; border:1px solid #333; border-radius:12px; overflow:hidden;"></div>
</div>
<script src="https://s3.tradingview.com/tv.js"></script>
<script>
    function scan1(){
        const t = document.getElementById('in1').value.toUpperCase();
        new TradingView.widget({"autosize": true, "symbol": t, "interval": "D", "theme": "dark", "container_id": "chart1", "style": "1"});
    }
    window.onload = scan1;
</script>
"""

# 2. RISK & TIER
html_tab2 = """
<div style="background:#0d1117; color:white; font-family:sans-serif; padding:30px; height:800px;">
    <h2>🛡️ Risk Management</h2>
    <input id="in2" placeholder="TICKER" style="background:#161b22; border:1px solid #333; color:white; padding:12px; border-radius:8px;">
    <button onclick="risk2()" style="background:#1f6feb; color:white; padding:12px 20px; border:none; border-radius:8px; cursor:pointer;">BEREKEN</button>
    <div id="out2" style="margin-top:20px;"></div>
</div>
<script>
    async function risk2(){
        const t = document.getElementById('in2').value.toUpperCase();
        const r = await fetch('https://finnhub.io/api/v1/quote?symbol='+t+'&token=d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0');
        const d = await r.json();
        document.getElementById('out2').innerHTML = `<div style="padding:20px; border-left:5px solid #2f81f7; background:#161b22;">
            <b>${t} Prijs: $${d.c}</b><br>Stop Loss: $${(d.c*0.96).toFixed(2)}<br>Target: $${(d.c*1.08).toFixed(2)}
        </div>`;
    }
</script>
"""

# 3. PRO SCANNER
html_tab3 = """
<div style="background:#0d1117; color:white; font-family:sans-serif; padding:20px;">
    <textarea id="in3" style="width:100%; height:60px; background:#111; color:#39d353; border:1px solid #333; padding:10px;">AAPL,NVDA,TSLA,AMD</textarea>
    <button onclick="scan3()" style="width:100%; background:#238636; color:white; padding:15px; border:none; margin-top:10px; cursor:pointer;">RUN BATCH SCAN</button>
    <table style="width:100%; margin-top:20px; text-align:left;"><tbody id="out3"></tbody></table>
</div>
<script>
    async function scan3(){
        const list = document.getElementById('in3').value.split(',');
        const out = document.getElementById('out3'); out.innerHTML = '';
        for(let t of list){
            const r = await fetch('https://finnhub.io/api/v1/quote?symbol='+t.trim().toUpperCase()+'&token=d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0');
            const d = await r.json();
            out.innerHTML += `<tr><td>${t.toUpperCase()}</td><td>$${d.c}</td><td style="color:${d.dp>0?'#39d353':'#f85149'}">${d.dp.toFixed(2)}%</td></tr>`;
        }
    }
</script>
"""

# 4. SIGNAL ANALYZER
html_tab4 = """
<div style="background:#050505; color:white; font-family:sans-serif; padding:20px;">
    <div style="display:flex; gap:10px;">
        <input id="in4" value="AAPL" style="background:#111; border:1px solid #333; color:white; padding:12px; border-radius:8px; flex:1;">
        <button onclick="scan4()" style="background:#2ecc71; color:black; padding:12px 25px; border:none; border-radius:8px; font-weight:bold;">ANALYSE</button>
    </div>
    <div id="out4" style="margin-top:20px; display:grid; grid-template-columns:1fr 1fr; gap:15px;"></div>
</div>
<script>
    async function scan4(){
        const t = document.getElementById('in4').value.toUpperCase();
        const r = await fetch('https://finnhub.io/api/v1/quote?symbol='+t+'&token=d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0');
        const d = await r.json();
        const score = Math.round(50 + (d.dp * 10));
        document.getElementById('out4').innerHTML = `
            <div style="background:#111; padding:20px; border-radius:10px; border-top:4px solid #2ecc71;"><b>SIGNAL</b><br>${score > 55 ? 'BUY' : 'HOLD'}</div>
            <div style="background:#111; padding:20px; border-radius:10px; border-top:4px solid #2f81f7;"><b>TREND</b><br>${d.dp > 0 ? 'BULLISH' : 'BEARISH'}</div>
        `;
    }
</script>
"""

# 5. TECH PRO
html_tab5 = """
<div style="background:#050608; color:white; font-family:sans-serif; padding:20px;">
    <div style="display:flex; justify-content:space-between; margin-bottom:20px;">
        <h3>TechAnalysis PRO</h3>
        <input id="in5" placeholder="TICKER" style="background:#111; border:1px solid #333; color:white; padding:10px; width:100px;">
        <button onclick="add5()" style="background:#2f81f7; color:white; border:none; padding:10px; border-radius:5px;">ADD</button>
    </div>
    <div id="grid5" style="display:grid; grid-template-columns:repeat(auto-fill, minmax(200px, 1fr)); gap:15px;"></div>
</div>
<script>
    async function add5(){
        const t = document.getElementById('in5').value.toUpperCase();
        const r = await fetch('https://finnhub.io/api/v1/quote?symbol='+t+'&token=d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0');
        const d = await r.json();
        const card = document.createElement('div');
        card.style = "background:#161b22; padding:15px; border-radius:10px; border:1px solid #333;";
        card.innerHTML = `<b>${t}</b><br>$${d.c}<br><span style="color:${d.dp>0?'#39d353':'#f85149'}">${d.dp.toFixed(2)}%</span>`;
        document.getElementById('grid5').prepend(card);
    }
</script>
"""

# 6. SST ARCHITECT
html_tab6 = """
<div style="background:#0d1117; color:white; font-family:sans-serif; padding:25px; border-radius:15px; border:1px solid #30363d;">
    <div style="display:flex; gap:10px; margin-bottom:20px;">
        <input id="in6" placeholder="TICKER" style="background:#010409; border:1px solid #2f81f7; color:white; padding:12px; border-radius:10px; flex:1;">
        <button onclick="scan6()" style="background:#238636; color:white; border:none; padding:12px 25px; border-radius:10px; font-weight:bold;">DEEP SCAN</button>
    </div>
    <div style="display:grid; grid-template-columns: 1fr 2fr; gap:20px;">
        <div style="background:#161b22; padding:20px; border-radius:15px; text-align:center;">
            <div style="font-size:0.8rem; color:#8b949e;">AI SCORE</div>
            <div id="score6" style="font-size:3.5rem; font-weight:900;">--</div>
        </div>
        <div style="background:#161b22; padding:20px; border-radius:15px;">
            <h3 id="sym6" style="margin:0;">Wachtend...</h3>
            <p id="ver6" style="font-size:0.9rem; color:#c9d1d9; margin-top:10px;">Voer ticker in voor AI verdict.</p>
        </div>
    </div>
</div>
<script>
    async function scan6(){
        const t = document.getElementById('in6').value.toUpperCase();
        document.getElementById('score6').innerText = "...";
        const r = await fetch('https://finnhub.io/api/v1/quote?symbol='+t+'&token=d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0');
        const d = await r.json();
        const s = Math.min(Math.max(Math.round(50 + (d.dp * 12)), 5), 98);
        document.getElementById('score6').innerText = s;
        document.getElementById('sym6').innerText = t;
        
        const gRes = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyDTDyQWKgCJ3tvcexRCYYvuRUfkTpN4J5w`, {
            method: "POST", headers: {"Content-Type":"application/json"},
            body: JSON.stringify({contents:[{parts:[{text:"Geef kort trading advies voor "+t+" in het Nederlands."}]}]})
        });
        const gData = await gRes.json();
        document.getElementById('ver6').innerText = gData.candidates[0].content.parts[0].text;
    }
</script>
"""

# --- TABS RENDERING ---
tabs = st.tabs(["🚀 TERMINAL", "🛡️ RISK", "📊 SCANNER", "🔍 ANALYZER", "📈 TECH PRO", "🏛️ ARCHITECT"])

with tabs[0]: components.html(html_tab1, height=800)
with tabs[1]: components.html(html_tab2, height=800)
with tabs[2]: components.html(html_tab3, height=800, scrolling=True)
with tabs[3]: components.html(html_tab4, height=700)
with tabs[4]: components.html(html_tab5, height=900, scrolling=True)
with tabs[5]: components.html(html_tab6, height=900)































