import streamlit as st
from pathlib import Path

html_content = ("../assets/xavier_erd_panel.html")
st.components.v1.html(html_content, height=750, scrolling=False)
