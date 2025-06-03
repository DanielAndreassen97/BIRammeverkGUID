import streamlit as st
from streamlit.runtime.scriptrunner_utils.script_run_context import (
    get_script_run_ctx,
)
from auth_utils import authenticate, get_customers, add_customer

# Exit with a helpful message if run directly without `streamlit run`
if get_script_run_ctx(suppress_warning=True) is None:
    raise RuntimeError("Please run this app using 'streamlit run main.py'")

# Set page layout to wide
st.set_page_config(layout="wide")

login_page = st.Page("pages/login.py", title="Login", url_path="login")
about_page = st.Page(
    page="pages/about.py",
    title="About",
    default=True,
)
dataloadparameter_page = st.Page(
    page="pages/dataloadparameter.py",
    title="Data Load Parameters",
)
tablecolumnmapping_page = st.Page(
    page="pages/tablecolumnmapping.py",
    title="Table Column Mapping",
)

pg = st.navigation([
    about_page,
    dataloadparameter_page,
    tablecolumnmapping_page,
    login_page,
])

# ---- PAGE SETUP ----

if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    if pg.url_path != login_page.url_path:
        st.switch_page("login")
    else:
        pg.run()
    st.stop()

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.switch_page("login")

username = st.session_state.get("username")
customers = get_customers(username)

if customers:
    if "selected_customer" not in st.session_state:
        st.session_state["selected_customer"] = customers[0]
    idx = customers.index(st.session_state["selected_customer"])
    selected = st.sidebar.selectbox(
        "Select customer", customers, index=idx
    )
    st.session_state["selected_customer"] = selected
else:
    st.sidebar.write("No customers configured.")
    with st.sidebar.form("add_first_customer"):
        new_customer = st.text_input("Customer name")
        submitted = st.form_submit_button("Add Customer")
    if submitted and new_customer.strip():
        add_customer(username, new_customer.strip())
        st.session_state["selected_customer"] = new_customer.strip()
        st.rerun()

with st.sidebar.expander("Add Customer"):
    new_cust = st.text_input("New customer", key="new_customer")
    if st.button("Add", key="add_customer_btn") and new_cust.strip():
        add_customer(username, new_cust.strip())
        st.session_state["selected_customer"] = new_cust.strip()
        st.rerun()

st.logo("images/crayon-logo.png")
st.sidebar.text("Made by Daniel🚀")

pg.run()
