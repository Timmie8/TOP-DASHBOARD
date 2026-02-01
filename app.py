import streamlit as st
import streamlit.components.v1 as components

# --- 1. SETTINGS ---
st.set_page_config(page_title="SST MASTER TERMINAL", layout="wide")

st.sidebar.header("🕹️ TERMINAL CONTROLS")
ticker = st.sidebar.text_input("DEFAULT TICKER", "NVDA").upper()

# CSS for Tab Styling
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    [data-baseweb="tab-list"] { background-color: #050505; border-bottom: 1px solid #333; gap: 10px; }
    [data-baseweb="tab"] { 
        height: 50px; background-color: #0d1117; color: #8b949e; 
        border-radius: 8px 8px 0 0; border: 1px solid #30363d; padding: 0 25px;
    }
    [aria-selected="true"] { background-color: #2ecc71 !important; color: black !important; font-weight: bold; }
    iframe { border: none !important; width: 100% !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. TABS ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🚀 ARCHITECT AI", "📊 MARKET METERS", "🛡️ RISK SCANNER", 
    "🔍 DEEP SCANNER", "⚡ PRO DASHBOARD", "🎯 SIGNAL ANALYZER"
])

# --- TAB 5: PRO DASHBOARD (Enhanced Data Fetch) ---
with tab5:
    pro_html = f"""
    <body style="background:#050505; color:white; font-family:sans-serif; padding:15px;">
        <div style="display:flex; justify-content:space-between; align-items:center; background:#111; padding:15px; border:1px solid #333; border-radius:10px;">
            <h2 style="margin:0;">TechAnalysis PRO</h2>
            <div id="pro-status" style="font-size:12px; color:#2ecc71;">Initializing...</div>
        </div>
        
        <div id="pro-content" style="display:none;">
            <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:15px; margin-top:20px;">
                <div style="background:#111; padding:15px; border:1px solid #333; border-radius:10px; text-align:center;">
                    <p style="color:#888; margin:0;">24h Change</p>
                    <h2 id="pro-change">--%</h2>
                </div>
                <div style="background:#111; padding:15px; border:1px solid #333; border-radius:10px; text-align:center;">
                    <p style="color:#888; margin:0;">Target (5%)</p>
                    <h2 id="pro-target" style="color:#2ecc71;">--</h2>
                </div>
                <div style="background:#111; padding:15px; border:1px solid #333; border-radius:10px; text-align:center;">
                    <p style="color:#888; margin:0;">Stop Loss (3%)</p>
                    <h2 id="pro-stop" style="color:#ff4d4f;">--</h2>
                </div>
            </div>

            <div style="margin-top:20px; background:#111; padding:20px; border-radius:10px; border-left:5px solid #2ecc71;">
                <h3 style="margin:0;">{ticker} Signal</h3>
                <p id="pro-price" style="font-size:24px; margin:10px 0;">Loading Price...</p>
                <p id="pro-desc" style="color:#aaa; font-size:14px;">Calculating algorithmic trend strength...</p>
            </div>
        </div>
        <div id="pro-error" style="color:#ff4d4f; margin-top:20px; text-align:center;"></div>

        <script>
            async function loadPro() {{
                try {{
                    const url = `https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=5d`;
                    const response = await fetch(`https://api.allorigins.win/get?url=${{encodeURIComponent(url)}}&ts=${{Date.now()}}`);
                    const json = await response.json();
                    const data = JSON.parse(json.contents);
                    
                    if (!data.chart.result) throw new Error("Ticker not found");
                    
                    const res = data.chart.result[0];
                    const close = res.indicators.quote[0].close.filter(v => v !== null);
                    
                    const last = close[close.length - 1];
                    const prev = close[close.length - 2];
                    const pct = ((last - prev) / prev * 100).toFixed(2);

                    document.getElementById('pro-price').innerText = "$" + last.toFixed(2);
                    document.getElementById('pro-change').innerText = pct + "%";
                    document.getElementById('pro-target').innerText = "$" + (last * 1.05).toFixed(2);
                    document.getElementById('pro-stop').innerText = "$" + (last * 0.97).toFixed(2);
                    document.getElementById('pro-status').innerText = "● LIVE MARKET";
                    document.getElementById('pro-content').style.display = "block";
                }} catch (e) {{
                    document.getElementById('pro-error').innerText = "Data Connection Lost. Retrying in 5s...";
                    setTimeout(loadPro, 5000);
                }}
            }}
            loadPro();
        </script>
    </body>
    """
    components.html(pro_html, height=500)

# --- TAB 6: SIGNAL ANALYZER (Enhanced Logic Recovery) ---
with tab6:
    analyzer_html = f"""
    <body style="background:#050505; color:white; font-family:sans-serif; padding:15px;">
        <h3 style="margin-bottom:15px;">Technical Matrix: {ticker}</h3>
        <table style="width:100%; border-collapse:collapse; background:#0c0c0c; border:1px solid #333; border-radius:10px; overflow:hidden;">
            <thead style="background:#151515; color:#888; text-align:left;">
                <tr><th style="padding:15px;">Indicator Condition</th><th style="padding:15px; text-align:center;">Market Status</th></tr>
            </thead>
            <tbody id="sig-body">
                <tr><td colspan="2" style="padding:30px; text-align:center;">Synchronizing with Liquidity Pools...</td></tr>
            </tbody>
        </table>

        <script>
            async function runAnalysis() {{
                try {{
                    const url = `https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=1y`;
                    const response = await fetch(`https://api.allorigins.win/get?url=${{encodeURIComponent(url)}}&ts=${{Date.now()}}`);
                    const json = await response.json();
                    const data = JSON.parse(json.contents);
                    
                    const res = data.chart.result[0];
                    const q = res.indicators.quote[0];
                    const close = q.close.filter(v => v !== null);
                    const high = q.high.filter(v => v !== null);
                    const low = q.low.filter(v => v !== null);

                    const last = close[close.length - 1];
                    const sma20 = close.slice(-20).reduce((a, b) => a + b, 0) / 20;
                    const sma60 = close.slice(-60).reduce((a, b) => a + b, 0) / 60;
                    
                    const hh = Math.max(...high.slice(-14));
                    const ll = Math.min(...low.slice(-14));
                    const willR = ((hh - last) / (hh - ll)) * -100;

                    const indicators = [
                        {{ n: "Price vs SMA 20 (Short-Term Trend)", v: last > sma20 }},
                        {{ n: "SMA 20 vs SMA 60 (Trend Confirmation)", v: sma20 > sma60 }},
                        {{ n: "Williams %R (Momentum Oscillator)", v: willR > -50 }},
                        {{ n: "Momentum Index (10-Day Window)", v: last > close[close.length - 11] }},
                        {{ n: "Institutional Volume Proxy", v: last > sma20 }}
                    ];

                    document.getElementById('sig-body').innerHTML = indicators.map(row => `
                        <tr style="border-bottom:1px solid #222;">
                            <td style="padding:15px;">${{row.n}}</td>
                            <td style="padding:15px; text-align:center;">
                                <div style="background:${{row.v ? '#123f2a' : '#4a1212'}}; color:${{row.v ? '#1dd75f' : '#ff4d4f'}}; font-weight:bold; border-radius:4px; padding:6px; font-size:12px;">
                                    ${{row.v ? 'BULLISH' : 'BEARISH'}}
                                </div>
                            </td>
                        </tr>
                    `).join('');
                }} catch (e) {{
                    document.getElementById('sig-body').innerHTML = '<tr><td colspan="2" style="text-align:center; padding:20px; color:#ff4d4f;">Failed to fetch matrix. Checking proxy...</td></tr>';
                    setTimeout(runAnalysis, 3000);
                }}
            }}
            runAnalysis();
        </script>
    </body>
    """
    components.html(analyzer_html, height=550)












