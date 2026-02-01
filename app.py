import streamlit as st
import streamlit.components.v1 as components

# 1. Pagina configuratie
st.set_page_config(page_title="SST AI TRADING SUITE", layout="wide")

# API Sleutels
FIN_KEY = "d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0"
GEM_KEY = "AIzaSyDTDyQWKgCJ3tvcexRCYYvuRUfkTpN4J5w"

# CSS voor de tabbladen en achtergrond
st.markdown("""
    <style>
    .block-container { padding: 0px; background-color: #050608; }
    .stTabs [data-baseweb="tab-list"] { 
        background-color: #0d1117; 
        padding: 10px 20px; 
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #8b949e;
        border-radius: 4px;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f2937;
        color: #2f81f7 !important;
    }
    iframe { border: none !important; }
    </style>
    """, unsafe_allow_html=True)

# Initialiseer tabbladen
t1, t2, t3, t4, t5, t6 = st.tabs([
    "🚀 SMART TERMINAL", "🛡️ RISK & TIER", "📊 PRO SCANNER", 
    "🔍 SIGNAL ANALYZER", "📈 TECH PRO", "🏛️ ARCHITECT"
])

# --- TAB 1: SMART TERMINAL ---
with t1:
    components.html(f"""
    <div style="background:#050608; color:white; font-family:sans-serif; height:800px; padding:20px;">
        <div style="display:flex; gap:10px; margin-bottom:20px;">
            <input id="t1_in" value="NVDA" style="background:#111; border:1px solid #333; color:white; padding:12px; border-radius:8px; flex:1;">
            <button onclick="updateT1()" style="background:#2563eb; color:white; padding:12px 25px; border:none; border-radius:8px; cursor:pointer; font-weight:bold;">SCAN TICKER</button>
        </div>
        <div id="t1_advice" style="background:#1e3a8a; padding:15px; border-radius:10px; text-align:center; font-weight:bold; margin-bottom:15px;">INITIALIZING...</div>
        <div id="t1_chart" style="height:550px; border-radius:12px; overflow:hidden; border:1px solid #333;"></div>
    </div>
    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>
        async function updateT1() {{
            const sym = document.getElementById('t1_in').value.toUpperCase();
            const res = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{sym}}&token={FIN_KEY}`);
            const d = await res.json();
            const adv = document.getElementById('t1_advice');
            adv.innerText = d.dp > 0 ? "BULLISH SIGNAL" : "WATCH / NEUTRAL";
            adv.style.background = d.dp > 0 ? "#065f46" : "#1e3a8a";
            new TradingView.widget({{"autosize":true, "symbol":sym, "interval":"D", "theme":"dark", "container_id":"t1_chart", "style":"1"}});
        }}
        window.onload = updateT1;
    </script>
    """, height=800)

# --- TAB 2: RISK & TIER ---
with t2:
    components.html(f"""
    <div style="background:#0d1117; color:white; font-family:sans-serif; padding:30px; height:800px;">
        <h2>🛡️ Risk Management</h2>
        <div style="display:flex; gap:10px; margin:20px 0;">
            <input id="t2_in" placeholder="TICKER" style="background:#161b22; border:1px solid #333; color:white; padding:12px; border-radius:8px;">
            <button onclick="calcT2()" style="background:#1f6feb; color:white; border:none; padding:12px 25px; border-radius:8px; cursor:pointer;">ANALYSE</button>
        </div>
        <div id="t2_out"></div>
    </div>
    <script>
        async function calcT2() {{
            const t = document.getElementById('t2_in').value.toUpperCase();
            const r = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{t}}&token={FIN_KEY}`);
            const d = await r.json();
            document.getElementById('t2_out').innerHTML = `
                <div style="background:#161b22; padding:25px; border-radius:15px; border-left:8px solid #2f81f7;">
                    <h1 style="margin:0;">${{t}}</h1>
                    <p style="font-size:1.4rem;">Price: $${{d.c}}</p>
                    <p style="color:#f85149;">Stop Loss (4%): $${{(d.c*0.96).toFixed(2)}}</p>
                    <p style="color:#3fb950;">Target (8%): $${{(d.c*1.08).toFixed(2)}}</p>
                </div>`;
        }}
    </script>
    """, height=800)

