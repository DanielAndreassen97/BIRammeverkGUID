# BIRammeverkGUID

This repository contains a small Streamlit application for creating and editing configuration tables used in a data warehouse project. The app exposes pages for managing data load parameters and table column mappings.

## Installation

Install the required packages with pip:

```bash
pip install -r requirements.txt
```

## Running the application

Start the Streamlit app from the repository root with:

```bash
streamlit run main.py
```

Streamlit configuration files are kept in the `.streamlit/` folder. Data created through the UI is stored as JSON files inside `pages_data/`.

