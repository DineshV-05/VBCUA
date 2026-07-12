import streamlit as st

from config import *

from components.navbar import navbar

from pages.home import home

st.set_page_config(

    page_title=PAGE_TITLE,

    page_icon=PAGE_ICON,

    layout="wide"

)

# Load CSS
def load_css():

    with open("styles/main.css") as f:

        st.markdown(

            f"<style>{f.read()}</style>",

            unsafe_allow_html=True

        )

load_css()

navbar()

home()