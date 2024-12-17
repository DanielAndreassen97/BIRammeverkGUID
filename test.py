import streamlit as st
import pandas as pd
import json
import os

# File path for JSON storage
JSON_FILE = "tablecolumnmapping.json"

# Initialize session state
if "data_updated" not in st.session_state:
    st.session_state.data_updated = False

# Load or initialize data
if os.path.exists(JSON_FILE) and os.stat(JSON_FILE).st_size > 0:
    with open(JSON_FILE, "r") as file:
        data = json.load(file)
        df = pd.DataFrame(data)
else:
    df = pd.DataFrame()  # Start with an empty table

st.title("Dynamic Table Manager")

# Function to save the DataFrame to JSON
def save_to_json(dataframe):
    with open(JSON_FILE, "w") as file:
        json.dump(dataframe.to_dict(orient="records"), file)

# Display Table
st.write("## Current Table")
if df.empty:
    st.write("The table is currently empty. Add columns to begin.")
else:
    st.dataframe(df)

# Actions Dropdown
st.write("## Table Actions")
action = st.selectbox(
    "Choose an action:", 
    ["", "Add New Row", "Add New Column", "Rename Column", "Delete Column", "Delete Rows", "Modify Cell Value", "Import Data From Excel"]
)

# Add New Column
if action == "Add New Column":
    st.write("### Add New Column")
    new_col = st.text_input("Enter new column name:", key="add_column")
    if st.button("Add Column"):
        if new_col.strip():
            if df.empty:
                # Initialize an empty DataFrame with the new column
                df = pd.DataFrame({new_col.strip(): [""]})
            else:
                # Add a new column to an existing DataFrame
                if new_col.strip() not in df.columns:
                    df[new_col.strip()] = ""  # Initialize the new column with empty values
                else:
                    st.error("Column name already exists!")
                    st.stop()

            # Save the updated DataFrame
            save_to_json(df)
            st.success(f"Added new column '{new_col.strip()}'.")
            st.rerun()
        else:
            st.error("Column name cannot be empty.")

# Add New Row
if action == "Add New Row":
    st.write("### Add New Row")
    if df.empty:
        st.warning("Please add at least one column before adding rows.")
    else:
        new_row_data = {}
        for col in df.columns:
            new_row_data[col] = st.text_input(f"Enter value for '{col}':", key=f"row_{col}")
        if st.button("Add Row"):
            if all(new_row_data.values()):
                df = pd.concat([df, pd.DataFrame([new_row_data])], ignore_index=True)
                save_to_json(df)
                st.success("Added new row.")
                st.rerun()
            else:
                st.error("All fields must be filled to add a row.")

# Rename Column
if action == "Rename Column" and not df.empty:
    st.write("### Rename Column")
    col_to_rename = st.selectbox("Select a column to rename:", df.columns, key="rename_column")
    new_col_name = st.text_input("Enter new column name:", key="new_column_name")
    if st.button("Rename"):
        if new_col_name.strip():
            df.rename(columns={col_to_rename: new_col_name.strip()}, inplace=True)
            save_to_json(df)
            st.success(f"Renamed '{col_to_rename}' to '{new_col_name.strip()}'.")
            st.rerun()

# Delete Column
if action == "Delete Column" and not df.empty:
    st.write("### Delete Column")
    col_to_delete = st.selectbox("Select column to delete:", df.columns, key="delete_column")
    if st.button("Delete Column"):
        df.drop(columns=[col_to_delete], inplace=True)
        save_to_json(df)
        st.success(f"Deleted column '{col_to_delete}'.")
        st.rerun()

# Delete Rows
if action == "Delete Rows" and not df.empty:
    st.write("### Delete Rows")
    start_index = st.number_input("Enter start row index:", min_value=0, max_value=len(df)-1, step=1, key="start_index")
    end_index = st.number_input("Enter end row index:", min_value=0, max_value=len(df)-1, step=1, key="end_index")
    if st.button("Delete Rows"):
        if start_index <= end_index:
            df = df.drop(index=range(start_index, end_index + 1)).reset_index(drop=True)
            save_to_json(df)
            st.success(f"Deleted rows from index {start_index} to {end_index}.")
            st.rerun()
        else:
            st.error("Start index must be less than or equal to the end index.")

# Modify Cell Value
if action == "Modify Cell Value" and not df.empty:
    st.write("### Modify Cell Value")
    col_to_modify = st.selectbox("Select column:", df.columns, key="modify_column")
    row_index = st.number_input("Enter row index:", min_value=0, max_value=len(df)-1, step=1, key="row_index")
    current_value = df.at[row_index, col_to_modify]
    st.write(f"Current value: `{current_value}`")
    new_value = st.text_input("Enter new value:", key="new_value")
    if st.button("Update Value"):
        df.at[row_index, col_to_modify] = new_value
        save_to_json(df)
        st.success(f"Updated row {row_index}, column '{col_to_modify}' with value '{new_value}'.")
        st.rerun()

# Import Data From Excel
if action == "Import Data From Excel":
    st.write("### Import Data From Excel")
    st.write("Paste tabular data from Excel here (tab-separated):")
    pasted_data = st.text_area("Paste your data:", height=200, key="import_data")

    if st.button("Import"):
        if pasted_data.strip():
            try:
                # Clean up pasted data: Replace multiple spaces with tabs
                cleaned_data = "\n".join(["\t".join(row.split()) for row in pasted_data.splitlines()])

                if df.empty:
                    # For empty tables, treat first row as headers
                    new_df = pd.read_csv(pd.io.common.StringIO(cleaned_data), sep="\t", header=0)
                    df = new_df  # Assign directly
                    save_to_json(df)
                    st.success("Data imported successfully! First row used as column headers.")
                else:
                    # For non-empty tables, read data without headers
                    new_df = pd.read_csv(pd.io.common.StringIO(cleaned_data), sep="\t", header=None)

                    # Validate schema: Match number of columns
                    if new_df.shape[1] == len(df.columns):
                        new_df.columns = df.columns  # Assign existing column names
                        df = pd.concat([df, new_df], ignore_index=True)
                        save_to_json(df)
                        st.success("New rows added successfully!")
                    else:
                        st.error(f"Schema mismatch! Expected {len(df.columns)} columns but got {new_df.shape[1]}.")

                st.rerun()
            except Exception as e:
                st.error(f"Error processing data: {str(e)}")
        else:
            st.error("No data pasted. Please paste your Excel data.")



