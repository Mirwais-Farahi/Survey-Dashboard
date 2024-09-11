import streamlit as st
import pandas as pd
from survey import load_dataset
from filter_dataframe import apply_filters
from PIL import Image

# Load and resize the logo
logo = Image.open("logo.png")
st.sidebar.image(logo)

# Sidebar title and description
st.sidebar.title("Survey Dashboard")
st.sidebar.markdown("## Data Selection and Filtering")
st.sidebar.write("Select a dataset and specify the number of last records to load.")

# List of dataset names
dataset_names = {
    "None": None,  # Default value when no dataset is selected
    "LTA Baseline": "lta_baseline.xlsx",
    "LTA PDM": "lta_pdm.xlsx",
    "LTA PHM": "lta_phm.xlsx"
}

# Sidebar to select the dataset
selected_dataset = st.sidebar.selectbox("Select a dataset", list(dataset_names.keys()))

# Input for the number of last records
num_records = st.sidebar.number_input("Number of last records to display", min_value=1, value=1000, step=1)

# Button to load the dataset
load_data_button = st.sidebar.button("Load Dataset")

# Load the dataset if the button is clicked
df = None
if load_data_button and selected_dataset != "None":
    df = load_dataset(dataset_names[selected_dataset], num_records=num_records)

# Main title and header
st.title("📊 Survey Data Dashboard")
st.markdown("""
Welcome to the **Survey Data Dashboard**. Here, you can analyze different survey datasets, 
apply filters, and visualize the data.
""")

if df is not None:
    # Show the dataset overview
    with st.expander(f"Dataset Overview: {selected_dataset}"):
        st.write(f"Displaying the last {num_records} records for {selected_dataset}")
        st.write(df.head(5))  # Show a preview of the first 5 records of the last N records

    # Allow user to select the date column
    date_column = st.selectbox("Select the date column", ["None"] + df.columns.tolist())

    if date_column != "None":
        # Convert the date column to datetime
        df[date_column] = pd.to_datetime(df[date_column], format='%Y-%m-%d', errors='coerce')

        # Add date range picker
        start_date, end_date = st.date_input("Select Date Range", [df[date_column].min(), df[date_column].max()])

        # Apply date range filter
        mask = (df[date_column] >= pd.to_datetime(start_date)) & (df[date_column] <= pd.to_datetime(end_date))
        filtered_df = df.loc[mask]

        # Apply additional filters
        filtered_df = apply_filters(filtered_df)

        # Display filtered data with pagination
        st.subheader("Filtered Data")

        # Pagination setup
        page_size = 100  # Define the number of rows to display per page
        total_rows = len(filtered_df)
        page_number = st.number_input("Page number", min_value=1, max_value=(total_rows // page_size) + 1, step=1)

        # Calculate start and end indices for the current page
        start_idx = (page_number - 1) * page_size
        end_idx = start_idx + page_size

        # Display the paginated data
        st.write(filtered_df.iloc[start_idx:end_idx])

elif selected_dataset == "None":
    st.write("Please select a dataset and specify the number of last records to display.")
else:
    st.write("Click the 'Load Dataset' button to load the dataset.")
