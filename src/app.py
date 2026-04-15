import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from pipeline.guard_pipeline import analyze_prompt

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="REDACTRA",
    page_icon="🛡️",
    layout="wide"
)

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
body {
    background-color: #0f172a;
    color: #e2e8f0;
}

/* Title */
.title {
    font-size: 36px;
    font-weight: bold;
    color: #38bdf8;
}

/* Panels */
.panel {
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
    background-color: #1e293b;
}

/* Status Colors */
.safe {
    border-left: 5px solid #22c55e;
}
.warn {
    border-left: 5px solid #facc15;
}
.danger {
    border-left: 5px solid #ef4444;
}
.info {
    border-left: 5px solid #38bdf8;
}

/* Input box */
textarea {
    background-color: #020617 !important;
    color: #e2e8f0 !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown('<div class="title">🛡️ REDACTRA Security Console</div>', unsafe_allow_html=True)
st.caption("Real-time prompt threat detection system")

st.markdown("---")

# ------------------ INPUT ------------------
user_input = st.text_area("💬 Enter Prompt", height=150)

# ------------------ ANALYZE ------------------
if st.button("⚡ Scan Prompt"):

    if user_input.strip() == "":
        st.warning("You opened a security console and typed nothing. Bold strategy.")
    else:
        with st.spinner("Scanning for threats..."):
            result = analyze_prompt(user_input)

        col1, col2 = st.columns(2)

        # -------- Sensitive --------
        with col1:
            if result["sensitive_data"]:
                st.markdown('<div class="panel danger"><b>⚠️ Sensitive Data Detected</b></div>', unsafe_allow_html=True)
                for item in result["sensitive_data"]:
                    st.code(f"{item['type']} → {item['value']}")
            else:
                st.markdown('<div class="panel safe">✅ No Sensitive Data</div>', unsafe_allow_html=True)

        # -------- Jailbreak --------
        with col2:
            if result["jailbreak"]:
                st.markdown('<div class="panel danger">🚨 Jailbreak Attempt</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="panel safe">✅ No Jailbreak</div>', unsafe_allow_html=True)

        st.markdown("---")

        col3, col4 = st.columns(2)

        # -------- Intent --------
        with col3:
            intent = result["intent"]
            if intent == "harmful":
                st.markdown(f'<div class="panel warn">🧠 Intent: {intent}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="panel info">🧠 Intent: {intent}</div>', unsafe_allow_html=True)

        # -------- Action --------
        with col4:
            action = result.get("action", "allow")

            if action == "block":
                st.markdown('<div class="panel danger">⛔ ACTION: BLOCK</div>', unsafe_allow_html=True)
            elif action == "warn":
                st.markdown('<div class="panel warn">⚠️ ACTION: WARN</div>', unsafe_allow_html=True)
            elif action == "redact":
                st.markdown('<div class="panel warn">🛡️ ACTION: REDACT</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="panel safe">✅ ACTION: ALLOW</div>', unsafe_allow_html=True)

# ------------------ FOOTER ------------------
st.markdown("---")
st.caption("REDACTRA • AI Security Layer • Monitoring Active")  