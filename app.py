import streamlit as st
import pandas as pd
from filter_dataframe import apply_filters
from sidebar import sidebar
from header import top_header
from survey import load_dataset
from data_quality import detect_outliers_and_plot_box  # Import from data_quality.py

# Call the top-header function
top_header()

# Call the sidebar function
selected_dataset, load_data_button, dataset_names = sidebar()

# Initialize session state for dataset
if 'df' not in st.session_state:
    st.session_state.df = None
    st.session_state.selected_dataset = None

# Load the dataset if the button is clicked
if load_data_button and selected_dataset != "None":
    st.session_state.df = load_dataset(dataset_names[selected_dataset])
    st.session_state.selected_dataset = selected_dataset

df = st.session_state.df
selected_dataset = st.session_state.selected_dataset

if df is not None:
    # Show the dataset overview
    with st.expander(f"Dataset Overview: {selected_dataset}"):
        st.write(f"Displaying records for {selected_dataset}")
        st.write(df.head(5))  # Show a preview of the first 5 records

    # Display the total number of surveys in the dataset
    st.write(f"Total number of surveys: {len(df)}")

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

        # Count surveys within the date range
        count_surveys = len(filtered_df)
        st.write(f"Number of surveys in the selected date range: {count_surveys}")

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

        # Allow user to select columns for grouping
        group_by_columns = st.multiselect("Select columns to group by", options=df.columns.tolist(), default=[])

        if group_by_columns:
            # Perform the groupby operation
            grouped_df = filtered_df.groupby(group_by_columns).size().reset_index(name='Count')

            # Display the grouped data
            st.subheader("Grouped Data")
            st.write(grouped_df)

        # Outlier Detection Section
        st.subheader("Outlier Detection with Box Plot")

        # Ask the user to select a column for outlier detection
        column_name = st.selectbox("Select a numeric column for outlier detection", options=["None"] + filtered_df.columns.tolist())

        if column_name != "None":
            # Call the detect_outliers_and_plot_box function from data_quality.py
            detect_outliers_and_plot_box(filtered_df, column_name)

elif selected_dataset == "None":
    st.write("Please select a dataset to display.")
else:
    st.write("Click the 'Load Dataset' button to load the dataset.")
