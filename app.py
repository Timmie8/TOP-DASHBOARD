import streamlit as st
import streamlit.components.v1 as components

# 1. Globale Pagina Instellingen
st.set_page_config(page_title="SST AI TRADING SUITE", layout="wide")

# API Config
FIN_TOKEN = "d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0"
GEM_TOKEN = "AIzaSyDTDyQWKgCJ3tvcexRCYYvuRUfkTpN4J5w"

# 2. CSS voor schone interface
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; background-color: #050608; }
    .stTabs [data-baseweb="tab-list"] { background-color: #0d1117; border-radius: 10px; padding: 5px; }
    .stTabs [data-baseweb="tab"] { color: #8b949e; font-weight: bold; }
    .stTabs [aria-selected="true"] { color: #2f81f7 !important; }
    iframe { border: none !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Definitie van de Tabbladen
tabs = st.tabs([
    "🚀 TERMINAL", 
    "🛡️ RISK", 
    "📊 SCANNER", 
    "🔍 ANALYZER", 
    "📈 TECH PRO", 
    "🏛️ ARCHITECT"
])

# --- TAB 1: SMART TERMINAL ---
with tabs[0]:
    html_1 = f"""
    <div style="background:#050608; color:white; font-family:sans-serif; height:800px; padding:10px;">
        <div style="display:flex; gap:10px; margin-bottom:15px;">
            <input id="in1" value="NVDA" style="background:#111; color:white; border:1px solid #333; padding:12px; border-radius:8px; flex:1;">
            <button onclick="run1()" style="background:#2563eb; color:white; border:none; padding:12px 25px; border-radius:8px; cursor:pointer;">SCAN</button>
        </div>
        <div id="chart1" style="height:600px; border:1px solid #333; border-radius:12px; overflow:hidden;"></div>
    </div>
    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>
        function run1() {{
            new TradingView.widget({{"autosize": true, "symbol": document.getElementById('in1').value, "interval": "D", "theme": "dark", "container_id": "chart1", "style": "1"}});
        }}
        window.onload = run1;
    </script>
    """
    components.html(html_1, height=800)

# --- TAB 2: RISK MANAGEMENT ---
with tabs[1]:
    html_2 = f"""
    <div style="background:#0d1117; color:white; font-family:sans-serif; padding:20px;">
        <h2>🛡️ Risk Tier</h2>
        <input id="in2" placeholder="TICKER" style="background:#161b22; color:white; border:1px solid #333; padding:12px; border-radius:8px;">
        <button onclick="run2()" style="background:#1f6feb; color:white; border:none; padding:12px 20px; border-radius:8px; cursor:pointer;">BEREKEN</button>
        <div id="out2" style="margin-top:20px;"></div>
    </div>
    <script>
        async function run2() {{
            const t = document.getElementById('in2').value.toUpperCase();
            const r = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{t}}&token={FIN_TOKEN}`);
            const d = await r.json();
            document.getElementById('out2').innerHTML = `<div style="background:#161b22; padding:20px; border-radius:10px; border-left:5px solid #2f81f7;">
                <h3>${{t}}: $${{d.c}}</h3>
                <p>Stop Loss (4%): $${{(d.c*0.96).toFixed(2)}}</p>
                <p>Target (8%): $${{(d.c*1.08).toFixed(2)}}</p>
            </div>`;
        }}
    </script>
    """
    components.html(html_2, height=600)

# --- TAB 3: BATCH SCANNER ---
with tabs[2]:
    html_3 = f"""
    <div style="background:#0d1117; color:white; font-family:sans-serif; padding:20px;">
        <textarea id="in3" style="width:100%; height:50px; background:#111; color:#39d353; border:1px solid #333; padding:10px;">AAPL,NVDA,TSLA,AMD</textarea>
        <button onclick="run3()" style="width:100%; background:#238636; border:none; color:white; padding:12px; margin-top:10px; cursor:pointer;">START BATCH</button>
        <table style="width:100%; margin-top:15px; text-align:left;"><tbody id="out3"></tbody></table>
    </div>
    <script>
        async function run3() {{
            const list = document.getElementById('in3').value.split(',');
            const out = document.getElementById('out3'); out.innerHTML = '';
            for(let t of list) {{
                const r = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{t.trim().toUpperCase()}}&token={FIN_TOKEN}`);
                const d = await r.json();
                out.innerHTML += `<tr><td>${{t.toUpperCase()}}</td><td>$${{d.c}}</td><td style="color:${{d.dp>0?'#39d353':'#f85149'}}">${{d.dp.toFixed(2)}}%</td></tr>`;
            }}
        }}
    </script>
    """
    components.html(html_3, height=800, scrolling=True)

# --- TAB 4: SIGNAL ANALYZER ---
with tabs[3]:
    html_4 = f"""
    <div style="background:#050505; color:white; font-family:sans-serif; padding:20px;">
        <input id="in4" value="AAPL" style="background:#111; color:white; border:1px solid #333; padding:12px; border-radius:8px;">
        <button onclick="run4()" style="background:#2ecc71; border:none; padding:12px 20px; cursor:pointer; font-weight:bold;">ANALYSE</button>
        <div id="out4" style="margin-top:20px; display:grid; grid-template-columns:1fr 1fr; gap:10px;"></div>
    </div>
    <script>
        async function run4() {{
            const r = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{document.getElementById('in4').value.toUpperCase()}}&token={FIN_TOKEN}`);
            const d = await r.json();
            document.getElementById('out4').innerHTML = `
                <div style="background:#111; padding:20px; border-radius:10px; border-top:3px solid #2ecc71;">SIGNAL: ${{d.dp > 0 ? 'BUY' : 'HOLD'}}</div>
                <div style="background:#111; padding:20px; border-radius:10px; border-top:3px solid #2f81f7;">CHANGE: ${{d.dp.toFixed(2)}}%</div>
            `;
        }}
    </script>
    """
    components.html(html_4, height=600)

# --- TAB 5: TECH PRO (GRID) ---
with tabs[4]:
    html_5 = f"""
    <div style="background:#050608; color:white; font-family:sans-serif; padding:20px;">
        <div style="display:flex; justify-content:space-between; margin-bottom:15px;">
            <h3>TechAnalysis PRO</h3>
            <div>
                <input id="in5" placeholder="SYMBOL" style="background:#111; color:white; border:1px solid #333; padding:8px; width:100px;">
                <button onclick="run5()" style="background:#2f81f7; color:white; border:none; padding:8px 15px; cursor:pointer;">+</button>
            </div>
        </div>
        <div id="grid5" style="display:grid; grid-template-columns:repeat(auto-fill, minmax(200px, 1fr)); gap:15px;"></div>
    </div>
    <script>
        async function run5() {{
            const t = document.getElementById('in5').value.toUpperCase();
            const r = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{t}}&token={FIN_TOKEN}`);
            const d = await r.json();
            const c = document.createElement('div');
            c.style = "background:#161b22; padding:15px; border-radius:10px; border:1px solid #333;";
            c.innerHTML = `<b>${{t}}</b><br>$${{d.c}}<br><span style="color:${{d.dp>0?'#39d353':'#f85149'}}">${{d.dp.toFixed(2)}}%</span>`;
            document.getElementById('grid5').prepend(c);
        }}
    </script>
    """
    components.html(html_5, height=900, scrolling=True)

# --- TAB 6: SST ARCHITECT (AI) ---
with tabs[5]:
    html_6 = f"""
    <div style="background:#0d1117; color:white; font-family:sans-serif; padding:25px; border-radius:15px; border:1px solid #333;">
        <div style="display:flex; gap:10px; margin-bottom:20px;">
            <input id="in6" placeholder="TICKER" style="background:#010409; color:white; border:1px solid #2f81f7; padding:12px; flex:1; border-radius:10px;">
            <button onclick="run6()" style="background:#238636; color:white; border:none; padding:12px 25px; border-radius:10px; font-weight:bold; cursor:pointer;">RUN AI</button>
        </div>
        <div style="display:grid; grid-template-columns: 1fr 2fr; gap:20px;">
            <div style="background:#161b22; padding:20px; border-radius:12px; text-align:center;">
                <div style="color:#8b949e;">SCORE</div>
                <div id="score6" style="font-size:3.5rem; font-weight:900;">--</div>
            </div>
            <div style="background:#161b22; padding:20px; border-radius:12px;">
                <h3 id="sym6" style="margin:0;">READY</h3>
                <p id="ver6" style="color:#c9d1d9; font-size:0.9rem;">Voer ticker in.</p>
            </div>
        </div>
    </div>
    <script>
        async function run6() {{
            const t = document.getElementById('in6').value.toUpperCase();
            const r = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{t}}&token={FIN_TOKEN}`);
            const d = await r.json();
            document.getElementById('score6').innerText = Math.round(50 + (d.dp * 10));
            document.getElementById('sym6').innerText = t;
            
            const g = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEM_TOKEN}`, {{
                method: "POST", headers: {{"Content-Type":"application/json"}},
                body: JSON.stringify({{contents:[{{parts:[{{text:"Geef kort koopadvies voor "+t+" in het Nederlands."}}]}}]}})
            }});
            const gD = await g.json();
            document.getElementById('ver6').innerText = gD.candidates[0].content.parts[0].text;
        }}
    </script>
    """
    components.html(html_6, height=800)
































