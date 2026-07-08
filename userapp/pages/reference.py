import streamlit as st
from pathlib import Path

html_content = (Path(__file__).parent.parent / "assets" / "xavier_erd_panel.html").read_text()
st.components.v1.html(html_content, height=800, scrolling=True)
