# table_utils.py
import os
import json
import pandas as pd
import streamlit as st
import io
def create_config_table(data_file, page_title):
    """
    Creates or manages a configuration table with actions like adding columns,
    rows, renaming, and deleting columns/rows.

    Args:
        data_file (str): Path to the JSON file to save/load data.
        table_name (str): Name of the table to display.
        page_title (str): Title for the Streamlit page.
    """
    # Page Title
    st.title(page_title)

    folder_path = "pages_data"
    os.makedirs(folder_path, exist_ok=True)  # Ensure the folder exists

    full_file_path = os.path.join(folder_path, data_file)

    # Load or initialize the DataFrame
    if os.path.exists(full_file_path):
        with open(full_file_path, "r") as file:
            data = json.load(file)
            df = pd.DataFrame(data)
    else:
        df = pd.DataFrame()  # Start with an empty DataFrame

    # Display the table
    if df.empty:
        st.write(f"The table '{page_title}' is currently empty. Add columns to begin.")
    else:
        df = df.astype(str)
        styled_df = df.style.set_properties(**{'white-space': 'pre-wrap'})  # Wrap text in cells
        st.dataframe(styled_df, use_container_width=True)

    def save_to_json(dataframe, folder_path=folder_path):
        """
        Saves the DataFrame to a JSON file in a specified folder.

        Args:
            dataframe (pd.DataFrame): The DataFrame to save.
            folder_path (str): Folder path where the file will be saved. Default is 'pages_data'.
        """
        # Ensure the folder exists
        os.makedirs(folder_path, exist_ok=True)

        # Build the full file path
        file_path = os.path.join(folder_path, data_file)

        # Ensure all data is saved as text
        dataframe = dataframe.astype(str)

        # Save the DataFrame as a JSON file
        with open(file_path, "w") as file:
            json.dump(dataframe.to_dict(orient="records"), file)

        print(f"File saved to {file_path}")

    # Table actions
    st.write("## Table Actions")
    action = st.selectbox(
        "Choose an action:",
        ["", "Add New Row", "Add New Column", "Rename Column", "Delete Column", "Delete Rows", "Modify Cell Value", "Import Data From Excel"]
    )


    # Add New Column
    if action == "Add New Column":
        new_col = st.text_input("Enter new column name:")
        if st.button("Add Column"):
            if new_col.strip():
                if df.empty:
                    df = pd.DataFrame({new_col: [None]})  # Ensure JSON compatibility with a blank row
                elif new_col not in df.columns:
                    df[new_col] = None
                else:
                    st.error("Column name already exists!")
                    st.stop()

                save_to_json(df)
                st.session_state["success_message"] = f"Added new column '{new_col}'."
                st.rerun()
            else:
                st.error("Column name cannot be empty!")

    # Add New Row
    if action == "Add New Row":
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
                    st.session_state["success_message"] = "Added new row."
                    st.rerun()
                else:
                    st.error("All fields must be filled to add a row.")

    # Rename Column
    if action == "Rename Column" and not df.empty:
        col_to_rename = st.selectbox("Select a column to rename:", df.columns)
        new_col_name = st.text_input("Enter new column name:")
        if st.button("Rename"):
            if new_col_name.strip():
                df.rename(columns={col_to_rename: new_col_name}, inplace=True)
                save_to_json(df)
                st.success(f"Renamed '{col_to_rename}' to '{new_col_name}'.")
                st.rerun()

    # Delete Column
    if action == "Delete Column" and not df.empty:
        col_to_delete = st.selectbox("Select column to delete:", df.columns)
        if st.button("Delete Column"):
            df.drop(columns=[col_to_delete], inplace=True)
            save_to_json(df)
            st.session_state["success_message"] = f"Deleted column '{col_to_delete}'."
            st.rerun()

    # Delete Rows
    if action == "Delete Rows" and not df.empty:
        start_index = st.number_input("Enter start row index:", min_value=0, max_value=len(df)-1, step=1)
        end_index = st.number_input("Enter end row index:", min_value=0, max_value=len(df)-1, step=1)
        if st.button("Delete Rows"):
            if start_index <= end_index:
                df = df.drop(index=range(start_index, end_index + 1)).reset_index(drop=True)
                save_to_json(df)
                st.session_state["success_message"] = f"Deleted rows from index {start_index} to {end_index}."
                st.rerun()

    # Modify Cell Value
    if action == "Modify Cell Value" and not df.empty:
        col_to_modify = st.selectbox("Select column:", df.columns)
        row_index = st.number_input("Enter row index:", min_value=0, max_value=len(df)-1, step=1)
        current_value = df.at[row_index, col_to_modify]
        st.write(f"Current value: `{current_value}`")
        new_value = st.text_input("Enter new value:")
        if st.button("Update Value"):
            df.at[row_index, col_to_modify] = new_value
            save_to_json(df)
            st.session_state["success_message"] = f"Updated row {row_index}, column '{col_to_modify}' with value '{new_value}'."
            st.rerun()


    import io

    # Import Data From Excel
    if action == "Import Data From Excel":
        st.write("### Import Data From Excel")
        st.write("Paste tabular data from Excel here (tab-separated):")
        
        # Text area for pasting data
        pasted_data = st.text_area("Paste your data:", height=200)

        if st.button("Import"):
            if pasted_data.strip():
                try:
                    # Clean up pasted data: Replace multiple spaces with tabs
                    cleaned_data = "\n".join(["\t".join(row.split()) for row in pasted_data.splitlines()])

                    if df.empty:
                        # For empty tables, treat first row as headers
                        new_df = pd.read_csv(io.StringIO(cleaned_data), sep="\t", header=0)
                        df = new_df  # Assign directly
                        save_to_json(df)
                        st.session_state["success_message"] = "Data imported successfully! First row used as column headers."
                        st.rerun()
                    else:
                        # For non-empty tables, read data without headers
                        new_df = pd.read_csv(io.StringIO(cleaned_data), sep="\t", header=None)

                        # Validate schema: Match number of columns
                        if new_df.shape[1] == len(df.columns):
                            new_df.columns = df.columns  # Assign existing column names
                            df = pd.concat([df, new_df], ignore_index=True)
                            save_to_json(df)
                            st.session_state["success_message"] = "New rows added successfully!"
                            st.rerun()
                        elif new_df.shape[1] < len(df.columns):
                            st.error(
                                f"Schema mismatch! The pasted data has fewer columns ({new_df.shape[1]}) "
                                f"than the existing table ({len(df.columns)})."
                            )
                        elif new_df.shape[1] > len(df.columns):
                            st.error(
                                f"Schema mismatch! The pasted data has more columns ({new_df.shape[1]}) "
                                f"than the existing table ({len(df.columns)})."
                            )
                except Exception as e:
                    st.error(f"Error processing data: {str(e)}")
            else:
                st.error("No data pasted. Please paste your Excel data.")


    # Display the success message at the bottom
    if "success_message" in st.session_state:
        st.success(st.session_state.pop("success_message"))
