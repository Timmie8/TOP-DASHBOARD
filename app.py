import streamlit as st
import streamlit.components.v1 as components

# 1. Pagina Configuratie
st.set_page_config(page_title="SST AI TRADING SUITE PRO", layout="wide")

# API Keys
FIN_KEY = "d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0"
GEM_KEY = "AIzaSyDTDyQWKgCJ3tvcexRCYYvuRUfkTpN4J5w"

# 2. CSS voor de Interface
st.markdown("""
    <style>
    .block-container { padding: 0px; background-color: #050608; }
    .stTabs [data-baseweb="tab-list"] { background-color: #0d1117; padding: 10px; border-bottom: 1px solid #30363d; }
    .stTabs [data-baseweb="tab"] { color: #8b949e; font-weight: bold; }
    .stTabs [aria-selected="true"] { color: #2f81f7 !important; }
    iframe { border: none !important; width: 100% !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Streamlit Tabbladen Structuur
t1, t2, t3, t4, t5, t6 = st.tabs([
    "🚀 SMART TERMINAL", "🛡️ RISK & TIER", "📊 PRO SCANNER", 
    "🔍 SIGNAL ANALYZER", "📈 TECH PRO", "🏛️ ARCHITECT"
])

# --- TAB 1: SMART TERMINAL ---
with t1:
    components.html(f"""
    <div style="background:#050608; color:white; font-family:sans-serif; padding:15px; height:800px;">
        <div style="display:flex; gap:10px; margin-bottom:15px;">
            <input id="t1_in" value="NVDA" style="background:#111; border:1px solid #333; color:white; padding:12px; border-radius:8px; flex:1;">
            <button onclick="runT1()" style="background:#2563eb; color:white; border:none; padding:12px 25px; border-radius:8px; cursor:pointer; font-weight:bold;">SCAN & SCORE</button>
        </div>
        <div style="display:grid; grid-template-columns: 1fr 2fr; gap:15px; margin-bottom:15px;">
            <div style="background:#161b22; padding:15px; border-radius:10px; text-align:center; border:1px solid #333;">
                <div style="font-size:0.7rem; color:#8b949e;">AI MOMENTUM SCORE</div>
                <div id="t1_score" style="font-size:2.5rem; font-weight:900;">--</div>
            </div>
            <div id="t1_advice" style="background:#1e3a8a; padding:15px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-weight:bold; border:1px solid #333;">READY FOR ANALYSIS</div>
        </div>
        <div id="t1_chart" style="height:550px; border-radius:12px; overflow:hidden; border:1px solid #333;"></div>
    </div>
    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>
        async function runT1() {{
            const sym = document.getElementById('t1_in').value.toUpperCase();
            try {{
                const res = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{sym}}&token={FIN_KEY}`);
                const d = await res.json();
                const score = Math.min(Math.max(Math.round(50 + (d.dp * 12)), 5), 98);
                document.getElementById('t1_score').innerText = score;
                const adv = document.getElementById('t1_advice');
                adv.innerText = score > 60 ? "STRONG BUY" : (score < 40 ? "SELL" : "NEUTRAL");
                adv.style.background = score > 60 ? "#065f46" : (score < 40 ? "#7a1a1a" : "#1e3a8a");
                new TradingView.widget({{"autosize":true, "symbol":sym, "interval":"D", "theme":"dark", "container_id":"t1_chart", "style":"1"}});
            }} catch(e) {{ alert("Data Error T1"); }}
        }}
        window.onload = runT1;
    </script>
    """, height=850)

# --- TAB 2: RISK & TIER ---
with t2:
    components.html(f"""
    <div style="background:#0d1117; color:white; font-family:sans-serif; padding:20px; height:600px;">
        <input id="t2_in" value="AAPL" style="background:#111; color:white; border:1px solid #333; padding:12px; border-radius:8px;">
        <button onclick="runT2()" style="background:#1f6feb; color:white; border:none; padding:12px; border-radius:8px;">CALC RISK</button>
        <div id="t2_out" style="margin-top:20px;"></div>
    </div>
    <script>
        async function runT2() {{
            const t = document.getElementById('t2_in').value.toUpperCase();
            const r = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{t}}&token={FIN_KEY}`);
            const d = await r.json();
            document.getElementById('t2_out').innerHTML = `<div style="background:#161b22; padding:20px; border-radius:10px;">
                <h3>Price: $${{d.c}}</h3><p>Stop Loss: $${{(d.c*0.96).toFixed(2)}}</p><p>Target: $${{(d.c*1.08).toFixed(2)}}</p>
            </div>`;
        }}
    </script>
    """, height=600)

# --- TAB 3: PRO SCANNER ---
with t3:
    components.html(f"""
    <div style="background:#0d1117; color:white; font-family:sans-serif; padding:20px;">
        <textarea id="t3_in" style="width:100%; height:50px; background:#111; color:#39d353; border:1px solid #333; padding:10px;">AAPL,NVDA,TSLA,AMD</textarea>
        <button onclick="runT3()" style="width:100%; background:#238636; border:none; color:white; padding:10px; margin-top:10px;">SCAN BATCH</button>
        <table style="width:100%; margin-top:15px; text-align:left;"><tbody id="t3_out"></tbody></table>
    </div>
    <script>
        async function runT3() {{
            const list = document.getElementById('t3_in').value.split(',');
            const out = document.getElementById('t3_out'); out.innerHTML = 'Loading...';
            let h = '';
            for(let t of list) {{
                const r = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{t.trim().toUpperCase()}}&token={FIN_KEY}`);
                const d = await r.json();
                h += `<tr><td>${{t.toUpperCase()}}</td><td>$${{d.c}}</td><td style="color:${{d.dp>0?'#39d353':'#f85149'}}">${{d.dp.toFixed(2)}}%</td></tr>`;
            }}
            out.innerHTML = h;
        }}
    </script>
    """, height=700)

# --- TAB 4: SIGNAL ANALYZER ---
with t4:
    components.html(f"""
    <div style="background:#050505; color:white; font-family:sans-serif; padding:20px;">
        <input id="t4_in" value="TSLA" style="background:#111; color:white; border:1px solid #333; padding:12px; border-radius:8px;">
        <button onclick="runT4()" style="background:#2ecc71; border:none; padding:12px 20px;">ANALYSE</button>
        <div id="t4_out" style="margin-top:20px; display:grid; grid-template-columns:1fr 1fr; gap:10px;"></div>
    </div>
    <script>
        async function runT4() {{
            const r = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{document.getElementById('t4_in').value.toUpperCase()}}&token={FIN_KEY}`);
            const d = await r.json();
            document.getElementById('t4_out').innerHTML = `
                <div style="background:#111; padding:20px; border-radius:10px; border-top:3px solid #2ecc71;">SIGNAL: ${{d.dp > 0 ? 'BUY' : 'HOLD'}}</div>
                <div style="background:#111; padding:20px; border-radius:10px; border-top:3px solid #2f81f7;">CHANGE: ${{d.dp.toFixed(2)}}%</div>
            `;
        }}
    </script>
    """, height=600)

# --- TAB 5: TECH PRO ---
with t5:
    components.html(f"""
    <div style="background:#050608; color:white; font-family:sans-serif; padding:20px;">
        <input id="t5_in" style="background:#111; color:white; border:1px solid #333; padding:8px; width:100px;">
        <button onclick="runT5()" style="background:#2f81f7; color:white; border:none; padding:8px 15px;">+</button>
        <div id="t5_grid" style="display:grid; grid-template-columns:repeat(auto-fill, minmax(180px, 1fr)); gap:15px; margin-top:20px;"></div>
    </div>
    <script>
        async function runT5() {{
            const t = document.getElementById('t5_in').value.toUpperCase();
            const r = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{t}}&token={FIN_KEY}`);
            const d = await r.json();
            const c = document.createElement('div');
            c.style = "background:#161b22; padding:15px; border-radius:10px; border:1px solid #333;";
            c.innerHTML = `<b>${{t}}</b><br>$${{d.c}}<br><span style="color:${{d.dp>0?'#39d353':'#f85149'}}">${{d.dp.toFixed(2)}}%</span>`;
            document.getElementById('t5_grid').prepend(c);
        }}
    </script>
    """, height=800)

# --- TAB 6: SST ARCHITECT ---
with t6:
    components.html(f"""
    <div style="background:#0d1117; color:white; font-family:sans-serif; padding:25px; border-radius:15px; border:1px solid #333;">
        <div style="display:flex; gap:10px; margin-bottom:20px;">
            <input id="t6_in" placeholder="TICKER" style="background:#010409; border:1px solid #2f81f7; color:white; padding:12px; flex:1; border-radius:10px;">
            <button onclick="runT6()" style="background:#238636; color:white; border:none; padding:12px 25px; border-radius:10px; font-weight:bold;">RUN AI</button>
        </div>
        <div style="display:grid; grid-template-columns: 1fr 2fr; gap:20px;">
            <div style="background:#161b22; padding:20px; border-radius:12px; text-align:center;">
                <div style="color:#8b949e; font-size:0.8rem;">SCORE</div>
                <div id="score6" style="font-size:3.5rem; font-weight:900;">--</div>
            </div>
            <div style="background:#161b22; padding:20px; border-radius:12px;">
                <h3 id="sym6" style="margin:0;">READY</h3>
                <p id="ver6" style="color:#c9d1d9; font-size:0.9rem;">Voer ticker in.</p>
            </div>
        </div>
    </div>
    <script>
        async function runT6() {{
            const t = document.getElementById('t6_in').value.toUpperCase();
            try {{
                const r = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{t}}&token={FIN_KEY}`);
                const d = await r.json();
                if(!d.c) throw "error";
                document.getElementById('score6').innerText = Math.round(50 + (d.dp * 12));
                document.getElementById('sym6').innerText = t;
                const g = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEM_KEY}`, {{
                    method: "POST", headers: {{"Content-Type":"application/json"}},
                    body: JSON.stringify({{contents:[{{parts:[{{text:"Geef kort koopadvies voor "+t+" in het Nederlands."}}]}}]}})
                }});
                const gD = await g.json();
                document.getElementById('ver6').innerText = gD.candidates[0].content.parts[0].text;
            }} catch(e) {{ document.getElementById('score6').innerText = "ERR"; }}
        }}
    </script>
    """, height=800)

































