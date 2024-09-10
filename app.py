import streamlit as st
from survey import load_dataset
from filter_dataframe import apply_filters
from PIL import Image

# Load and resize the logo
logo = Image.open("logo.png")
st.sidebar.image(logo)

# Sidebar title and description
st.sidebar.title("Survey Dashboard")
st.sidebar.markdown("## Data Selection and Filtering")
st.sidebar.write("Select a dataset from the dropdown and apply filters to view the results.")

# List of dataset names
dataset_names = {
    "LTA Baseline": "lta_baseline.xlsx",
    "LTA PDM": "lta_pdm.xlsx",
    "LTA PHM": "lta_phm.xlsx"
}

# Sidebar to select the dataset
selected_dataset = st.sidebar.selectbox("Select a dataset", list(dataset_names.keys()))

# Load the dataset based on the selection
df = load_dataset(dataset_names[selected_dataset])

# Main title and header
st.title("📊 Survey Data Dashboard")
st.markdown("""
Welcome to the **Survey Data Dashboard**. Here, you can analyze different survey datasets, 
apply filters, and visualize the data.
""")

if df is not None:
    # Display dataset info in an expander for a clean UI
    with st.expander(f"Dataset Overview: {selected_dataset}"):
        st.write(f"Displaying data for {selected_dataset}")
        st.write(df.head())  # Show a preview of the dataset

    # Display filter options and apply filters
    filtered_df = apply_filters(df)
    st.subheader("Filtered Data")
    st.write(filtered_df)

else:
    st.error("No data available. Please select a valid dataset from the sidebar.")
