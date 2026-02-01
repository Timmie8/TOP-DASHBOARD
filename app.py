import streamlit as st
import streamlit.components.v1 as components
import requests

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="SST MASTER TERMINAL", layout="wide", initial_sidebar_state="expanded")

# API KEYS
FIN_KEY = "d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0"
GEM_KEY = "AIzaSyDTDyQWKgCJ3tvcexRCYYvuRUfkTpN4J5w"

# --- 2. DYNAMIC TICKER LOGIC ---
st.sidebar.header("🕹️ Terminal Controls")
user_input = st.sidebar.text_input("Main Ticker (for Tabs 1 & 2)", "NVDA").upper()
clean_ticker = user_input.split(':')[-1]
display_ticker = f"NASDAQ:{clean_ticker}" if ":" not in user_input else user_input

# --- 3. AI STRATEGY FUNCTION (Python) ---
def get_ai_strategy(ticker, price):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEM_KEY}"
    prompt = {
        "contents": [{
            "parts": [{
                "text": f"Provide a short swing trade strategy for {ticker} at ${price}. Max 2 sentences in English."
            }]
        }]
    }
    try:
        response = requests.post(url, json=prompt)
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "AI analysis temporarily unavailable."

# --- 4. DATA FETCHING ---
try:
    data = requests.get(f"https://finnhub.io/api/v1/quote?symbol={clean_ticker}&token={FIN_KEY}").json()
    current_price = data.get('c', 0)
except:
    current_price = 0

# --- 5. GLOBAL STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: #050505; }
    .stTabs [data-baseweb="tab"] {
        height: 45px; background-color: #0d1117; color: #8b949e;
        border-radius: 8px 8px 0px 0px; border: 1px solid #30363d;
    }
    .stTabs [aria-selected="true"] { background-color: #2ecc71 !important; color: black !important; font-weight: bold; }
    iframe { border: none !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 6. TABS LAYOUT ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🚀 ARCHITECT AI", 
    "📊 MARKET METERS", 
    "🛡️ RISK SCANNER", 
    "🔍 DEEP SCANNER", 
    "⚡ PRO DASHBOARD",
    "🎯 SIGNAL ANALYZER"
])

# (Tabs 1-5 remain consistent with previous logic...)

