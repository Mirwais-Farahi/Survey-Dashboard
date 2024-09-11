# filter_dataframe.py
import streamlit as st

def apply_filters(df):
    # Let the user select columns to filter by
    filter_columns = st.multiselect("Select columns to filter", df.columns.tolist())

    filtered_df = df.copy()

    # Apply filters dynamically
    for col in filter_columns:
        unique_values = df[col].unique().tolist()
        filter_value = st.selectbox(f"Filter {col}", unique_values)
        filtered_df = filtered_df[filtered_df[col] == filter_value]

    return filtered_df
