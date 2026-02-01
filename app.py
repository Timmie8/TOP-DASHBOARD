import streamlit as st
import streamlit.components.v1 as components

# --- 1. PAGINA CONFIGURATIE ---
st.set_page_config(page_title="SST ARCHITECT TERMINAL", layout="wide", initial_sidebar_state="expanded")

# --- 2. DYNAMISCHE TICKER INPUT ---
st.sidebar.header("🕹️ Terminal Controls")

# Vrij invoerveld voor de gebruiker
user_input = st.sidebar.text_input("Voer Ticker in (bijv. AAPL of NASDAQ:TSLA)", "NVDA").upper()

# Zorg voor het juiste formaat voor TradingView (Exchange:Symbol)
if ":" not in user_input:
    # Default naar NASDAQ voor gemak, maar de widget zoekt vaak zelf ook goed
    selected_ticker = f"NASDAQ:{user_input}"
else:
    selected_ticker = user_input

# Schoon symbool voor de Architect API
clean_ticker = user_input.split(':')[-1]

# --- 3. GLOBALE STYLING (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: #050505; }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: #0d1117;
        border-radius: 8px 8px 0px 0px;
        color: #8b949e;
        border: 1px solid #30363d;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #238636 !important;
        color: white !important;
    }
    /* Zorg dat de iframe containers geen scrollbars geven */
    iframe { border: none !important; border-radius: 15px; overflow: hidden !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DE TOOLS ---

def render_sst_architect(ticker):
    architect_html = f"""
    <div style="background: #0d1117; padding: 25px; border-radius: 15px; border: 1px solid #30363d; font-family: 'Inter', sans-serif; color: white;">
        <h2 style="margin: 0;">SST <span style="color: #2f81f7;">ARCHITECT</span>: {ticker}</h2>
        <div style="display: flex; gap: 20px; margin-top: 20px;">
            <div style="flex: 1; background: #161b22; padding: 20px; border-radius: 12px; text-align: center; border: 1px solid #30363d;">
                <span style="color: #8b949e; font-size: 0.8rem;">AI SIGNAL</span>
                <div style="font-size: 2.5rem; font-weight: 900; color: #3fb950; margin: 10px 0;">READY</div>
            </div>
            <div style="flex: 2; background: #161b22; padding: 20px; border-radius: 12px; border: 1px solid #30363d;">
                <span style="color: #8b949e; font-size: 0.8rem;">SYSTEM STATUS</span>
                <p style="margin: 10px 0; font-size: 0.9rem; line-height: 1.4;">Terminal is gekoppeld aan <b>{ticker}</b>. Gebruik de MARKET METERS tab voor technische bevestiging.</p>
            </div>
        </div>
    </div>
    """
    components.html(architect_html, height=250)

def render_massive_gauge(ticker_symbol):
    """Extra grote Gauge om afkap-problemen te voorkomen"""
    # We zetten de height in de widget op 100% en in de component op 650px
    html_gauge = f"""
    <div class="tradingview-widget-container" style="width: 100%; height: 600px; margin: 0 auto;">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
      {{
        "interval": "1D",
        "width": "100%",
        "isTransparent": false,
        "height": "100%",
        "symbol": "{ticker_symbol}",
        "showIntervalTabs": true,
        "displayMode": "regular",
        "locale": "nl",
        "colorTheme": "dark"
      }}
      </script>
    </div>
    """
    # De component hoogte staat nu op 650, ruim voldoende voor de hele cirkel + tekst
    components.html(html_gauge, height=650)

# --- 5. DASHBOARD LAYOUT ---

st.title(f"🚀 SST TERMINAL | {user_input}")

tab_research, tab_technical, tab_scanner = st.tabs(["🛡️ ARCHITECT", "📊 MARKET METERS", "🔍 SCANNER"])

with tab_research:
    render_sst_architect(clean_ticker)

with tab_technical:
    st.subheader(f"Technical Sentiment: {user_input}")
    # Hier roepen we de nieuwe grote gauge aan
    render_massive_gauge(selected_ticker)
    
    st.divider()
    
    st.subheader("Structure Chart")
    components.html(f"""
        <div style="height: 600px; border-radius: 12px; overflow: hidden; border: 1px solid #30363d;">
            <div id="tv-chart" style="height:100%;"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
            <script type="text/javascript">
                new TradingView.widget({{
                    "autosize": true, "symbol": "{selected_ticker}", "interval": "D", "theme": "dark", "container_id": "tv-chart"
                }});
            </script>
        </div>
    """, height=620)

with tab_scanner:
    components.html('<iframe src="https://ai-stock-dashboard-qocavy6wajfcfgzjxaszb7.streamlit.app//?embed=true" style="width: 100%; height: 800px; border: none;"></iframe>', height=820)



