import streamlit as st


def footer():

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <hr>

    <center>

    <p style="
        color:#64748b;
        font-size:16px;
    ">
        ❤️ Built with <b>Python</b> |
        🎤 Whisper AI |
        🧠 Sentence-BERT |
        🤖 Gemini AI |
        📊 Streamlit
    </p>

    <p style="
        color:#94a3b8;
        font-size:14px;
    ">
        © 2026 Voice-Based Concept Understanding Analyzer
    </p>

    </center>
    """, unsafe_allow_html=True)