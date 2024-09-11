import pandas as pd
import streamlit as st

# Cache the dataset loading to avoid reloading it on every app rerun
@st.cache_data
def load_dataset(file_name, num_records=None):
    try:
        # Load the dataset
        df = pd.read_excel(file_name)
        
        # If num_records is specified, only load the last num_records records
        if num_records is not None:
            if len(df) > num_records:
                df = df.tail(num_records)
                
        return df
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None
