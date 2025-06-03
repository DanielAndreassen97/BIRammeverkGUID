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

## Authentication

The app now displays a simple login screen before showing the configuration pages.
Credentials are stored in a `users.json` file at the repository root. The repository ships with a test account:

```
username: admin
password: admin123
```

Add or edit entries in `users.json` to manage users.

## Deploying for Free

You can host this application for free using **Streamlit Community Cloud**. Once
logged in with your GitHub account, click *"New app"* and select this repository
and branch. Streamlit will automatically install the dependencies and run the
app live on a public URL.

See [Streamlit's documentation](https://docs.streamlit.io/streamlit-community-cloud) for detailed steps.

