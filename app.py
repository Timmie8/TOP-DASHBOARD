import streamlit as st
import streamlit.components.v1 as components

# Pagina instellingen
st.set_page_config(page_title="SST AI TRADING SUITE", layout="wide")

# CSS om Streamlit padding te minimaliseren
st.markdown("""
    <style>
    .block-container { padding: 0px; background-color: #050608; }
    iframe { border: none !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #0d1117; padding: 10px; border-bottom: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# API KEYS
FIN_TOKEN = "d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0"
GEM_TOKEN = "AIzaSyDTDyQWKgCJ3tvcexRCYYvuRUfkTpN4J5w"

# --- TABS DEFINITIES ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🚀 TERMINAL", "🛡️ RISK", "📊 SCANNER", "🔍 ANALYZER", "📈 TECH PRO", "🏛️ ARCHITECT"
])

# 1. SMART TERMINAL
with tab1:
    components.html(f"""
    <div style="background:#050608; color:white; font-family:sans-serif; height:800px; padding:15px;">
        <div style="display:flex; gap:10px; margin-bottom:15px;">
            <input id="t1In" value="NVDA" style="background:#111; color:white; border:1px solid #333; padding:12px; border-radius:8px; flex:1;">
            <button onclick="loadT1()" style="background:#2563eb; color:white; border:none; padding:12px 25px; border-radius:8px; cursor:pointer; font-weight:bold;">SCAN</button>
        </div>
        <div id="t1Chart" style="height:650px; border-radius:12px; overflow:hidden; border:1px solid #333;"></div>
    </div>
    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>
        function loadT1() {{
            const symbol = document.getElementById('t1In').value.toUpperCase();
            new TradingView.widget({{"autosize": true, "symbol": symbol, "interval": "D", "theme": "dark", "container_id": "t1Chart", "style": "1", "hide_side_toolbar": false}});
        }}
        window.onload = loadT1;
    </script>
    """, height=850)

# 2. RISK & TIER
with tab2:
    components.html(f"""
    <div style="background:#0d1117; color:white; font-family:sans-serif; padding:25px; height:800px;">
        <h2 style="margin-top:0;">🛡️ Risk & Tier System</h2>
        <div style="display:flex; gap:10px;">
            <input id="t2In" placeholder="SYMBOL" style="background:#161b22; color:white; border:1px solid #333; padding:12px; border-radius:8px;">
            <button onclick="calcT2()" style="background:#1f6feb; color:white; border:none; padding:12px 25px; border-radius:8px; cursor:pointer;">CALCULATE</button>
        </div>
        <div id="t2Out" style="margin-top:25px;"></div>
    </div>
    <script>
        async function calcT2() {{
            const t = document.getElementById('t2In').value.toUpperCase();
            const r = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{t}}&token={FIN_TOKEN}`);
            const d = await r.json();
            document.getElementById('t2Out').innerHTML = `
                <div style="background:#161b22; padding:25px; border-radius:15px; border-left:6px solid #2f81f7;">
                    <h2 style="margin:0;">${{t}}</h2>
                    <p style="font-size:1.5rem;">Price: $${{d.c}}</p>
                    <p style="color:#f85149; font-weight:bold;">Stop Loss (4%): $${{(d.c*0.96).toFixed(2)}}</p>
                    <p style="color:#3fb950; font-weight:bold;">Target (8%): $${{(d.c*1.08).toFixed(2)}}</p>
                </div>`;
        }}
    </script>
    """, height=800)

# 3. PRO SCANNER
with tab3:
    components.html(f"""
    <div style="background:#0d1117; color:white; font-family:sans-serif; padding:20px;">
        <textarea id="t3In" style="width:100%; height:60px; background:#111; color:#3fb950; border:1px solid #333; padding:10px; border-radius:8px;">AAPL,NVDA,TSLA,AMD,MSFT</textarea>
        <button onclick="scanT3()" style="width:100%; background:#238636; color:white; padding:15px; border:none; border-radius:8px; margin-top:10px; cursor:pointer; font-weight:bold;">START BATCH SCAN</button>
        <table style="width:100%; margin-top:20px; border-collapse:collapse;">
            <thead style="color:#8b949e; text-align:left;"><tr><th>TICKER</th><th>PRICE</th><th>CHANGE</th></tr></thead>
            <tbody id="t3Out"></tbody>
        </table>
    </div>
    <script>
        async function scanT3() {{
            const list = document.getElementById('t3In').value.split(',');
            const out = document.getElementById('t3Out'); out.innerHTML = 'Loading...';
            let html = '';
            for(let t of list) {{
                const r = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{t.trim().toUpperCase()}}&token={FIN_TOKEN}`);
                const d = await r.json();
                if(d.c) html += `<tr style="border-bottom:1px solid #333;"><td style="padding:12px;">${{t.toUpperCase()}}</td><td>$${{d.c}}</td><td style="color:${{d.dp>0?'#3fb950':'#f85149'}}">${{d.dp.toFixed(2)}}%</td></tr>`;
            }}
            out.innerHTML = html;
        }}
    </script>
    """, height=800)

# 4. SIGNAL ANALYZER
with tab4:
    components.html(f"""
    <div style="background:#050505; color:white; font-family:sans-serif; padding:20px;">
        <div style="display:flex; gap:10px; margin-bottom:20px;">
            <input id="t4In" value="TSLA" style="background:#111; border:1px solid #333; color:white; padding:12px; border-radius:8px; flex:1;">
            <button onclick="analyzeT4()" style="background:#2ecc71; color:black; padding:12px 25px; border:none; border-radius:8px; font-weight:bold; cursor:pointer;">ANALYZE SIGNAL</button>
        </div>
        <div id="t4Out" style="display:grid; grid-template-columns:1fr 1fr; gap:20px;"></div>
    </div>
    <script>
        async function analyzeT4() {{
            const t = document.getElementById('t4In').value.toUpperCase();
            const r = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{t}}&token={FIN_TOKEN}`);
            const d = await r.json();
            document.getElementById('t4Out').innerHTML = `
                <div style="background:#111; padding:25px; border-radius:15px; border-top:5px solid #2ecc71; text-align:center;">
                    <div style="color:#8b949e;">SIGNAL</div>
                    <div style="font-size:2rem; font-weight:bold; color:${{d.dp>0?'#3fb950':'#f85149'}}">${{d.dp > 0 ? 'BUY' : 'HOLD'}}</div>
                </div>
                <div style="background:#111; padding:25px; border-radius:15px; border-top:5px solid #2f81f7; text-align:center;">
                    <div style="color:#8b949e;">MOMENTUM</div>
                    <div style="font-size:2rem; font-weight:bold;">${{d.dp.toFixed(2)}}%</div>
                </div>
            `;
        }}
    </script>
    """, height=700)

# 5. TECH PRO
with tab5:
    components.html(f"""
    <div style="background:#050608; color:white; font-family:sans-serif; padding:20px;">
        <div style="display:flex; justify-content:space-between; margin-bottom:30px; border-bottom:1px solid #333; padding-bottom:15px;">
            <h2 style="margin:0;">TechAnalysis <span style="color:#2f81f7;">PRO</span></h2>
            <div>
                <input id="t5In" placeholder="ADD TICKER" style="background:#111; border:1px solid #333; color:white; padding:10px; border-radius:5px; width:120px;">
                <button onclick="addT5()" style="background:#2f81f7; color:white; border:none; padding:10px 15px; border-radius:5px; cursor:pointer;">+</button>
            </div>
        </div>
        <div id="t5Grid" style="display:grid; grid-template-columns:repeat(auto-fill, minmax(250px, 1fr)); gap:20px;"></div>
    </div>
    <script>
        async function addT5() {{
            const t = document.getElementById('t5In').value.toUpperCase();
            if(!t) return;
            const r = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{t}}&token={FIN_TOKEN}`);
            const d = await r.json();
            const card = document.createElement('div');
            card.style = "background:#161b22; padding:20px; border-radius:15px; border:1px solid #333; position:relative;";
            card.innerHTML = `
                <div style="font-weight:bold; font-size:1.2rem;">${{t}}</div>
                <div style="font-size:1.8rem; margin:10px 0;">$${{d.c}}</div>
                <div style="color:${{d.dp>0?'#3fb950':'#f85149'}}; font-weight:bold;">${{d.dp.toFixed(2)}}%</div>
                <button onclick="this.parentElement.remove()" style="position:absolute; top:10px; right:10px; background:none; border:none; color:#f85149; cursor:pointer; font-size:1.2rem;">&times;</button>
            `;
            document.getElementById('t5Grid').prepend(card);
            document.getElementById('t5In').value = '';
        }}
    </script>
    """, height=900)

# 6. SST ARCHITECT
with tab6:
    components.html(f"""
    <div style="background:#0d1117; color:white; font-family:sans-serif; padding:30px; border-radius:20px; border:1px solid #333;">
        <div style="display:flex; gap:15px; margin-bottom:30px;">
            <input id="t6In" placeholder="SYMBOL" style="background:#010409; border:1px solid #2f81f7; color:white; padding:15px; border-radius:12px; flex:1; font-weight:bold;">
            <button onclick="scanT6()" style="background:#238636; color:white; padding:15px 30px; border:none; border-radius:12px; font-weight:bold; cursor:pointer;">RUN ARCHITECT</button>
        </div>
        <div style="display:grid; grid-template-columns: 1fr 2fr; gap:25px;">
            <div style="background:#161b22; padding:30px; border-radius:18px; text-align:center; border:1px solid #333;">
                <div style="color:#8b949e; font-size:0.8rem;">AI CONFIDENCE</div>
                <div id="t6Score" style="font-size:4.5rem; font-weight:900; color:white;">--</div>
            </div>
            <div style="background:#161b22; padding:30px; border-radius:18px; border:1px solid #333;">
                <h3 id="t6Sym" style="margin-top:0;">READY FOR SCAN</h3>
                <p id="t6Ver" style="color:#c9d1d9; line-height:1.6;">Voer ticker in...</p>
            </div>
        </div>
    </div>
    <script>
        async function scanT6() {{
            const t = document.getElementById('t6In').value.toUpperCase();
            if(!t) return;
            document.getElementById('t6Score').innerText = "...";
            const r = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{t}}&token={FIN_TOKEN}`);
            const d = await r.json();
            const score = Math.min(Math.max(Math.round(50 + (d.dp * 10)), 10), 98);
            document.getElementById('t6Score').innerText = score;
            document.getElementById('t6Sym').innerText = t + " ANALYSIS";

            const gRes = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEM_TOKEN}`, {{
                method: "POST", headers: {{"Content-Type": "application/json"}},
                body: JSON.stringify({{contents: [{{parts: [{{text: "Geef kort en krachtig trading advies voor "+t+" in het Nederlands."}}]}}]}})
            }});
            const gData = await gRes.json();
            document.getElementById('t6Ver').innerText = gData.candidates[0].content.parts[0].text;
        }}
    </script>
    """, height=900)
































