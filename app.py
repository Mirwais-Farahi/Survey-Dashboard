import streamlit as st
from survey import load_dataset
from filter_dataframe import apply_filters

# List of dataset names
dataset_names = {
    "LTA Baseline": "lta_baseline.xlsx",
    "LTA PDM": "lta_pdm.xlsx",
    "LTA PHM": "lta_phm.xlsx"
}

st.title("LTA Survey Data Dashboard")

# Sidebar to select the dataset
selected_dataset = st.sidebar.selectbox("Select a dataset", list(dataset_names.keys()))

# Load the dataset based on the selection
df = load_dataset(dataset_names[selected_dataset])

if df is not None:
    st.write(f"Displaying data for {selected_dataset}")
    st.write(df.head())  # Show a preview of the dataset

    # Display filter options and apply filters
    filtered_df = apply_filters(df)
    st.write("Filtered Data")
    st.write(filtered_df)

else:
    st.write("No data to display")
