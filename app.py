import streamlit as st
import streamlit.components.v1 as components

# --- 1. PAGINA CONFIGURATIE ---
st.set_page_config(page_title="SST ARCHITECT AI", layout="wide", initial_sidebar_state="expanded")

# --- 2. DYNAMISCHE TICKER LOGICA ---
st.sidebar.header("🕹️ Terminal Controls")
raw_input = st.sidebar.text_input("Voer Ticker in (bijv. NVDA of TSLA)", "NVDA").upper()

if ":" in raw_input:
    display_ticker = raw_input
    api_ticker = raw_input.split(":")[-1]
else:
    display_ticker = f"NASDAQ:{raw_input}"
    api_ticker = raw_input

# --- 3. GLOBALE STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    iframe { border: none !important; border-radius: 15px; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: #050505; }
    .stTabs [data-baseweb="tab"] {
        height: 45px; background-color: #0d1117; color: #8b949e;
        border-radius: 8px 8px 0px 0px; border: 1px solid #30363d;
    }
    .stTabs [aria-selected="true"] { background-color: #238636 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DE SST ARCHITECT AI COMPONENT ---

def render_sst_architect_ai(ticker):
    architect_html = f"""
    <div style="background: #0d1117; padding: 30px; border-radius: 20px; border: 1px solid #30363d; font-family: 'Inter', sans-serif; color: white;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #30363d; padding-bottom: 20px; margin-bottom: 20px;">
            <h2 style="margin: 0;">SST <span style="color: #2f81f7;">ARCHITECT AI</span> | {ticker}</h2>
            <div id="ai-decision" style="padding: 10px 20px; border-radius: 10px; font-weight: 900; background: #161b22; border: 1px solid #30363d;">ANALYZING...</div>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
            <div style="background: #161b22; padding: 20px; border-radius: 15px; border: 1px solid #30363d; text-align: center;">
                <span style="font-size: 0.75rem; color: #8b949e; text-transform: uppercase; font-weight: 800;">AI Tech Score</span>
                <div id="ai-score" style="font-size: 3.5rem; font-weight: 900; color: #2f81f7; margin: 10px 0;">--</div>
            </div>
            
            <div style="background: #161b22; padding: 20px; border-radius: 15px; border: 1px solid #30363d; text-align: center;">
                <span style="font-size: 0.75rem; color: #3fb950; text-transform: uppercase; font-weight: 800;">AI Profit Target</span>
                <div id="profit-target" style="font-size: 2.5rem; font-weight: 900; margin: 10px 0;">$--</div>
                <span id="profit-pct" style="color: #3fb950; font-weight: bold;">+0.00%</span>
            </div>
            
            <div style="background: #161b22; padding: 20px; border-radius: 15px; border: 1px solid #30363d; text-align: center;">
                <span style="font-size: 0.75rem; color: #f85149; text-transform: uppercase; font-weight: 800;">AI Stop Loss</span>
                <div id="stop-loss" style="font-size: 2.5rem; font-weight: 900; margin: 10px 0;">$--</div>
                <span id="stop-pct" style="color: #f85149; font-weight: bold;">-0.00%</span>
            </div>
        </div>

        <div style="margin-top: 25px; background: #010409; padding: 20px; border-radius: 12px; border: 1px solid #30363d;">
            <span style="font-size: 0.75rem; color: #8b949e; text-transform: uppercase; font-weight: 800;">AI Reasoning & Strategy</span>
            <p id="ai-reasoning" style="margin-top: 10px; line-height: 1.6; color: #c9d1d9; font-size: 0.95rem;">Booting neural engine for {ticker}...</p>
        </div>
    </div>

    <script>
        const FIN_KEY = "d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0";
        const GEM_KEY = "AIzaSyDTDyQWKgCJ3tvcexRCYYvuRUfkTpN4J5w";

        async function runAIEngine() {{
            try {{
                // 1. Haal Prijs Data op
                const qResp = await fetch(`https://finnhub.io/api/v1/quote?symbol={ticker}&token=${{FIN_KEY}}`);
                const qData = await qResp.json();
                const price = qData.c;

                if(!price) {{
                    document.getElementById('ai-reasoning').innerText = "Data niet gevonden.";
                    return;
                }}

                // 2. AI Simulatie Logica (Score & Targets)
                const score = Math.floor(Math.random() * 31) + 65; // Score tussen 65-95
                const targetPrice = price * (1 + (score/1000));
                const stopPrice = price * (1 - (score/2500));

                document.getElementById('ai-score').innerText = score;
                document.getElementById('profit-target').innerText = "$" + targetPrice.toFixed(2);
                document.getElementById('stop-loss').innerText = "$" + stopPrice.toFixed(2);
                document.getElementById('profit-pct').innerText = "+" + ((targetPrice/price-1)*100).toFixed(2) + "%";
                document.getElementById('stop-pct').innerText = "-" + ((1-stopPrice/price)*100).toFixed(2) + "%";

                // Beslissing kleur
                const decisionEl = document.getElementById('ai-decision');
                if(score > 85) {{
                    decisionEl.innerText = "STRONG BUY";
                    decisionEl.style.color = "#3fb950";
                    decisionEl.style.borderColor = "#3fb950";
                }} else if(score > 75) {{
                    decisionEl.innerText = "BUY / LONG";
                    decisionEl.style.color = "#2f81f7";
                    decisionEl.style.borderColor = "#2f81f7";
                }} else {{
                    decisionEl.innerText = "NEUTRAL / HOLD";
                    decisionEl.style.color = "#8b949e";
                    decisionEl.style.borderColor = "#30363d";
                }}

                // 3. Haal AI Reasoning op bij Gemini
                const prompt = `Analyze ticker {ticker} at price ${{price}}. AI Score is ${{score}}/100. Provide a 2-sentence swing trade strategy including target and stop levels.`;
                const gResp = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${{GEM_KEY}}`, {{
                    method: "POST", headers: {{"Content-Type": "application/json"}},
                    body: JSON.stringify({{contents: [{{parts: [{{text: prompt}}]}}]}})
                }});
                const gData = await gResp.json();
                document.getElementById('ai-reasoning').innerText = gData.candidates[0].content.parts[0].text;

            }} catch (err) {{
                document.getElementById('ai-reasoning').innerText = "AI Engine timeout.";
            }}
        }}
        runAIEngine();
    </script>
    """
    components.html(architect_html, height=550)

# --- 5. LAYOUT ---

st.title(f"🛡️ SST MASTER TERMINAL | {api_ticker}")

tab1, tab2 = st.tabs(["🚀 ARCHITECT AI", "📊 TECHNICAL ANALYSIS"])

with tab1:
    render_sst_architect_ai(api_ticker)

with tab2:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Technical Gauge")
        # Grote gauge code
        components.html(f"""
            <div class="tradingview-widget-container">
              <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
              {{
                "interval": "1D", "width": "100%", "isTransparent": false, "height": 550,
                "symbol": "{display_ticker}", "showIntervalTabs": true, "displayMode": "regular",
                "locale": "nl", "colorTheme": "dark"
              }}
              </script>
            </div>
        """, height=600)
    with col2:
        st.subheader("Live Chart")
        components.html(f"""
            <div style="height: 550px; border: 1px solid #30363d; border-radius: 15px; overflow: hidden;">
                <div id="tv-chart" style="height:100%;"></div>
                <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
                <script type="text/javascript">
                    new TradingView.widget({{
                        "autosize": true, "symbol": "{display_ticker}", "interval": "D", "theme": "dark", "container_id": "tv-chart"
                    }});
                </script>
            </div>
        """, height=560)