# --- TAB 6: SIGNAL ANALYZER (NEW TRANSLATED CODE) ---
with tab6:
    signal_analyzer_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ background-color: #050505; margin: 0; padding: 10px; font-family: 'Segoe UI', Arial, sans-serif; color: white; }}
            .search-box {{ margin-bottom: 20px; display: flex; align-items: center; gap: 10px; }}
            input, select {{ padding: 10px; border-radius: 8px; border: 1px solid #333; background: #1c1c1c; color: #fff; }}
            button {{ padding: 10px 20px; border-radius: 8px; border: none; cursor: pointer; background: #2ecc71; color: #000; font-weight: bold; }}
            table {{ width: 100%; border-collapse: collapse; background: #0c0c0c; border-radius: 12px; overflow: hidden; border: 1px solid #222; }}
            th {{ padding: 15px; text-align: left; background: #151515; border-bottom: 2px solid #222; color: #888; text-transform: uppercase; font-size: 12px; }}
            td {{ padding: 12px; border-bottom: 1px solid #222; }}
            .bullish {{ background: #123f2a; color: #1dd75f; font-weight: bold; text-align: center; border-radius: 4px; }}
            .bearish {{ background: #4a1212; color: #ff4d4f; font-weight: bold; text-align: center; border-radius: 4px; }}
            .header-cell {{ background: #111; border-left: 4px solid #2ecc71; }}
        </style>
    </head>
    <body>
        <div class="search-box">
            <input id="symbol" value="{clean_ticker}">
            <select id="tf">
                <option value="1h|60d">1 Hour</option>
                <option value="4h|120d">4 Hours</option>
                <option value="1d|1y" selected>Daily</option>
            </select>
            <button onclick="loadData()">RUN ANALYSIS</button>
            <span id="update-time" style="color:#666; font-size:12px;"></span>
        </div>

        <table>
            <thead>
                <tr>
                    <th>Technical Indicator</th>
                    <th style="text-align:center">Market Status</th>
                </tr>
            </thead>
            <tbody id="tbody"></tbody>
        </table>

        <script>
        async function loadData() {{
            const tbody = document.getElementById("tbody");
            const sym = document.getElementById("symbol").value.toUpperCase();
            const tf = document.getElementById("tf").value.split("|");
            
            try {{
                const yahooUrl = `https://query1.finance.yahoo.com/v8/finance/chart/${{sym}}?interval=${{tf[0]}}&range=${{tf[1]}}`;
                const proxyUrl = `https://api.allorigins.win/get?url=${{encodeURIComponent(yahooUrl)}}`;

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
                const change = last - prev;
                const pct = (change / prev * 100).toFixed(2);
                const date = new Date(res.timestamp.at(-1) * 1000).toLocaleTimeString();

                const avg = a => a.reduce((x, y) => x + y, 0) / a.length;
                const std = a => Math.sqrt(avg(a.map(x => (x - avg(a)) ** 2)));
                const SMA = (p) => close.map((_, i) => i < p ? null : avg(close.slice(i - p, i))).filter(v => v !== null);

                const s5 = SMA(5), s20 = SMA(20), s60 = SMA(60), s200 = SMA(200);
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
                if (pos - neg > 2) {{ final = "BUY"; sigCol = "#1dd75f"; }}
                if (neg - pos > 2) {{ final = "SELL"; sigCol = "#ff4d4f"; }}

                document.getElementById("update-time").innerText = `Last Update: ${{date}}`;
                tbody.innerHTML = `
                    <tr class="header-cell">
                        <td style="padding:20px"><b>${{sym}}</b> · ${{tf[0]}}<br>Price: <b>$${{last.toFixed(2)}}</b> (${{pct}}%)</td>
                        <td style="text-align:center"><div style="color:${{sigCol}};font-size:22px;font-weight:bold">${{final}}</div>AI Confidence: ${{pos}}/${{pos+neg}}</td>
                    </tr>
                    ${{row("SMA Cross (5/20)", s5.at(-1) > s20.at(-1))}}
                    ${{row("Trend (20/60)", s20.at(-1) > s60.at(-1))}}
                    ${{row("Long Term (60/200)", s60.at(-1) > s200.at(-1))}}
                    ${{row("Williams %R (Overbought/Sold)", WILL > -50)}}
                    ${{row("Momentum (10-Period)", MOM > 0)}}
                    ${{row("Commodity Channel Index (CCI)", CCI > 0)}}
                    ${{row("Relative Strength (RSI)", RSI > 50)}}
                    ${{row("Price vs Pivot Point", last > pivot)}}
                `;

            }} catch (e) {{
                tbody.innerHTML = `<tr><td colspan="2" style="text-align:center;padding:20px;">Error loading data for ${{sym}}</td></tr>`;
            }}
        }}

        function row(name, cond) {{
            return `<tr><td>${{name}}</td><td class="${{cond ? 'bullish' : 'bearish'}}">${{cond ? 'BULLISH' : 'BEARISH'}}</td></tr>`;
        }}

        function calcRSI(d, p) {{
            let r = [];
            for (let i = p; i < d.length; i++) {{
                let g = 0, l = 0;
                for (let j = i - p + 1; j <= i; j++) {{
                    const x = d[j] - d[j - 1];
                    x > 0 ? g += x : l -= x;
                }}
                r.push(100 - (100 / (1 + g / (l || 1))));
            }}
            return r;
        }}

        loadData();
        </script>
    </body>
    </html>
    """
    components.html(signal_analyzer_html, height=700)




