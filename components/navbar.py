import streamlit as st

def navbar():

    st.sidebar.image(
        "https://img.icons8.com/fluency/96/artificial-intelligence.png",
        width=80
    )

    st.sidebar.title("VBCUA")

    st.sidebar.markdown("---")

    st.sidebar.success("🟢 AI System Ready")

    st.sidebar.markdown("### Navigation")

    st.sidebar.write("🏠 Home")

    st.sidebar.write("🎙 Analyze")

    st.sidebar.write("📄 Reports")

    st.sidebar.write("ℹ About")

    st.sidebar.markdown("---")

    st.sidebar.info("Version 1.0")