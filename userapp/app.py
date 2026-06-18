from pathlib import Path
import streamlit as st

#Navigation only
html_content = (Path(__file__).parent / "assets/xavier_erd_panel.html").read_text()
st.components.v1.html(html_content, height=750, scrolling=False)

st.set_page_config(page_title="LIMS", layout="wide")

main_page = st.Page ("pages/main_page.py", title="Main Page")
page2 = st.Page("pages/ingest_data.py", title="Ingest")
page3 = st.Page("pages/query_data.py", title="Query")
page4 = st.Page("pages/data_dictionary.py", title="Data Dictionary")
pg = st.navigation([main_page, page2, page3, page4])

pg.run()



