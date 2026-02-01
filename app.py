import streamlit as st
import streamlit.components.v1 as components

# --- 1. FULL SCREEN CONFIG ---
st.set_page_config(page_title="SST MASTER TERMINAL", layout="wide")

# Sidebar for the global ticker
st.sidebar.header("🕹️ TERMINAL CONTROLS")
ticker = st.sidebar.text_input("SET GLOBAL TICKER", "NVDA").upper()

# --- 2. RAW CODE REPOSITORY ---
# Plak hier je EXACTE werkende codes tussen de triples quotes. 
# Ik heb de variabelen {ticker} toegevoegd zodat ze meebewegen.

code_tab_5 = f"""
<!DOCTYPE html>
<html>
<body style="background:#050505; color:white;">
    <h1 style="color:#2ecc71;">PRO DASHBOARD: {ticker}</h1>
    </body>
</html>
"""

code_tab_6 = f"""
<!DOCTYPE html>
<html>
<body style="background:#050505; color:white;">
    <h1 style="color:#2ecc71;">SIGNAL ANALYZER: {ticker}</h1>
    </body>
</html>
"""

# --- 3. THE INTERFACE ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; }
    /* Verberg Streamlit rommel voor een cleaner look */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

tabs = st.tabs(["🚀 ARCHITECT AI", "📊 MARKET METERS", "🛡️ RISK SCANNER", "🔍 DEEP SCANNER", "⚡ PRO DASHBOARD", "🎯 SIGNAL ANALYZER"])

# Gebruik een directe 'RAW' injectie voor jouw codes
with tabs[4]: # Pro Dashboard
    # We gebruiken een extreem hoog iFrame en sturen de code 'as is'
    components.html(code_tab_5, height=800, scrolling=True)

with tabs[5]: # Signal Analyzer
    components.html(code_tab_6, height=800, scrolling=True)

# Voor de overige tabs (1 t/m 4) kun je tijdelijk placeholders of TradingView gebruiken
with tabs[0]:
    st.write(f"Architect AI is ready for {ticker}")














