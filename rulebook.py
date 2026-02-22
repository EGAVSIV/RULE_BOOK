import streamlit as st
from PIL import Image
import os

# ======================================
# PAGE CONFIG
# ======================================
st.set_page_config(
    page_title="My Trading Rulebook",
    page_icon="📊",
    layout="wide"
)

# ======================================
# CUSTOM CSS STYLING
# ======================================
st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #FFD700;
        text-align: center;
        margin-bottom: 30px;
    }

    .rule-header {
        font-size: 28px;
        font-weight: 700;
        color: #00E5FF;
        margin-top: 40px;
        margin-bottom: 10px;
    }

    .rule-box {
        background-color: #111111;
        padding: 25px;
        border-radius: 15px;
        border-left: 6px solid #FFD700;
        font-size: 18px;
        color: #FFFFFF;
        line-height: 1.8;
    }

    hr {
        margin-top: 40px;
        margin-bottom: 40px;
        border: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)

# ======================================
# TITLE
# ======================================
st.markdown('<div class="main-title">📊 MY TRADING RULEBOOK</div>', unsafe_allow_html=True)

# ======================================
# DEFINE YOUR RULES HERE
# ======================================

rules = [
    {
        "title": "RULE 1 - Trend Confirmation",
        "description": [
            "Trade only in direction of Higher Timeframe Trend",
            "15m must align with 1H",
            "ADX > 25",
            "Avoid sideways market"
        ],
        "image": "images/rule1.png"
    },
    {
        "title": "RULE 2 - Pullback Entry",
        "description": [
            "Wait for pullback to 20 EMA",
            "RSI bounce from 40-50 zone",
            "MACD crossover confirmation",
            "Volume increase required"
        ],
        "image": "images/rule2.png"
    },
    {
        "title": "RULE 3 - Risk Management",
        "description": [
            "Risk only 1% per trade",
            "Minimum RR = 1:2",
            "Move SL to BE after 1R",
            "Never average losing trades"
        ],
        "image": "images/rule3.png"
    }
]

# ======================================
# DISPLAY RULES
# ======================================

for rule in rules:

    # Rule Header
    st.markdown(f'<div class="rule-header">{rule["title"]}</div>', unsafe_allow_html=True)

    # Rule Box Start
    st.markdown('<div class="rule-box">', unsafe_allow_html=True)

    # Bullet Points (Each On New Line Properly)
    for point in rule["description"]:
        st.markdown(f"• {point}")

    # Rule Box End
    st.markdown('</div>', unsafe_allow_html=True)

    # Display Image If Exists
    if os.path.exists(rule["image"]):
        image = Image.open(rule["image"])
        st.image(image, use_container_width=True)
    else:
        st.warning(f"⚠ Image not found: {rule['image']}")

    st.markdown("<hr>", unsafe_allow_html=True)
