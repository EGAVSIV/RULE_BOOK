import streamlit as st
from PIL import Image
import os

# ==========================
# PAGE CONFIG
# ==========================
st.set_page_config(
    page_title="My Trading Rulebook",
    layout="wide",
    page_icon="📊"
)

# ==========================
# CUSTOM CSS FOR BEAUTIFUL DESIGN
# ==========================
st.markdown("""
    <style>
        .main-title {
            font-size: 40px;
            font-weight: bold;
            color: #FFD700;
            text-align: center;
        }
        .rule-header {
            font-size: 26px;
            font-weight: 700;
            color: #00E5FF;
            margin-top: 30px;
        }
        .rule-box {
            background-color: #1E1E1E;
            padding: 20px;
            border-radius: 12px;
            border-left: 6px solid #FFD700;
            margin-bottom: 10px;
            font-size: 18px;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================
# TITLE
# ==========================
st.markdown('<div class="main-title">📊 MY TRADING RULEBOOK</div>', unsafe_allow_html=True)
st.write("")

# ==========================
# YOUR RULES (WRITE IN PYTHON)
# ==========================

rules = [
    {
        "title": "RULE 1 - Trend Confirmation",
        "description": """
        • Trade only in direction of Higher Timeframe Trend  
        • Buy on Every DIPs 
        • RD and FIB Retracement  
        • Use EMA 20 and 50 Reversal  
        """,
        "image": "images/rule1.png"
    },
    {
        "title": "RULE 2 - Pullback Entry",
        "description": """
        • Wait for pullback to 20 EMA  
        • RSI must bounce from 40-50 zone  
        • MACD crossover confirmation  
        • Volume increase
        """,
        "image": "images/rule2.png"
    },
    {
        "title": "RULE 3 - Risk Management",
        "description": """
        • Risk only 1% per trade  
        • RR minimum 1:2  
        • Move SL to BE after 1R  
        • Never average losses
        """,
        "image": "images/rule3.png"
    }
]

# ==========================
# DISPLAY RULES
# ==========================

for rule in rules:

    st.markdown(f'<div class="rule-header">{rule["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="rule-box">{rule["description"]}</div>', unsafe_allow_html=True)

    # Load image if exists
    if os.path.exists(rule["image"]):
        image = Image.open(rule["image"])
        st.image(image, use_column_width=True)
    else:
        st.warning(f"Image not found: {rule['image']}")

    st.markdown("---")
