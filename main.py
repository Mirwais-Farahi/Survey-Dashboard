import streamlit as st
from streamlit_option_menu import option_menu
from data_loader import load_dataset
from data_visualization import group_by_visualize_and_download, display_group_by_table
from data_analysis import calculate_statistics
from streamlit_extras.metric_cards import style_metric_cards
from datetime import datetime

st.set_page_config(page_title="Dashboard", page_icon="🌍", layout="wide")

# Load Style CSS
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def home():
    st.title("Welcome to the Data Dashboard!")
    st.markdown(
        """
        This application provides insights into various datasets collected from field surveys. 
        Use the navigation menu on the left to select a project and explore the data.
        
        ### Features:
        - Data filtering
        - Statistical analysis
        - Visual data representation
        - Downloadable reports

        Select a dataset from the menu to begin!
        """
    )

def load_and_display_data(selected, submitted_after):
    df = load_dataset(selected, submitted_after=submitted_after)

    if df is not None and not df.empty:
        st.success(f"{selected} dataset loaded successfully!")

        # Dynamic filtering: User selects columns first, then filters based on their values
        available_columns = df.columns.tolist()
        selected_columns = st.multiselect("Select columns to filter:", available_columns)

        if selected_columns:
            filters = {}
            for column in selected_columns:
                unique_values = df[column].dropna().unique().tolist()
                selected_values = st.multiselect(f"Select values for {column}:", unique_values)
                if selected_values:
                    filters[column] = selected_values

            # Apply the filters dynamically based on user selection
            if filters:
                for column, values in filters.items():
                    df = df[df[column].isin(values)]

        with st.expander("VIEW EXCEL DATASET"):
            showData = st.multiselect('Filter columns to display:', df.columns.tolist())
            if showData:
                st.dataframe(df[showData], use_container_width=True)

        selected_columns = []
        column_options = df.select_dtypes(include=['number']).columns.tolist()
        selected_columns = st.multiselect("Select Columns for Statistical Calculation:", column_options, default=selected_columns)

        total_1 = len(df) if len(df) > 0 else 0
        total_2_mean, total_2_median, total_3_min, total_3_max, total_4 = calculate_statistics(df, selected_columns)

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


def sideBar():
    with st.sidebar:
        st.image("data/logo.png", use_column_width=True)
        selected = option_menu(
            menu_title="Projects",
            options=[
                "Home", 
                "LTA - Baseline 1", 
                "LTA - Baseline 2", 
                "LTA - Baseline 3", 
                "LTA - PDM", 
                "LTA - PHM"
            ],
            icons=["house", "eye", "eye", "eye", "eye", "book"],
            menu_icon="cast",
            default_index=0
        )
        st.session_state.selected_option = selected

        if selected in ["LTA - Baseline 1", "LTA - Baseline 2", "LTA - Baseline 3", "LTA - PDM", "LTA - PHM"]:
            st.subheader("Submission Date")
            submitted_after = st.date_input(
                "Select date from which to load data:",
                value=datetime.today(),
                min_value=datetime(2020, 1, 1),
                max_value=datetime.today()
            )
            st.session_state.submitted_after = submitted_after
        else:
            st.session_state.submitted_after = None

        # Add tooltips manually as info icons
        if selected == "LTA - Baseline 1":
            st.info("Baseline type 1 - TPM_Beneficiary_Verif_Final - AACS")
        elif selected == "LTA - Baseline 2":
            st.info("Baseline type 2 - 1. TPM_LTA_Beneficiary_Verif..")
        elif selected == "LTA - Baseline 3":
            st.info("Baseline type 3 - TPM_AACS_BBV_New Interventions_Questionnaire")
        elif selected == "LTA - PDM":
            st.info("Post-distribution Monitoring")
        elif selected == "LTA - PHM":
            st.info("Post-harvest Monitoring")

    if selected == "Home":
        home()
    elif selected in ["LTA - Baseline 1", "LTA - Baseline 2", "LTA - Baseline 3", "LTA - PDM", "LTA - PHM"]:
        submitted_after = st.session_state.submitted_after
        load_and_display_data(selected, submitted_after)

sideBar()
