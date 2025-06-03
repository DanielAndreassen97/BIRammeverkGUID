import streamlit as st
from auth_utils import authenticate, get_customers

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Hide the sidebar and navigation when on the login page
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {display: none;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Login")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if authenticate(username, password):
        st.session_state["authenticated"] = True
        st.session_state["username"] = username
        customers = get_customers(username)
        if customers:
            st.session_state["selected_customer"] = customers[0]
        # Navigate to the default page after successful login
        # Use the page path relative to the main script
        st.switch_page("pages/about.py")
    else:
        st.error("Invalid username or password")