# --- TAB 3: PRO SCANNER ---
with t3:
    components.html(f"""
    <div style="background:#0d1117; color:white; font-family:sans-serif; padding:20px; height:800px;">
        <textarea id="t3_list" style="width:100%; height:80px; background:#111; color:#3fb950; border:1px solid #333; padding:10px; border-radius:8px;">AAPL, NVDA, TSLA, AMD</textarea>
        <button onclick="scanT3()" style="width:100%; padding:15px; background:#238636; color:white; border:none; margin-top:10px; cursor:pointer; font-weight:bold; border-radius:8px;">RUN SCANNER</button>
        <table style="width:100%; margin-top:20px; border-collapse:collapse; text-align:left;">
            <thead style="border-bottom:2px solid #333; color:#8b949e;"><tr><th>SYMBOL</th><th>PRICE</th><th>CHANGE</th></tr></thead>
            <tbody id="t3_body"></tbody>
        </table>
    </div>
    <script>
        async function scanT3() {{
            const list = document.getElementById('t3_list').value.split(',').map(s => s.trim());
            const body = document.getElementById('t3_body'); body.innerHTML = 'Scanning...';
            let html = '';
            for(let t of list) {{
                const r = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{t.toUpperCase()}}&token={FIN_KEY}`);
                const d = await r.json();
                if(d.c) html += `<tr style="border-bottom:1px solid #222;"><td style="padding:12px;">${{t.toUpperCase()}}</td><td>$${{d.c}}</td><td style="color:${{d.dp>0?'#3fb950':'#f85149'}}">${{d.dp.toFixed(2)}}%</td></tr>`;
            }}
            body.innerHTML = html;
        }}
    </script>
    """, height=800)

# --- TAB 4: SIGNAL ANALYZER ---
with t4:
    components.html(f"""
    <div style="background:#050505; color:white; font-family:sans-serif; padding:20px; height:800px;">
        <div style="display:flex; gap:10px;">
            <input id="t4_in" value="TSLA" style="background:#111; border:1px solid #333; color:white; padding:12px; border-radius:8px; flex:1;">
            <button onclick="analyzeT4()" style="background:#2ecc71; color:black; padding:12px 25px; border:none; border-radius:8px; font-weight:bold; cursor:pointer;">ANALYZE</button>
        </div>
        <div id="t4_res" style="margin-top:20px; display:grid; grid-template-columns:1fr 1fr; gap:20px;"></div>
    </div>
    <script>
        async function analyzeT4() {{
            const s = document.getElementById('t4_in').value.toUpperCase();
            const r = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{s}}&token={FIN_KEY}`);
            const d = await r.json();
            document.getElementById('t4_res').innerHTML = `
                <div style="background:#111; padding:20px; border-radius:10px; border-top:4px solid #2ecc71;">
                    <div style="color:#8b949e; font-size:0.8rem;">TREND</div>
                    <div style="font-size:1.5rem; font-weight:bold;">${{d.dp > 0 ? 'BULLISH' : 'BEARISH'}}</div>
                </div>
                <div style="background:#111; padding:20px; border-radius:10px; border-top:4px solid #2f81f7;">
                    <div style="color:#8b949e; font-size:0.8rem;">DAILY CHANGE</div>
                    <div style="font-size:1.5rem; font-weight:bold;">${{d.dp.toFixed(2)}}%</div>
                </div>`;
        }}
    </script>
    """, height=800)

