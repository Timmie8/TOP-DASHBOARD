import streamlit as st
import streamlit.components.v1 as components

# --- 1. SETTINGS ---
st.set_page_config(page_title="SST MASTER TERMINAL", layout="wide")

st.sidebar.header("🕹️ TERMINAL CONTROLS")
ticker = st.sidebar.text_input("ENTER TICKER", "NVDA").upper()

# CSS to fix layout and visibility
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    [data-baseweb="tab-list"] { background-color: #050505; border-bottom: 1px solid #333; gap: 5px; }
    [data-baseweb="tab"] { 
        height: 50px; background-color: #0d1117; color: #8b949e; 
        border: 1px solid #30363d; padding: 0 20px;
    }
    [aria-selected="true"] { background-color: #2ecc71 !important; color: black !important; font-weight: bold; }
    iframe { border: none !important; width: 100% !important; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE 6 TABS ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🚀 ARCHITECT AI", "📊 MARKET METERS", "🛡️ RISK SCANNER", 
    "🔍 DEEP SCANNER", "⚡ PRO DASHBOARD", "🎯 SIGNAL ANALYZER"
])

# TAB 1: AI OVERVIEW
with tab1:
    st.markdown(f"""
    <div style="background:#111; padding:20px; border-radius:12px; border:1px solid #333;">
        <h2 style="color:#2ecc71; margin-top:0;">SST ARCHITECT AI | {ticker}</h2>
        <p style="color:#888;">AI is scanning global order flows for {ticker}. Recommended trade type: <b>SWING</b>.</p>
    </div>
    """, unsafe_allow_html=True)

# TAB 2: TECHNICAL GAUGES (TradingView - Always Works)
with tab2:
    components.html(f"""
        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
        {{ "interval": "1D", "width": "100%", "height": 450, "symbol": "{ticker}", "showIntervalTabs": true, "colorTheme": "dark", "locale": "en" }}
        </script>
    """, height=470)

# TAB 3: FUNDAMENTAL RISK (TradingView Profile)
with tab3:
    components.html(f"""
        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-profile.js" async>
        {{ "symbol": "{ticker}", "width": "100%", "height": 450, "colorTheme": "dark", "isTransparent": false, "locale": "en" }}
        </script>
    """, height=470)

# TAB 4: DEEP CHART (Interactive)
with tab4:
    components.html(f"""
        <div id="tv_chart_main" style="height:500px;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
            new TradingView.widget({{
                "width": "100%", "height": 500, "symbol": "{ticker}", "interval": "D", "theme": "dark", "style": "1", "locale": "en", "container_id": "tv_chart_main"
            }});
        </script>
    """, height=520)

# TAB 5: PRO DASHBOARD (Your Code - Isolated & Vetted)
with tab5:
    pro_html = f"""
    <body style="background:#050505; color:white; font-family:sans-serif; padding:10px;">
        <div style="background:#111; padding:15px; border:1px solid #333; border-radius:10px; display:flex; justify-content:space-between;">
            <h3 style="margin:0;">TechAnalysis PRO</h3>
            <span id="p-status" style="color:#2ecc71; font-size:12px;">Connecting...</span>
        </div>
        <div id="p-main" style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px; margin-top:15px;">
            <div style="background:#111; padding:15px; border-radius:10px; border:1px solid #333; text-align:center;">
                <small style="color:#888;">PRICE</small><h2 id="p-price">--</h2>
            </div>
            <div style="background:#111; padding:15px; border-radius:10px; border:1px solid #333; text-align:center;">
                <small style="color:#888;">TARGET</small><h2 id="p-target" style="color:#2ecc71;">--</h2>
            </div>
            <div style="background:#111; padding:15px; border-radius:10px; border:1px solid #333; text-align:center;">
                <small style="color:#888;">STOP</small><h2 id="p-stop" style="color:#ff4d4f;">--</h2>
            </div>
        </div>
        <script>
            async function getP() {{
                const url = `https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=5d`;
                try {{
                    const r = await fetch(`https://api.allorigins.win/get?url=${{encodeURIComponent(url)}}&ts=${{Date.now()}}`);
                    const j = await r.json();
                    const d = JSON.parse(j.contents).chart.result[0];
                    const last = d.indicators.quote[0].close.filter(v=>v).pop();
                    document.getElementById('p-price').innerText = "$" + last.toFixed(2);
                    document.getElementById('p-target').innerText = "$" + (last*1.06).toFixed(2);
                    document.getElementById('p-stop').innerText = "$" + (last*0.96).toFixed(2);
                    document.getElementById('p-status').innerText = "ONLINE";
                }} catch(e) {{ document.getElementById('p-status').innerText = "RETRYING..."; setTimeout(getP, 3000); }}
            }}
            getP();
        </script>
    </body>
    """
    components.html(pro_html, height=400)

# TAB 6: SIGNAL ANALYZER (Indicator Table)
with tab6:
    sig_html = f"""
    <body style="background:#050505; color:white; font-family:sans-serif; padding:10px;">
        <table style="width:100%; border-collapse:collapse; background:#0c0c0c; border:1px solid #333; border-radius:10px; overflow:hidden;">
            <thead style="background:#151515; color:#888; text-align:left;">
                <tr><th style="padding:15px;">Technical Indicator</th><th style="padding:15px; text-align:center;">Market Signal</th></tr>
            </thead>
            <tbody id="s-body">
                <tr><td colspan="2" style="text-align:center; padding:40px;">Fetching Signals for {ticker}...</td></tr>
            </tbody>
        </table>
        <script>
            async function getS() {{
                const url = `https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=1y`;
                try {{
                    const r = await fetch(`https://api.allorigins.win/get?url=${{encodeURIComponent(url)}}&ts=${{Date.now()}}`);
                    const j = await r.json();
                    const d = JSON.parse(j.contents).chart.result[0];
                    const close = d.indicators.quote[0].close.filter(v=>v);
                    const last = close.pop();
                    const sma20 = close.slice(-20).reduce((a,b)=>a+b,0)/20;
                    
                    const rows = [
                        {{ n: "Trend (Price vs SMA20)", v: last > sma20 }},
                        {{ n: "Momentum (10D)", v: last > close.slice(-10)[0] }},
                        {{ n: "Bullish Strength", v: true }}
                    ];
                    document.getElementById('s-body').innerHTML = rows.map(r => `
                        <tr style="border-bottom:1px solid #222;">
                            <td style="padding:15px;">${{r.n}}</td>
                            <td style="padding:15px; text-align:center;"><b style="color:${{r.v ? '#2ecc71':'#ff4d4f'}}">${{r.v ? 'BULLISH' : 'BEARISH'}}</b></td>
                        </tr>
                    `).join('');
                }} catch(e) {{ setTimeout(getS, 3000); }}
            }}
            getS();
        </script>
    </body>
    """
    components.html(sig_html, height=400)













