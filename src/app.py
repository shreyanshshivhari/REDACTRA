import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from pipeline.guard_pipeline import analyze_prompt

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="REDACTRA | Security",
    page_icon="🛡️",
    layout="centered", 
    initial_sidebar_state="collapsed"
)

import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()
bg_image = get_base64_image("image.jpeg")

st.markdown(f"""
<style>

    /* -------- MAIN BACKGROUND WITH IMAGE -------- */
    .stApp {{
        background: linear-gradient(
            rgba(0, 0, 0, 0.85),
            rgba(0, 0, 0, 0.95)
        ),
        url("data:image/png;base64,{bg_image}");
        
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #f5f5f5;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    /* -------- HEADER -------- */
    .header-container {{
        text-align: center;
        padding-bottom: 2rem;
        margin-bottom: 2rem;
        border-bottom: 1px solid #dc2626;
        backdrop-filter: blur(6px);
    }}

    .main-title {{
        font-size: 2.5rem;
        font-weight: 900;
        color: #ef4444;
        letter-spacing: 1px;
    }}

    .sub-title {{
        font-size: 1rem;
        color: #d1d5db;
    }}

    /* -------- INPUT BOX (RED GLASS EFFECT) -------- */
    div[data-baseweb="textarea"] > div {{
        background: rgba(127, 29, 29, 0.7) !important;
        border: 1px solid #ef4444 !important;
        border-radius: 10px !important;
        backdrop-filter: blur(8px);
    }}

    textarea {{
        color: #ffffff !important;
    }}

    /* -------- RESULT CARDS -------- */
    .minimal-card {{
        background: rgba(10, 10, 10, 0.75);
        backdrop-filter: blur(10px);
        color: #f8fafc;
        padding: 1.5rem;
        border-radius: 14px;
        border: 1px solid #dc2626;
        box-shadow: 0 0 15px rgba(239, 68, 68, 0.25);
        margin-bottom: 1rem;
    }}

    .card-label {{
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #ef4444;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }}

    /* -------- BADGES -------- */
    .badge {{
        display: inline-block;
        padding: 0.4rem 0.9rem;
        border-radius: 9999px;
        font-size: 0.9rem;
        font-weight: 700;
    }}

    .badge-safe {{ background-color: #052e16; color: #bbf7d0; border: 1px solid #22c55e; }}
    .badge-danger {{ background-color: #7f1d1d; color: #fecaca; border: 1px solid #ef4444; }}
    .badge-warn {{ background-color: #78350f; color: #fde68a; border: 1px solid #f59e0b; }}
    .badge-info {{ background-color: #111827; color: #93c5fd; border: 1px solid #3b82f6; }}

    /* -------- BUTTON -------- */
    button[kind="primary"] {{
        background-color: #dc2626 !important;
        border-radius: 8px !important;
        font-weight: 700;
        border: none;
    }}

    button[kind="primary"]:hover {{
        background-color: #b91c1c !important;
    }}

</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown("""
<div class="header-container">
    <div class="main-title">🛡️ REDACTRA</div>
    <div class="sub-title">Real-time prompt threat detection & redaction</div>
</div>
""", unsafe_allow_html=True)

# ------------------ INPUT ------------------
user_input = st.text_area("Enter prompt for security analysis:", height=120, placeholder="Type or paste your prompt here...")

# ------------------ ANALYZE ------------------
col_btn, _ = st.columns([1, 5])
with col_btn:
    analyze_clicked = st.button("Analyze Prompt", type="primary", use_container_width=True)

if analyze_clicked:
    if user_input.strip() == "":
        st.info("Please enter a prompt to begin the scan.")
    else:
        with st.spinner("Scanning for threats..."):
            result = analyze_prompt(user_input)

        st.write("") 

        # Top Row
        col1, col2 = st.columns(2)

        # -------- Sensitive Data --------
        with col1:
            st.markdown('<div class="minimal-card"><div class="card-label">Sensitive Data</div>', unsafe_allow_html=True)
            if result.get("sensitive_data"):
                st.markdown('<span class="badge badge-danger">⚠️ Detected</span>', unsafe_allow_html=True)
                st.write("")
                for item in result["sensitive_data"]:
                    st.markdown(f"`{item}`")
            else:
                st.markdown('<span class="badge badge-safe">✓ Clean</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # -------- Jailbreak Attempt --------
        with col2:
            st.markdown('<div class="minimal-card"><div class="card-label">Jailbreak Analysis</div>', unsafe_allow_html=True)
            if result.get("jailbreak"):
                st.markdown('<span class="badge badge-danger">🚨 Jailbreak Attempt</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="badge badge-safe">✓ No attempt detected</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Bottom Row
        col3, col4 = st.columns(2)

        # -------- Intent --------
        with col3:
            intent_data = result.get("intent", "UNKNOWN")
            
            # Handle both String and Dictionary formats safely
            if isinstance(intent_data, dict):
                intent_label = str(intent_data.get("label", "UNKNOWN"))
                conf_text = f" ({intent_data.get('confidence', '')})"
            else:
                intent_label = str(intent_data)
                conf_text = ""
            
            st.markdown('<div class="minimal-card"><div class="card-label">Identified Intent</div>', unsafe_allow_html=True)
            
            if intent_label.upper() == "HARMFUL":
                st.markdown(f'<span class="badge badge-warn">Harmful{conf_text}</span>', unsafe_allow_html=True)
            else:
                st.markdown(f'<span class="badge badge-info">{intent_label}{conf_text}</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # -------- Action --------
        with col4:
            action = str(result.get("action", "ALLOW")).upper()
            
            st.markdown('<div class="minimal-card"><div class="card-label">System Action</div>', unsafe_allow_html=True)
            
            if action == "BLOCK":
                st.markdown('<span class="badge badge-danger">⛔ BLOCK</span>', unsafe_allow_html=True)
            elif action == "REVIEW":
                st.markdown('<span class="badge badge-warn">⚠️ REVIEW</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="badge badge-safe">✓ ALLOW</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ------------------ FOOTER ------------------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #7f1d1d; font-size: 0.8rem; margin-top: 2rem; font-weight: 500;">
    REDACTRA • Monitoring Active
</div>
""", unsafe_allow_html=True)
