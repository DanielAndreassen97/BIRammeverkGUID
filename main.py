import streamlit as st
from streamlit.runtime.scriptrunner_utils.script_run_context import (
    get_script_run_ctx,
)
import json
import os


def authenticate(username: str, password: str, cred_file: str = "users.json") -> bool:
    """Simple authentication against a JSON file of credentials."""
    if not os.path.exists(cred_file):
        return False
    try:
        with open(cred_file, "r") as f:
            creds = json.load(f)
    except Exception:
        return False

    stored_pw = creds.get(username)
    return stored_pw == password

# Exit with a helpful message if run directly without `streamlit run`
if get_script_run_ctx(suppress_warning=True) is None:
    raise RuntimeError("Please run this app using 'streamlit run main.py'")

# Set page layout to wide
st.set_page_config(layout="wide")

# ---- PAGE SETUP ----

if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Invalid username or password")
    st.stop()

if st.sidebar.button("Logout"):
    st.session_state["authenticated"] = False
    st.rerun()

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
        "Config Tables": [dataloadparameter_page, tablecolumnmapping_page],
    }
)

st.logo("images/crayon-logo.png")
st.sidebar.text("Made by Daniel🚀")

pg.run()
