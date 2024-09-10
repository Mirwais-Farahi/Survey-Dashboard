import pandas as pd
import streamlit as st

def load_dataset(file_name):
    try:
        # Load the dataset and return a DataFrame
        df = pd.read_excel(file_name)
        return df
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None
