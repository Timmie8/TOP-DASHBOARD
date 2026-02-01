import streamlit as st
import streamlit.components.v1 as components

# Pagina instellingen
st.set_page_config(page_title="SST AI TRADING SUITE", layout="wide")

# API Config
FIN_TOKEN = "d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0"
GEM_TOKEN = "AIzaSyDTDyQWKgCJ3tvcexRCYYvuRUfkTpN4J5w"

# CSS om Streamlit elementen te verbergen en tabs te stylen
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .block-container { padding: 0px !important; }
    iframe { height: 100vh !important; width: 100% !important; border: none !important; }
    </style>
    """, unsafe_allow_html=True)

# De volledige applicatie in één HTML/JS block voor maximale stabiliteit
full_app_html = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ background-color: #050608; color: white; font-family: 'Inter', sans-serif; margin: 0; overflow: hidden; }}
        .nav {{ display: flex; background: #0d1117; border-bottom: 1px solid #30363d; padding: 0 20px; }}
        .nav-btn {{ padding: 15px 20px; cursor: pointer; color: #8b949e; border-bottom: 2px solid transparent; font-weight: bold; font-size: 13px; }}
        .nav-btn.active {{ color: #2f81f7; border-bottom: 2px solid #2f81f7; background: rgba(47, 129, 247, 0.1); }}
        .content {{ padding: 20px; height: calc(100vh - 60px); overflow-y: auto; }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}
        
        /* UI Elements */
        input, textarea {{ background: #161b22; border: 1px solid #30363d; color: white; padding: 12px; border-radius: 8px; font-family: inherit; }}
        button {{ background: #238636; color: white; border: none; padding: 12px 25px; border-radius: 8px; cursor: pointer; font-weight: bold; }}
        .card {{ background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 12px; margin-bottom: 20px; }}
        .score-big {{ font-size: 4rem; font-weight: 900; margin: 10px 0; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th {{ text-align: left; color: #8b949e; padding: 10px; border-bottom: 1px solid #30363d; }}
        td {{ padding: 10px; border-bottom: 1px solid #21262d; }}
    </style>
</head>
<body>

<div class="nav">
    <div class="nav-btn active" onclick="openTab(event, 't1')">🚀 TERMINAL</div>
    <div class="nav-btn" onclick="openTab(event, 't2')">🛡️ RISK</div>
    <div class="nav-btn" onclick="openTab(event, 't3')">📊 SCANNER</div>
    <div class="nav-btn" onclick="openTab(event, 't4')">🔍 ANALYZER</div>
    <div class="nav-btn" onclick="openTab(event, 't5')">📈 TECH PRO</div>
    <div class="nav-btn" onclick="openTab(event, 't6')">🏛️ ARCHITECT</div>
</div>

<div class="content">
    <div id="t1" class="tab-content active">
        <div style="display:flex; gap:10px; margin-bottom:20px;">
            <input id="in1" value="NVDA" style="flex:1;">
            <button onclick="run1()">SCAN & SCORE</button>
        </div>
        <div style="display:grid; grid-template-columns: 1fr 2fr; gap:20px; margin-bottom:20px;">
            <div class="card" style="text-align:center;">
                <div style="color:#8b949e;">AI SCORE</div>
                <div id="sc1" class="score-big">--</div>
            </div>
            <div class="card" id="adv1" style="display:flex; align-items:center; justify-content:center; font-size:1.5rem; font-weight:bold;">READY</div>
        </div>
        <div id="ch1" style="height:500px; border-radius:12px; overflow:hidden; border:1px solid #30363d;"></div>
    </div>

    <div id="t2" class="tab-content">
        <div class="card">
            <h2>Risk & Tier</h2>
            <input id="in2" placeholder="TICKER"> <button onclick="run2()">CALC</button>
            <div id="out2" style="margin-top:20px;"></div>
        </div>
    </div>

    <div id="t3" class="tab-content">
        <div class="card">
            <textarea id="in3" style="width:100%; margin-bottom:10px;">AAPL,NVDA,TSLA,AMD</textarea>
            <button onclick="run3()" style="width:100%;">RUN BATCH SCAN</button>
            <table><thead><tr><th>SYMBOL</th><th>PRICE</th><th>CHANGE</th></tr></thead><tbody id="out3"></tbody></table>
        </div>
    </div>

    <div id="t4" class="tab-content">
        <div class="card">
            <input id="in4" value="AAPL"> <button onclick="run4()">ANALYZE</button>
            <div id="out4" style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-top:20px;"></div>
        </div>
    </div>

    <div id="t5" class="tab-content">
        <div class="card">
            <input id="in5" placeholder="ADD SYMBOL"> <button onclick="run5()">+</button>
            <div id="out5" style="display:grid; grid-template-columns:repeat(auto-fill, minmax(200px, 1fr)); gap:15px; margin-top:20px;"></div>
        </div>
    </div>

    <div id="t6" class="tab-content">
        <div class="card">
            <input id="in6" placeholder="DEEP SCAN SYMBOL" style="width:70%;"> <button onclick="run6()">ARCHITECT SCAN</button>
            <div style="display:grid; grid-template-columns:1fr 2fr; gap:20px; margin-top:20px;">
                <div style="text-align:center;" class="card">
                    <div style="color:#8b949e;">CONFIDENCE</div>
                    <div id="sc6" class="score-big">--</div>
                </div>
                <div class="card">
                    <h3 id="sym6">READY</h3>
                    <p id="ver6" style="color:#c9d1d9; line-height:1.6;"></p>
                </div>
            </div>
        </div>
    </div>
</div>

<script src="https://s3.tradingview.com/tv.js"></script>
<script>
    const F_KEY = "{FIN_TOKEN}";
    const G_KEY = "{GEM_TOKEN}";

    function openTab(evt, tabName) {{
        var i, content, btn;
        content = document.getElementsByClassName("tab-content");
        for (i = 0; i < content.length; i++) {{ content[i].style.display = "none"; }}
        btn = document.getElementsByClassName("nav-btn");
        for (i = 0; i < btn.length; i++) {{ btn[i].className = btn[i].className.replace(" active", ""); }}
        document.getElementById(tabName).style.display = "block";
        evt.currentTarget.className += " active";
    }}

    async function run1() {{
        const s = document.getElementById('in1').value.toUpperCase();
        const r = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{s}}&token=${{F_KEY}}`);
        const d = await r.json();
        const score = Math.round(50 + (d.dp * 12));
        document.getElementById('sc1').innerText = score;
        document.getElementById('sc1').style.color = score > 55 ? '#3fb950' : '#f85149';
        document.getElementById('adv1').innerText = score > 55 ? "BULLISH MOMENTUM" : "BEARISH / NEUTRAL";
        new TradingView.widget({{"autosize":true, "symbol":s, "interval":"D", "theme":"dark", "container_id":"ch1", "style":"1"}});
    }}

    async function run2() {{
        const s = document.getElementById('in2').value.toUpperCase();
        const r = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{s}}&token=${{F_KEY}}`);
        const d = await r.json();
        document.getElementById('out2').innerHTML = `<h3>${{s}} at $${{d.c}}</h3><p>Stop Loss: $${{(d.c*0.96).toFixed(2)}}</p><p>Target: $${{(d.c*1.08).toFixed(2)}}</p>`;
    }}

    async function run3() {{
        const list = document.getElementById('in3').value.split(',');
        let h = '';
        for(let t of list) {{
            const r = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{t.trim().toUpperCase()}}&token=${{F_KEY}}`);
            const d = await r.json();
            h += `<tr><td>${{t.toUpperCase()}}</td><td>$${{d.c}}</td><td style="color:${{d.dp>0?'#3fb950':'#f85149'}}">${{d.dp.toFixed(2)}}%</td></tr>`;
        }}
        document.getElementById('out3').innerHTML = h;
    }}

    async function run4() {{
        const s = document.getElementById('in4').value.toUpperCase();
        const r = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{s}}&token=${{F_KEY}}`);
        const d = await r.json();
        document.getElementById('out4').innerHTML = `<div class="card">SIGNAL: ${{d.dp > 0 ? 'BUY' : 'HOLD'}}</div><div class="card">MOMENTUM: ${{d.dp.toFixed(2)}}%</div>`;
    }}

    async function run5() {{
        const s = document.getElementById('in5').value.toUpperCase();
        const r = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{s}}&token=${{F_KEY}}`);
        const d = await r.json();
        const c = document.createElement('div'); c.className = 'card';
        c.innerHTML = `<b>${{s}}</b><br>$${{d.c}}<br>${{d.dp.toFixed(2)}}%`;
        document.getElementById('out5').prepend(c);
    }}

    async function run6() {{
        const s = document.getElementById('in6').value.toUpperCase();
        const r = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{s}}&token=${{F_KEY}}`);
        const d = await r.json();
        document.getElementById('sc6').innerText = Math.round(50 + (d.dp * 15));
        document.getElementById('sym6').innerText = s + " ARCHITECT REPORT";
        const g = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${{G_KEY}}`, {{
            method:"POST", headers:{{"Content-Type":"application/json"}},
            body:JSON.stringify({{contents:[{{parts:[{{text:"Analyseer "+s+" prijs actie. Geef professioneel advies in 2 zinnen."}}]}}]}})
        }});
        const gD = await g.json();
        document.getElementById('ver6').innerText = gD.candidates[0].content.parts[0].text;
    }}
    
    window.onload = run1;
</script>
</body>
</html>
"""

components.html(full_app_html, height=1000, scrolling=False)

































