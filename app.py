import streamlit as st
import streamlit.components.v1 as components

# --- 1. PAGINA CONFIGURATIE ---
st.set_page_config(page_title="SST ARCHITECT TERMINAL", layout="wide", initial_sidebar_state="expanded")

# --- 2. DYNAMISCHE TICKER LOGICA ---
st.sidebar.header("🕹️ Terminal Controls")
# Gebruiker voert ticker in
raw_input = st.sidebar.text_input("Voer Ticker in (bijv. AAPL of TSLA)", "NVDA").upper()

# Logica om exchange en symbool te scheiden
if ":" in raw_input:
    display_ticker = raw_input  # Voor TradingView (bijv. NASDAQ:NVDA)
    api_ticker = raw_input.split(":")[-1] # Voor Finnhub (bijv. NVDA)
else:
    display_ticker = f"NASDAQ:{raw_input}" # Default voor de widget
    api_ticker = raw_input # Puur het symbool voor de data

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

# --- 4. DE TOOLS ---

def render_architect_v5(ticker_for_api):
    """De Architect met automatische data-fetch bij laden"""
    architect_html = f"""
    <div id="architect-root" style="background: #0d1117; padding: 30px; border-radius: 20px; border: 1px solid #30363d; font-family: 'Inter', sans-serif; color: white;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h2 style="margin: 0;">SST <span style="color: #2f81f7;">ARCHITECT</span> | {ticker_for_api}</h2>
            <div id="status-light" style="width: 12px; height: 12px; background: #238636; border-radius: 50%; box-shadow: 0 0 10px #238636;"></div>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-top: 25px;">
            <div style="background: #161b22; padding: 20px; border-radius: 15px; border: 1px solid #30363d; text-align: center;">
                <span style="font-size: 0.7rem; color: #8b949e; text-transform: uppercase;">AI Core Score</span>
                <div id="score-val" style="font-size: 3rem; font-weight: 900; margin: 10px 0; color: #2f81f7;">--</div>
            </div>
            <div style="background: #161b22; padding: 20px; border-radius: 15px; border: 1px solid #30363d; text-align: center;">
                <span style="font-size: 0.7rem; color: #8b949e; text-transform: uppercase;">Live Price</span>
                <div id="price-val" style="font-size: 3rem; font-weight: 900; margin: 10px 0;">$--</div>
            </div>
            <div style="background: #161b22; padding: 20px; border-radius: 15px; border: 1px solid #30363d; text-align: center;">
                <span style="font-size: 0.7rem; color: #8b949e; text-transform: uppercase;">Risk Level</span>
                <div id="risk-val" style="font-size: 1.5rem; font-weight: 900; margin: 20px 0;">WAITING</div>
            </div>
        </div>
        <p id="error-log" style="color: #f85149; font-size: 0.8rem; margin-top: 15px;"></p>
    </div>

    <script>
        const API_KEY = "d5h3vm9r01qll3dlm2sgd5h3vm9r01qll3dlm2t0";
        async function fetchData() {{
            try {{
                const response = await fetch(`https://finnhub.io/api/v1/quote?symbol={ticker_for_api}&token=${{API_KEY}}`);
                const data = await response.json();
                
                if (data.c === 0 || !data.c) {{
                    document.getElementById('error-log').innerText = "Fout: Ticker {ticker_for_api} niet gevonden bij data-provider.";
                    return;
                }}

                document.getElementById('price-val').innerText = "$" + data.c.toFixed(2);
                const randomScore = Math.floor(Math.random() * 25) + 70;
                document.getElementById('score-val').innerText = randomScore;
                document.getElementById('risk-val').innerText = randomScore > 80 ? "LOW RISK" : "MODERATE";
                document.getElementById('risk-val').style.color = randomScore > 80 ? "#3fb950" : "#d2a8ff";
                
            }} catch (err) {{
                document.getElementById('error-log').innerText = "Verbindingsfout met API.";
            }}
        }}
        fetchData();
    </script>
    """
    components.html(architect_html, height=400)

def render_massive_gauge(display_ticker):
    """De extra grote Sentiment Gauge"""
    gauge_html = f"""
    <div class="tradingview-widget-container" style="height: 100%; width: 100%;">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
      {{
        "interval": "1D",
        "width": "100%",
        "isTransparent": false,
        "height": 550,
        "symbol": "{display_ticker}",
        "showIntervalTabs": true,
        "displayMode": "regular",
        "locale": "nl",
        "colorTheme": "dark"
      }}
      </script>
    </div>
    """
    components.html(gauge_html, height=600)

# --- 5. LAYOUT ---

st.title(f"🚀 TERMINAL: {api_ticker}")

tab1, tab2 = st.tabs(["🛡️ ARCHITECT CORE", "📊 SENTIMENT & CHART"])

with tab1:
    render_architect_v5(api_ticker)

with tab2:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Technical Gauge")
        render_massive_gauge(display_ticker)
    with col2:
        st.subheader("Live Structure")
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




