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

# --- TOOL 1: SMART TERMINAL ---
tool1_html = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #050608; color: white; font-family: sans-serif; padding: 20px; }
        .data-strip { background: #11141b; border-radius: 1.5rem; border: 1px solid #1f2937; margin-bottom: 1rem; padding: 1.5rem; border-left: 8px solid #3b82f6; }
        .value { font-size: 2.5rem; font-weight: 900; }
        .label { color: #6b7280; text-transform: uppercase; font-size: 0.75rem; font-weight: 800; }
        #chart_box { height: 400px; border-radius: 1.5rem; overflow: hidden; border: 1px solid #1f2937; margin-top: 20px; }
        input { background: #11141b; border: 2px solid #1f2937; padding: 15px; border-radius: 1rem; color: white; width: 60%; font-size: 1.2rem; outline: none; }
        button { background: #2563eb; padding: 15px 30px; border-radius: 1rem; font-weight: 900; cursor: pointer; border: none; color: white; }
    </style>
</head>
<body>
    <div style="max-width: 800px; margin: auto;">
        <div style="display: flex; gap: 10px; margin-bottom: 20px;">
            <input id="tickerInput" type="text" value="NVDA">
            <button onclick="fetchAIData()">SCAN</button>
        </div>
        <div id="signalCard" style="background: #1e3a8a; padding: 20px; border-radius: 1.5rem; text-align: center; margin-bottom: 15px;">
            <p class="label">AI Decision</p>
            <div id="adviceVal" style="font-size: 2rem; font-weight: 900;">READY</div>
        </div>
        <div class="data-strip"><p class="label">Market Price</p><div id="priceVal" class="value">--</div></div>
        <div class="data-strip" style="border-left-color: #10b981;"><p class="label">AI Profit Target</p><div id="targetVal" class="value" style="color: #10b981;">--</div></div>
        <div id="chart_box"><div id="chart_container" style="height: 100%;"></div></div>
    </div>
    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>
        async function fetchAIData() {
            const ticker = document.getElementById('tickerInput').value.toUpperCase();
            try {
                const res = await fetch('https://finnhub.io/api/v1/quote?symbol='+ticker+'&token=d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0');
                const data = await res.json();
                document.getElementById('priceVal').innerText = '$' + data.c.toFixed(2);
                document.getElementById('targetVal').innerText = '$' + (data.c * 1.05).toFixed(2);
                document.getElementById('adviceVal').innerText = data.dp > 0 ? "STRONG BUY" : "HOLD / WATCH";
                document.getElementById('signalCard').style.backgroundColor = data.dp > 0 ? "#065f46" : "#1e3a8a";
                new TradingView.widget({"autosize": true, "symbol": ticker, "interval": "D", "theme": "dark", "container_id": "chart_container", "style": "1", "hide_top_toolbar": true});
            } catch(e) { console.error(e); }
        }
        window.onload = fetchAIData;
    </script>
</body>
</html>
"""

# --- TOOL 2: RISK SYSTEM ---
tool2_html = """
<div style="background:#0d1117; color:#c9d1d9; font-family:sans-serif; padding:20px; min-height:800px;">
    <div style="max-width:800px; margin:auto;">
        <h2 style="color:white; margin-bottom:20px;">🛡️ Risk Management & Tiering</h2>
        <div style="display:flex; gap:10px; margin-bottom:25px;">
            <input id="t2" type="text" placeholder="TICKER..." style="background:#161b22; border:1px solid #30363d; color:white; padding:12px; border-radius:8px; flex:1; outline:none;">
            <button onclick="s2()" style="background:#1f6feb; color:white; border:none; padding:12px 25px; border-radius:8px; font-weight:bold; cursor:pointer;">ANALYSE</button>
        </div>
        <div id="out2"></div>
    </div>
</div>
<script>
async function s2() {
    const t = document.getElementById('t2').value.toUpperCase();
    const r = await fetch('https://finnhub.io/api/v1/quote?symbol='+t+'&token=d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0');
    const d = await r.json();
    if(!d.c) return;
    const tier = d.dp > 1.5 ? 'A+' : (d.dp > 0 ? 'A' : 'B');
    document.getElementById('out2').innerHTML = `
        <div style="background:#161b22; border:1px solid #30363d; border-left:8px solid #39d353; padding:25px; border-radius:15px;">
            <b style="font-size:1.5rem; color:white;">${t}</b> - Tier ${tier}
            <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:15px; text-align:center; margin-top:15px;">
                <div style="background:#0d1117; padding:10px;">SL: $${(d.c*0.96).toFixed(2)}</div>
                <div style="background:#0d1117; padding:10px;">Entry: $${d.c.toFixed(2)}</div>
                <div style="background:#0d1117; padding:10px;">TP: $${(d.c*1.08).toFixed(2)}</div>
            </div>
        </div>`;
}
</script>
"""

# --- TOOL 3: PRO SCANNER V5.7 ---
tool3_html = """
<div style="background: #0d1117; color: #e6edf3; font-family: sans-serif; padding: 20px;">
    <div style="max-width: 1000px; margin: auto; background: #0d1117; border: 1px solid #30363d; padding: 30px; border-radius: 20px;">
        <h2 style="margin-top:0;">SST <span style="color:#2f81f7;">TERMINAL</span> v5.7</h2>
        <textarea id="listIn" style="width: 100%; background: #010409; border: 1px solid #30363d; color: white; padding: 15px; border-radius: 12px; margin-bottom: 10px; height: 60px;">AAPL,NVDA,TSLA,AMD,MSFT</textarea>
        <button onclick="runScanner()" style="background: #238636; color: white; border: none; padding: 15px 30px; border-radius: 10px; font-weight: 900; cursor: pointer; width: 100%;">RUN AI SCANNER</button>
        <div id="loader" style="display:none; text-align:center; margin:20px; color:#58a6ff;">Analysing...</div>
        <table id="resTable" style="width:100%; border-collapse:collapse; margin-top:20px; display:none;">
            <thead><tr style="text-align:left; color:#8b949e; border-bottom:1px solid #30363d;"><th>Symbol</th><th>AI Score</th><th>Signal</th></tr></thead>
            <tbody id="resBody"></tbody>
        </table>
    </div>
</div>
<script>
    async function runScanner() {
        const input = document.getElementById('listIn').value;
        const tickers = input.split(/[,\s\\n]+/).filter(t => t.trim() !== "");
        document.getElementById('loader').style.display = 'block';
        const body = document.getElementById('resBody'); body.innerHTML = '';
        for(let t of tickers) {
            try {
                const r = await fetch('https://finnhub.io/api/v1/quote?symbol='+t.trim().toUpperCase()+'&token=d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0');
                const d = await r.json();
                if(d.c) {
                    const s = Math.round(50 + (d.dp * 7));
                    body.insertAdjacentHTML('beforeend', `<tr><td style="padding:15px;"><b>${t.toUpperCase()}</b></td><td>${s}</td><td>${s > 55 ? 'BUY' : 'HOLD'}</td></tr>`);
                }
            } catch(e) {}
        }
        document.getElementById('loader').style.display = 'none';
        document.getElementById('resTable').style.display = 'table';
    }
</script>
"""

# --- TOOL 4: DE VOLLEDIGE SIGNAL ANALYZER (JOUW CODE) ---
tool4_html = """
<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <style>
        body { background-color: #050505; margin: 0; padding: 20px; font-family: Arial, sans-serif; color: white; }
        .container { max-width: 1100px; margin: auto; }
        .search-box { margin-bottom: 14px; display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
        input, select { padding: 10px; font-size: 16px; border-radius: 8px; border: none; background: #1c1c1c; color: #fff; outline:none; }
        button { padding: 10px 16px; font-size: 15px; border-radius: 8px; border: none; cursor: pointer; background: #2ecc71; color: #000; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; background: #0c0c0c; border-radius: 12px; overflow: hidden; }
        th { padding: 12px; text-align: left; background: #151515; border-bottom: 2px solid #222; }
        td { padding: 10px; border-bottom: 1px solid #222; }
        .bullish { background: #123f2a; color: #1dd75f; font-weight: bold; text-align: center; }
        .bearish { background: #4a1212; color: #ff4d4f; font-weight: bold; text-align: center; }
    </style>
</head>
<body>
<div class="container">
    <div class="search-box">
        <input id="symbol" value="AAPL">
        <select id="tf">
            <option value="1h|60d">1H</option>
            <option value="4h|120d">4H</option>
            <option value="1d|1y" selected>1D</option>
        </select>
        <button onclick="loadData()">LOAD ANALYSIS</button>
        <span id="update-time" style="margin-left:12px;color:#aaa;font-size:13px;"></span>
    </div>
    <table>
        <thead><tr><th>Indicator</th><th style="text-align:center">Status</th></tr></thead>
        <tbody id="tbody"></tbody>
    </table>
</div>
<script>
async function loadData() {
    const tbody = document.getElementById("tbody");
    const sym = document.getElementById("symbol").value.toUpperCase();
    const tf = document.getElementById("tf").value.split("|");
    try {
        const yahooUrl = `https://query1.finance.yahoo.com/v8/finance/chart/${sym}?interval=${tf[0]}&range=${tf[1]}`;
        const proxyUrl = `https://api.allorigins.win/get?url=${encodeURIComponent(yahooUrl)}`;
        const response = await fetch(proxyUrl);
        const wrapper = await response.json();
        const data = JSON.parse(wrapper.contents);
        const res = data.chart.result[0];
        const q = res.indicators.quote[0];
        const close = q.close.filter(v => v !== null);
        const high = q.high.filter(v => v !== null);
        const low = q.low.filter(v => v !== null);
        const last = close.at(-1);
        const prev = close.at(-2);
        const pct = ((last - prev) / prev * 100).toFixed(2);
        const date = new Date(res.timestamp.at(-1) * 1000).toLocaleString();

        const avg = a => a.reduce((x, y) => x + y, 0) / a.length;
        const std = a => Math.sqrt(avg(a.map(x => (x - avg(a)) ** 2)));
        const SMA = (p) => close.map((_, i) => i < p ? null : avg(close.slice(i - p, i))).filter(v => v !== null);
        
        const s5 = SMA(5), s20 = SMA(20), s60 = SMA(60), s200 = SMA(200);
        
        function calcRSI(d, p) {
            let r = [];
            for (let i = p; i < d.length; i++) {
                let g = 0, l = 0;
                for (let j = i - p + 1; j <= i; j++) {
                    const x = d[j] - d[j - 1];
                    x > 0 ? g += x : l -= x;
                }
                r.push(100 - (100 / (1 + g / (l || 1))));
            }
            return r;
        }

        const RSI = calcRSI(close, 14).at(-1);
        const MOM = close.at(-1) - close.at(-11);
        const CCI = (last - avg(close.slice(-20))) / (0.015 * std(close.slice(-20)));
        const WILL = -100 * (Math.max(...high.slice(-14)) - last) / (Math.max(...high.slice(-14)) - Math.min(...low.slice(-14)));
        const pivot = (high.at(-2) + low.at(-2) + close.at(-2)) / 3;

        let pos = 0, neg = 0;
        const add = (c) => c ? pos++ : neg++;
        add(s5.at(-1) > s20.at(-1));
        add(s20.at(-1) > s60.at(-1));
        add(s60.at(-1) > s200.at(-1));
        add(WILL > -50);
        add(MOM > 0);
        add(CCI > 0);
        add(RSI > 50);
        add(last > pivot);

        let final = "NEUTRAL", sigCol = "#aaa";
        if (pos - neg > 2) { final = "BUY"; sigCol = "#1dd75f"; }
        if (neg - pos > 2) { final = "SELL"; sigCol = "#ff4d4f"; }

        document.getElementById("update-time").innerText = `Update: ${date}`;
        tbody.innerHTML = `
            <tr style="background:#111"><td style="padding:15px"><b>${sym}</b><br>Prijs: <b>${last.toFixed(2)}</b> (${pct}%)</td>
            <td style="text-align:center"><div style="color:${sigCol};font-size:18px;font-weight:bold">${final}</div>Score: ${pos}/${neg}</td></tr>
            ${row("SMA5 > SMA20", s5.at(-1) > s20.at(-1))}
            ${row("SMA20 > SMA60", s20.at(-1) > s60.at(-1))}
            ${row("RSI > 50", RSI > 50)}
            ${row("Williams %R", WILL > -50)}
            ${row("Momentum", MOM > 0)}
            ${row("CCI Positive", CCI > 0)}
            ${row("Price > Pivot", last > pivot)}
        `;
    } catch (e) { tbody.innerHTML = "<tr><td colspan='2'>Error loading symbol</td></tr>"; }
}
function row(name, cond) { return `<tr><td>${name}</td><td class="${cond ? 'bullish' : 'bearish'}">${cond ? 'Bullish' : 'Bearish'}</td></tr>`; }
loadData();
</script>
</body>
</html>
"""

# --- TABS RENDEREN ---
t1, t2, t3, t4 = st.tabs(["🚀 SMART TERMINAL", "🛡️ RISK & TIER", "📊 PRO SCANNER v5.7", "🔍 SIGNAL ANALYZER"])

with t1:
    components.html(tool1_html, height=850, scrolling=True)
with t2:
    components.html(tool2_html, height=800, scrolling=True)
with t3:
    components.html(tool3_html, height=900, scrolling=True)
with t4:
    components.html(tool4_html, height=900, scrolling=True)























