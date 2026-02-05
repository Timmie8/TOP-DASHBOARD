import streamlit as st
import streamlit.components.v1 as components

# 1. Pagina Configuratie
st.set_page_config(page_title="SST SMART TERMINAL", layout="wide")

FIN_KEY = "d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0"

# 2. CSS voor styling en de nieuwe Alert Banner
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .block-container { padding: 0px !important; background-color: #050608; }
    iframe { border: none !important; width: 100% !important; height: 115vh !important; }
    </style>
    """, unsafe_allow_html=True)

terminal_html = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ background-color: #050608; color: white; font-family: 'Inter', sans-serif; margin: 0; padding: 20px; }}
        .header-row {{ display: flex; gap: 15px; margin-bottom: 20px; align-items: center; }}
        input {{ background: #161b22; border: 1px solid #30363d; color: white; padding: 15px; border-radius: 10px; flex: 1; font-size: 16px; font-weight: bold; }}
        button {{ background: #2563eb; color: white; border: none; padding: 15px 30px; border-radius: 10px; cursor: pointer; font-weight: bold; transition: 0.2s; }}
        
        /* Alert Banner */
        #superSignal {{ 
            display: none; background: linear-gradient(90deg, #d29922, #f1e05a); 
            color: black; padding: 15px; border-radius: 10px; text-align: center; 
            font-weight: 900; margin-bottom: 20px; font-size: 1.2rem;
            animation: pulse 2s infinite;
        }}
        @keyframes pulse {{ 0% {{ opacity: 0.8; }} 50% {{ opacity: 1; }} 100% {{ opacity: 0.8; }} }}

        .stats-container {{ display: grid; grid-template-columns: 1fr 2fr; gap: 20px; margin-bottom: 20px; }}
        .card {{ background: #0d1117; border: 1px solid #30363d; padding: 20px; border-radius: 12px; text-align: center; }}
        .score-value {{ font-size: 3.5rem; font-weight: 900; margin: 5px 0; }}
        .advice-box {{ display: flex; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: bold; text-transform: uppercase; border: 2px solid #30363d; }}
        
        .indicator-panel {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin-bottom: 20px; }}
        .ind-card {{ background: #0d1117; border: 2px solid #30363d; padding: 10px; border-radius: 8px; text-align: center; font-size: 0.8rem; font-weight: bold; }}
        .status-green {{ border-color: #3fb950; color: #3fb950; background: rgba(63, 185, 80, 0.1); }}
        .status-blue {{ border-color: #2563eb; color: #2563eb; background: rgba(37, 99, 235, 0.1); }}
        .status-red {{ border-color: #f85149; color: #f85149; background: rgba(248, 81, 73, 0.1); }}
        
        #chart_container {{ height: 550px; border-radius: 15px; overflow: hidden; border: 1px solid #30363d; }}
    </style>
</head>
<body>

    <div id="superSignal">🚀 CONFLUENCE DETECTED: ALL INDICATORS BULLISH 🚀</div>

    <div class="header-row">
        <input id="tickerInput" value="NVDA" placeholder="Ticker...">
        <button onclick="updateTerminal()">ANALYSEER</button>
    </div>

    <div class="stats-container">
        <div class="card"><div style="color: #8b949e; font-size: 0.8rem;">SCORE</div><div id="scoreDisplay" class="score-value">--</div></div>
        <div id="adviceDisplay" class="card advice-box">READY</div>
    </div>

    <div class="indicator-panel" id="indicatorPanel">
        <div id="ind-rsi" class="ind-card">RSI</div>
        <div id="ind-stoch" class="ind-card">STOCH</div>
        <div id="ind-macd" class="ind-card">MACD</div>
        <div id="ind-ema" class="ind-card">EMA CLOUD</div>
        <div id="ind-bb" class="ind-card">BB BREAKOUT</div>
    </div>

    <div id="chart_container"></div>

    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>
        async function fetchInd(s, i, p="") {{
            const r = await fetch(`https://finnhub.io/api/v1/indicator?symbol=${{s}}&resolution=D&token={FIN_KEY}&indicator=${{i}}${{p}}`);
            return await r.json();
        }}

        async function updateTerminal() {{
            const s = document.getElementById('tickerInput').value.toUpperCase();
            let greenCount = 0;
            document.getElementById('superSignal').style.display = 'none';

            try {{
                const qRes = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{s}}&token={FIN_KEY}`);
                const q = await qRes.json();
                
                // RSI logic
                const rsiD = await fetchInd(s, "rsi", "&timeperiod=14");
                const lastRSI = rsiD.rsi[rsiD.rsi.length-1];
                const rsiIsGreen = lastRSI >= 30 && lastRSI <= 65;
                document.getElementById('ind-rsi').className = "ind-card " + (rsiIsGreen ? "status-green" : "");
                if(rsiIsGreen) greenCount++;

                // Stoch logic
                const stD = await fetchInd(s, "stoch", "&fastkperiod=14&slowkperiod=3&slowdperiod=3");
                const lastK = stD.slowk[stD.slowk.length-1];
                const prevK = stD.slowk[stD.slowk.length-2];
                const lastD = stD.slowd[stD.slowd.length-1];
                const stochEl = document.getElementById('ind-stoch');
                if(lastK > lastD && lastK > prevK) {{ stochEl.className="ind-card status-green"; greenCount++; }}
                else if(lastK > lastD) {{ stochEl.className="ind-card status-blue"; }}
                else {{ stochEl.className="ind-card status-red"; }}

                // MACD logic
                const mD = await fetchInd(s, "macd");
                const mIsGreen = mD.macd[mD.macd.length-1] > mD.macdSignal[mD.macdSignal.length-1];
                document.getElementById('ind-macd').className = "ind-card " + (mIsGreen ? "status-green" : "");
                if(mIsGreen) greenCount++;

                // EMA logic
                const e20 = await fetchInd(s, "ema", "&timeperiod=20");
                const e50 = await fetchInd(s, "ema", "&timeperiod=50");
                const e200 = await fetchInd(s, "ema", "&timeperiod=200");
                const emaIsGreen = q.c > e20.ema[e20.ema.length-1] && q.c > e50.ema[e50.ema.length-1] && q.c > e200.ema[e200.ema.length-1];
                document.getElementById('ind-ema').className = "ind-card " + (emaIsGreen ? "status-green" : "");
                if(emaIsGreen) greenCount++;

                // BB logic
                const bbD = await fetchInd(s, "bbands", "&timeperiod=20");
                const bbIsGreen = q.c > bbD.upperband[bbD.upperband.length-1];
                document.getElementById('ind-bb').className = "ind-card " + (bbIsGreen ? "status-green" : "");
                if(bbIsGreen) greenCount++;

                // Final Super Signal Check
                if(greenCount === 5) {{ document.getElementById('superSignal').style.display = 'block'; }}

                new TradingView.widget({{ "autosize": true, "symbol": s, "interval": "D", "theme": "dark", "container_id": "chart_container" }});
            }} catch(e) {{ console.error(e); }}
        }}
        window.onload = updateTerminal;
    </script>
</body>
</html>
"""
components.html(terminal_html, height=1200)



































