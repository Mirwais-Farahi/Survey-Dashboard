import streamlit as st
import pandas as pd
from koboextractor import KoboExtractor
import plotly.express as px
import random
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
from streamlit_extras.metric_cards import style_metric_cards

st.set_page_config(page_title="Dashboard", page_icon="🌍", layout="wide")

# Load Style CSS
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Set up the KoBoToolbox API token and the base URL
KOBO_TOKEN = "0e7a75b50290d146396d6a3efef6d6de287683c6"
kobo = KoboExtractor(KOBO_TOKEN, 'https://eu.kobotoolbox.org/api/v2')

# Function to load dataset based on selection
def load_dataset(option):
    if option == "LTA - Baseline":
        return pd.read_excel('datasets/baseline.xlsx')  # Load local baseline data
    elif option == "LTA - PDM":
        asset_uid = "aHDFcWo745yEdv6bJvdJQt"  # Baseline Form ID
        new_data = kobo.get_data(asset_uid, submitted_after='2024-09-10T00:00:00')  # Fetch data from KoBoToolbox
        df = pd.DataFrame(new_data['results'])
        return df
    return None

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

def group_by_visualize_and_download(df_selection):
    with st.expander("GROUP BY AND VISUALIZE"):
        # Multi-selection for column selection for group-by operation
        group_by_columns = st.multiselect("Select Columns for Grouping:", df_selection.columns.tolist())

        if group_by_columns:
            # Grouping the data
            grouped_data = df_selection.groupby(group_by_columns).size().reset_index(name='Count')
            
            # Display total count for the grouped data
            total_count = grouped_data['Count'].sum()
            st.write(f"**Total Count:** {total_count}")

            # Generate random colors for the bars
            num_bars = len(grouped_data)
            colors = [f'rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})' for _ in range(num_bars)]

            # Create a horizontal bar chart of the grouped data
            fig = px.bar(
                grouped_data,
                y=group_by_columns[0],  # Use the first selected column for y-axis
                x='Count',  # Set x to the count of occurrences
                color=group_by_columns[1] if len(group_by_columns) > 1 else None,  # Color by second selected column if available
                title="Grouped Data Visualization",
                orientation='h',
                color_discrete_sequence=colors  # Assign the random colors
            )

            # Labeling the chart
            fig.update_layout(
                xaxis_title="Count",
                yaxis_title=group_by_columns[0],  # Set y-axis title to the first grouping column
                plot_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(fig, use_container_width=True)

            # Allow user to download grouped data as an Excel file
            excel_file = f"grouped_data.xlsx"
            grouped_data.to_excel(excel_file, index=False)

            # Create a download button
            with open(excel_file, "rb") as f:
                st.download_button(
                    label="Download Grouped Data as Excel",
                    data=f,
                    file_name=excel_file,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

def display_group_by_table(df_selection):
    with st.expander("GROUP BY TABLE"):
        # Multi-selection for columns to group by
        group_by_columns = st.multiselect("Select Columns for Table Grouping:", df_selection.columns.tolist())

        if group_by_columns:
            # Grouping the data
            grouped_data_table = df_selection.groupby(group_by_columns).size().reset_index(name='Total')
            st.write(grouped_data_table)

            # Display total count for the grouped data in the table
            total_count = grouped_data_table['Total'].sum()
            st.write(f"**Total Count Across All Groups:** {total_count}")

def calculate_statistics(df_selection, selected_columns):
    # Initialize totals
    total_2_mean = total_2_median = total_3_min = total_3_max = total_4 = 0

    # Calculate totals based on the order of selected columns
    if selected_columns:
        # Calculate mean and median for the first selected column
        total_2_mean = float(df_selection[selected_columns[0]].mean())
        total_2_median = float(df_selection[selected_columns[0]].median())

        if len(selected_columns) > 1:
            # Calculate min and max for the second selected column
            total_3_min = float(df_selection[selected_columns[1]].min())
            total_3_max = float(df_selection[selected_columns[1]].max())

        if len(selected_columns) > 2:
            # Calculate number of outliers for the third selected column
            col_data = df_selection[selected_columns[2]]
            q1 = col_data.quantile(0.25)
            q3 = col_data.quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            # Count outliers
            total_4 = ((col_data < lower_bound) | (col_data > upper_bound)).sum()

    return total_2_mean, total_2_median, total_3_min, total_3_max, total_4

def home():
    selected = st.session_state.selected_option  # Get the selected option from the session state
    df = load_dataset(selected)

    # Alert the user which dataset is loaded
    if df is not None and not df.empty:
        st.success(f"{selected} dataset loaded successfully!")

        with st.expander("VIEW EXCEL DATASET"):
            showData = st.multiselect('Filter: ', df.columns.tolist())
            if showData:  # Check if any columns are selected
                st.dataframe(df[showData], use_container_width=True)

        # Initialize selected_columns to avoid UnboundLocalError
        selected_columns = []

        # Multi-selection for column selection for Statistical Calculation
        column_options = df.select_dtypes(include=['number']).columns.tolist()  # Select only numeric columns
        selected_columns = st.multiselect("Select Columns for Statistical Calculation:", column_options, default=selected_columns)

        # Initialize total_1 to len
        total_1 = len(df) if len(df) > 0 else 0

        # Call the statistics calculation function
        total_2_mean, total_2_median, total_3_min, total_3_max, total_4 = calculate_statistics(df, selected_columns)

        # Display totals
        total1, total2, total3, total4 = st.columns(4, gap='small')
        with total1:
            st.metric(label="Total Surveys", value=f"{total_1:,.0f}", help="Total Collected Surveys")

        with total2:
            st.metric(label="Mean / Median", value=f"{total_2_mean:,.0f} / {total_2_median:,.0f}", help=selected_columns[0] if len(selected_columns) > 0 else "No Columns Selected")

        with total3:
            st.metric(label="Min / Max", value=f"{total_3_min:,.0f} / {total_3_max:,.0f}", help=selected_columns[1] if len(selected_columns) > 1 else "No Columns Selected")

        with total4:
            st.metric(label="Number of Outliers", value=f"{total_4:,.0f}", help=selected_columns[2] if len(selected_columns) > 2 else "No Columns Selected")

        style_metric_cards(background_color="#FFFFFF", border_left_color="#686664", border_color="#000000", box_shadow="#F71938")

        # Group by visualization and download section
        group_by_visualize_and_download(df)

        # Display group by table section
        display_group_by_table(df)
    else:
        st.warning("No data available for the selected option.")

# Menu bar
def sideBar():
    with st.sidebar:
        # Add logo at the top of the sidebar
        st.image("data/logo.png")  # Adjust the width as needed
        selected = option_menu(
            menu_title="Projects",
            options=["LTA - Baseline", "LTA - PDM"],
            icons=["house", "eye"],
            menu_icon="cast",
            default_index=0
        )
        # Store selected option in session state
        st.session_state.selected_option = selected

    # Call the home function after loading the dataset
    if selected in ["LTA - Baseline", "LTA - PDM"]:
        home()

# Execute sidebar function
sideBar()
