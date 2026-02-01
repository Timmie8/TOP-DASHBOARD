import streamlit as st
import streamlit.components.v1 as components

# 1. Pagina Configuratie
st.set_page_config(page_title="SST SMART TERMINAL", layout="wide")

# API Keys
FIN_KEY = "d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0"

# 2. CSS voor een fullscreen ervaring
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .block-container { padding: 0px !important; background-color: #050608; }
    iframe { border: none !important; width: 100% !important; height: 95vh !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. De Terminal Code
terminal_html = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ background-color: #050608; color: white; font-family: 'Inter', sans-serif; margin: 0; padding: 20px; overflow: hidden; }}
        .header-row {{ display: flex; gap: 15px; margin-bottom: 20px; align-items: center; }}
        input {{ background: #161b22; border: 1px solid #30363d; color: white; padding: 15px; border-radius: 10px; flex: 1; font-size: 16px; font-weight: bold; }}
        button {{ background: #2563eb; color: white; border: none; padding: 15px 30px; border-radius: 10px; cursor: pointer; font-weight: bold; transition: 0.2s; }}
        button:hover {{ background: #1d4ed8; }}
        .stats-container {{ display: grid; grid-template-columns: 1fr 2fr; gap: 20px; margin-bottom: 20px; }}
        .card {{ background: #0d1117; border: 1px solid #30363d; padding: 20px; border-radius: 12px; text-align: center; }}
        .score-value {{ font-size: 3.5rem; font-weight: 900; margin: 5px 0; }}
        .advice-box {{ display: flex; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: bold; text-transform: uppercase; border: 2px solid #30363d; }}
        #chart_container {{ height: calc(100vh - 250px); border-radius: 15px; overflow: hidden; border: 1px solid #30363d; }}
    </style>
</head>
<body>

    <div class="header-row">
        <input id="tickerInput" value="NVDA" placeholder="Voer ticker in (bijv. AAPL, BTCUSD)...">
        <button onclick="updateTerminal()">UPDATE CHART & SCORE</button>
    </div>

    <div class="stats-container">
        <div class="card">
            <div style="color: #8b949e; font-size: 0.8rem; font-weight: bold;">AI MOMENTUM SCORE</div>
            <div id="scoreDisplay" class="score-value">--</div>
        </div>
        <div id="adviceDisplay" class="card advice-box">
            WAITING FOR DATA
        </div>
    </div>

    <div id="chart_container"></div>

    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>
        async function updateTerminal() {{
            const symbol = document.getElementById('tickerInput').value.toUpperCase();
            
            try {{
                // 1. Haal Prijsdata op voor Score
                const response = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{symbol}}&token={FIN_KEY}`);
                const data = await response.json();
                
                if (data.c) {{
                    // Score berekening: Basis 50 + (dagelijkse verandering * multiplier)
                    const rawScore = Math.round(50 + (data.dp * 12));
                    const finalScore = Math.min(Math.max(rawScore, 5), 99);
                    
                    const scoreEl = document.getElementById('scoreDisplay');
                    const adviceEl = document.getElementById('adviceDisplay');
                    
                    scoreEl.innerText = finalScore;
                    
                    // Visuele feedback op basis van score
                    if (finalScore > 60) {{
                        scoreEl.style.color = "#3fb950";
                        adviceEl.innerText = "Bullish Momentum: Strong Buy";
                        adviceEl.style.borderColor = "#3fb950";
                        adviceEl.style.color = "#3fb950";
                    }} else if (finalScore < 40) {{
                        scoreEl.style.color = "#f85149";
                        adviceEl.innerText = "Bearish Trend: Avoid / Short";
                        adviceEl.style.borderColor = "#f85149";
                        adviceEl.style.color = "#f85149";
                    }} else {{
                        scoreEl.style.color = "#d29922";
                        adviceEl.innerText = "Neutral / Sideways Market";
                        adviceEl.style.borderColor = "#d29922";
                        adviceEl.style.color = "#d29922";
                    }}

                    // 2. Laad de TradingView Chart
                    new TradingView.widget({{
                        "autosize": true,
                        "symbol": symbol,
                        "interval": "D",
                        "timezone": "Etc/UTC",
                        "theme": "dark",
                        "style": "1",
                        "locale": "nl",
                        "toolbar_bg": "#f1f3f6",
                        "enable_publishing": false,
                        "hide_top_toolbar": false,
                        "save_image": false,
                        "container_id": "chart_container"
                    }});
                }} else {{
                    alert("Ticker niet gevonden. Probeer een andere.");
                }}
            }} catch (error) {{
                console.error("Fout:", error);
            }}
        }}

        // Start direct met NVDA bij laden
        window.onload = updateTerminal;
    </script>
</body>
</html>
"""

# Render de terminal
components.html(terminal_html, height=1000)

































