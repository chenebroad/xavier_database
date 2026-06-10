import streamlit as st
import pandas as pd

st.title("LIMS Dashboard")

st.write("Use the sidebar to navigate:")
st.write("How to ingest data into the LIMS system")
st.write("How to query data in the LIMS system")
st.write("Consult the data dictionary to get a definition of the schema and the columns")

st.sidebar.markdown("Main page with instructions")
