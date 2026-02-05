import streamlit as st
import streamlit.components.v1 as components

# 1. Pagina Configuratie
st.set_page_config(page_title="SST SMART TERMINAL", layout="wide")

# API Keys (Let op: Finnhub gratis tier heeft limieten per minuut)
FIN_KEY = "d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0"

# 2. CSS voor een fullscreen ervaring en de indicator badges
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .block-container { padding: 0px !important; background-color: #050608; }
    iframe { border: none !important; width: 100% !important; height: 110vh !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. De Terminal Code
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
        button:hover {{ background: #1d4ed8; }}
        
        .stats-container {{ display: grid; grid-template-columns: 1fr 2fr; gap: 20px; margin-bottom: 20px; }}
        .card {{ background: #0d1117; border: 1px solid #30363d; padding: 20px; border-radius: 12px; text-align: center; }}
        .score-value {{ font-size: 3.5rem; font-weight: 900; margin: 5px 0; }}
        .advice-box {{ display: flex; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: bold; text-transform: uppercase; border: 2px solid #30363d; }}
        
        /* Indicator Panel Styles */
        .indicator-panel {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin-bottom: 20px; }}
        .ind-card {{ 
            background: #0d1117; border: 2px solid #30363d; padding: 10px; border-radius: 8px; 
            text-align: center; font-size: 0.8rem; font-weight: bold; transition: 0.3s;
        }}
        .status-green {{ background: rgba(63, 185, 80, 0.2); border-color: #3fb950; color: #3fb950; }}
        .status-blue {{ background: rgba(37, 99, 235, 0.2); border-color: #2563eb; color: #2563eb; }}
        .status-red {{ background: rgba(248, 81, 73, 0.2); border-color: #f85149; color: #f85149; }}
        
        #chart_container {{ height: 600px; border-radius: 15px; overflow: hidden; border: 1px solid #30363d; }}
    </style>
</head>
<body>

    <div class="header-row">
        <input id="tickerInput" value="NVDA" placeholder="Voer ticker in...">
        <button onclick="updateTerminal()">UPDATE ANALYSE</button>
    </div>

    <div class="stats-container">
        <div class="card">
            <div style="color: #8b949e; font-size: 0.8rem; font-weight: bold;">AI MOMENTUM SCORE</div>
            <div id="scoreDisplay" class="score-value">--</div>
        </div>
        <div id="adviceDisplay" class="card advice-box">LADEN...</div>
    </div>

    <div class="indicator-panel" id="indicatorPanel">
        <div id="ind-rsi" class="ind-card">RSI (14)</div>
        <div id="ind-stoch" class="ind-card">STOCHASTIC</div>
        <div id="ind-macd" class="ind-card">MACD</div>
        <div id="ind-ema" class="ind-card">EMA (20/50/200)</div>
        <div id="ind-bb" class="ind-card">BOLLINGER BANDS</div>
    </div>

    <div id="chart_container"></div>

    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>
        async function fetchIndicator(symbol, indicator, params="") {{
            const url = `https://finnhub.io/api/v1/indicator?symbol=${{symbol}}&resolution=D&token={FIN_KEY}&indicator=${{indicator}}${{params}}`;
            const res = await fetch(url);
            return await res.json();
        }}

        async function updateTerminal() {{
            const symbol = document.getElementById('tickerInput').value.toUpperCase();
            
            try {{
                // 1. Prijsdata voor de hoofdscore
                const quoteRes = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{symbol}}&token={FIN_KEY}`);
                const quote = await quoteRes.json();
                
                if (!quote.c) return alert("Ticker niet gevonden");

                // Update Score & Advice
                const rawScore = Math.round(50 + (quote.dp * 12));
                const finalScore = Math.min(Math.max(rawScore, 5), 99);
                document.getElementById('scoreDisplay').innerText = finalScore;
                
                // 2. INDICATOREN BEREKENEN
                
                // RSI 14
                const rsiData = await fetchIndicator(symbol, "rsi", "&timeperiod=14");
                const lastRSI = rsiData.rsi[rsiData.rsi.length - 1];
                const rsiEl = document.getElementById('ind-rsi');
                rsiEl.className = "ind-card " + (lastRSI >= 30 && lastRSI <= 65 ? "status-green" : "");
                rsiEl.innerHTML = `RSI: ${{lastRSI.toFixed(1)}}`;

                // Stochastic 14,3,3
                const stochData = await fetchIndicator(symbol, "stoch", "&fastkperiod=14&slowkperiod=3&slowdperiod=3");
                const k = stochData.slowk;
                const d = stochData.slowd;
                const lastK = k[k.length - 1];
                const prevK = k[k.length - 2];
                const lastD = d[d.length - 1];
                const stochEl = document.getElementById('ind-stoch');
                
                if (lastK > lastD && lastK > prevK) {{
                    stochEl.className = "ind-card status-green";
                }} else if (lastK > lastD && lastK <= prevK) {{
                    stochEl.className = "ind-card status-blue";
                }} else if (lastK < lastD) {{
                    stochEl.className = "ind-card status-red";
                }}
                stochEl.innerHTML = `STOCH K: ${{lastK.toFixed(1)}}`;

                // MACD
                const macdData = await fetchIndicator(symbol, "macd");
                const lastMACD = macdData.macd[macdData.macd.length - 1];
                const lastSignal = macdData.macdSignal[macdData.macdSignal.length - 1];
                const macdEl = document.getElementById('ind-macd');
                macdEl.className = "ind-card " + (lastMACD > lastSignal ? "status-green" : "");
                macdEl.innerHTML = `MACD: ${{lastMACD > lastSignal ? 'BULLISH' : 'BEARISH'}}`;

                // EMA 20, 50, 200
                const ema20 = await fetchIndicator(symbol, "ema", "&timeperiod=20");
                const ema50 = await fetchIndicator(symbol, "ema", "&timeperiod=50");
                const ema200 = await fetchIndicator(symbol, "ema", "&timeperiod=200");
                const p = quote.c;
                const e20 = ema20.ema[ema20.ema.length-1];
                const e50 = ema50.ema[ema50.ema.length-1];
                const e200 = ema200.ema[ema200.ema.length-1];
                const emaEl = document.getElementById('ind-ema');
                emaEl.className = "ind-card " + (p > e20 && p > e50 && p > e200 ? "status-green" : "");
                emaEl.innerHTML = `EMA CLOUD: ${{p > e20 ? 'UP' : 'DOWN'}}`;

                // Bollinger Bands
                const bbData = await fetchIndicator(symbol, "bbands", "&timeperiod=20");
                const upperBand = bbData.upperband[bbData.upperband.length - 1];
                const bbEl = document.getElementById('ind-bb');
                bbEl.className = "ind-card " + (p > upperBand ? "status-green" : "");
                bbEl.innerHTML = `BOLLINGER: ${{p > upperBand ? 'BREAKOUT' : 'INSIDE'}}`;

                // 3. TradingView Chart laden
                new TradingView.widget({{
                    "autosize": true, "symbol": symbol, "interval": "D", "theme": "dark", "container_id": "chart_container",
                    "style": "1", "locale": "nl", "enable_publishing": false, "hide_top_toolbar": false
                }});

            }} catch (e) {{ console.error(e); }}
        }}
        window.onload = updateTerminal;
    </script>
</body>
</html>
"""

components.html(terminal_html, height=1200)


































