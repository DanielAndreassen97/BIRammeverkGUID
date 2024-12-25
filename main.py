import streamlit as st
# Set page layout to wide
st.set_page_config(layout="wide")
# ---- PAGE SETUP ----

about_page = st.Page(
    page="pages/about.py",
    title="About",
    default=True
)

dataloadparameter_page = st.Page(
    page="pages/dataloadparameter.py",
    title="Data Load Parameters"
)

tablecolumnmapping_page = st.Page(
    page="pages/tablecolumnmapping.py",
    title="Table Column Mapping"
)


pg = st.navigation(
    {
    "Info": [about_page],
    "Config Tables": [dataloadparameter_page, tablecolumnmapping_page]
    }
)

st.logo("images/crayon-logo.png")
st.sidebar.text("Made by Daniel🚀")

pg.run()