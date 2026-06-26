import streamlit as st
from pathlib import Path

html_content = (Path(__file__).parent / "assets/xavier_erd_panel.html").read_text()
st.components.v1.html(html_content, height=750, scrolling=False)
