from tableutils import create_config_table
import streamlit as st



# File path for storing the data
DATA_FILE = "tablecolumnmapping.json"

# Call the function to create/manage the configuration table
customer = st.session_state.get("selected_customer")
create_config_table(DATA_FILE, "Table Column Mapping", customer)
