import streamlit as st

st.title("Voice-Based Concept Understanding Analyzer")

st.write("Welcome to the Voice-Based Concept Understanding Analyzer Project.")

uploaded_file = st.file_uploader("Upload an Audio File", type=["wav", "mp3"])

if uploaded_file:
    st.success("Audio uploaded successfully!")