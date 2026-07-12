import streamlit as st


def uploader():

    st.markdown("## 📚 Select Concept")

    concept = st.selectbox(
        "",
        [
            "Machine Learning",
            "Artificial Intelligence",
            "Cloud Computing",
            "DBMS"
        ]
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("## 🎧 Upload Your Explanation")

    audio = st.file_uploader(
        "",
        type=["wav", "mp3", "m4a"]
    )

    return concept, audio