# --- TAB 5: TECH PRO ---
with t5:
    components.html(f"""
    <div style="background:#050608; color:white; font-family:sans-serif; padding:20px; min-height:800px;">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #333; padding-bottom:15px; margin-bottom:20px;">
            <h3>TechAnalysis PRO</h3>
            <div style="display:flex; gap:10px;">
                <input id="t5_in" placeholder="TICKER" style="background:#111; border:1px solid #333; color:white; padding:8px; width:100px; border-radius:5px;">
                <button onclick="addT5()" style="background:#2f81f7; color:white; border:none; padding:8px 15px; border-radius:5px; cursor:pointer;">+</button>
            </div>
        </div>
        <div id="t5_grid" style="display:grid; grid-template-columns:repeat(auto-fill, minmax(200px, 1fr)); gap:15px;"></div>
    </div>
    <script>
        async function addT5() {{
            const t = document.getElementById('t5_in').value.toUpperCase();
            if(!t) return;
            const r = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{t}}&token={FIN_KEY}`);
            const d = await r.json();
            const card = document.createElement('div');
            card.style = "background:#161b22; padding:15px; border-radius:10px; border:1px solid #333; position:relative;";
            card.innerHTML = `
                <b>${{t}}</b> <button onclick="this.parentElement.remove()" style="float:right; background:none; border:none; color:#f85149; cursor:pointer;">&times;</button>
                <div style="font-size:1.5rem; margin:10px 0;">$${{d.c}}</div>
                <div style="color:${{d.dp>0?'#3fb950':'#f85149'}}">${{d.dp.toFixed(2)}}%</div>`;
            document.getElementById('t5_grid').prepend(card);
            document.getElementById('t5_in').value = '';
        }}
    </script>
    """, height=900)

# --- TAB 6: SST ARCHITECT ---
with t6:
    components.html(f"""
    <div style="background:#0d1117; color:white; font-family:sans-serif; padding:30px; border-radius:15px; border:1px solid #333;">
        <div style="display:flex; gap:10px; margin-bottom:25px;">
            <input id="t6_in" placeholder="SYMBOL" style="background:#010409; border:1px solid #2f81f7; color:white; padding:15px; border-radius:10px; flex:1; font-weight:bold;">
            <button onclick="scanT6()" style="background:#238636; color:white; border:none; padding:15px 30px; border-radius:10px; font-weight:bold; cursor:pointer;">DEEP SCAN</button>
        </div>
        <div style="display:grid; grid-template-columns: 1fr 2fr; gap:20px;">
            <div style="background:#161b22; padding:30px; border-radius:15px; text-align:center; border:1px solid #333;">
                <div style="color:#8b949e;">AI SCORE</div>
                <div id="t6_score" style="font-size:4rem; font-weight:900; color:white;">--</div>
            </div>
            <div style="background:#161b22; padding:30px; border-radius:15px; border:1px solid #333;">
                <h3 id="t6_sym" style="margin:0;">Wachtend op input...</h3>
                <p id="t6_ver" style="color:#c9d1d9; line-height:1.6; font-size:0.95rem;"></p>
            </div>
        </div>
    </div>
    <script>
        async function scanT6() {{
            const t = document.getElementById('t6_in').value.toUpperCase();
            if(!t) return;
            document.getElementById('t6_score').innerText = "...";
            const r = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{t}}&token={FIN_KEY}`);
            const d = await r.json();
            const score = Math.min(Math.max(Math.round(50 + (d.dp * 10)), 5), 98);
            document.getElementById('t6_score').innerText = score;
            document.getElementById('t6_sym').innerText = t + " ANALYSIS";

            const g = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEM_KEY}`, {{
                method: "POST", headers: {{"Content-Type":"application/json"}},
                body: JSON.stringify({{contents:[{{parts:[{{text:"Geef kort en professioneel trading advies voor "+t+" in het Nederlands."}}]}}]}})
            }});
            const res = await g.json();
            document.getElementById('t6_ver').innerText = res.candidates[0].content.parts[0].text;
        }}
    </script>
    """, height=800)
































