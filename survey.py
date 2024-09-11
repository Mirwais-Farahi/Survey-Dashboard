# survey.py
import pandas as pd
import streamlit as st

# Cache the dataset loading to avoid reloading it on every app rerun
@st.cache_data
def load_dataset(file_name):
    try:
        # Load the dataset
        df = pd.read_excel(file_name)
        return df
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None
