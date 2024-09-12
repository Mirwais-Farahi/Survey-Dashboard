# sidebar.py
import streamlit as st
from PIL import Image  # Import Image from PIL
from survey import load_dataset

def sidebar():
    # Load and resize the logo
    logo = Image.open("logo.png")
    st.sidebar.image(logo)

    # Sidebar title and description
    st.sidebar.title("Survey Dashboard")
    st.sidebar.markdown("## Data Selection and Filtering")
    st.sidebar.write("Select a dataset to load.")

    # List of dataset names
    dataset_names = {
        "None": None,  # Default value when no dataset is selected
        "LTA Baseline Form-1": "lta_baseline_1.xlsx",
        "LTA Baseline Form-2": "lta_baseline_2.xlsx",
        "LTA PDM": "lta_pdm.xlsx",
        "LTA PHM": "lta_phm.xlsx",
        "sample data": "https://raw.githubusercontent.com/Mirwais-Farahi/datasets/main/lta_baseline_1.xlsx"
    }

    # Sidebar to select the dataset
    selected_dataset = st.sidebar.selectbox("Select a dataset", list(dataset_names.keys()))

    # Button to load the dataset
    load_data_button = st.sidebar.button("Load Dataset")

    return selected_dataset, load_data_button, dataset_names
