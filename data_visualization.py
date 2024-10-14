import streamlit as st
import pandas as pd
import plotly.express as px
import random
import matplotlib.pyplot as plt
import seaborn as sns
from data_analysis import identify_outliers

def apply_filters(df):
    filter_columns = st.multiselect("Select columns to filter", df.columns.tolist())
    filtered_df = df.copy()

    for col in filter_columns:
        unique_values = df[col].unique().tolist()
        filter_value = st.selectbox(f"Filter {col}", unique_values)
        filtered_df = filtered_df[filtered_df[col] == filter_value]

    return filtered_df

def group_by_visualize_and_download(df_selection):
    with st.expander("GROUP BY AND VISUALIZE"):
        group_by_columns = st.multiselect("Select Columns for Grouping:", df_selection.columns.tolist())

        if group_by_columns:
            grouped_data = df_selection.groupby(group_by_columns).size().reset_index(name='Count')
            total_count = grouped_data['Count'].sum()
            st.write(f"**Total Count:** {total_count}")

            num_bars = len(grouped_data)
            colors = [f'rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})' for _ in range(num_bars)]

            fig = px.bar(
                grouped_data,
                y=group_by_columns[0],
                x='Count',
                color=group_by_columns[1] if len(group_by_columns) > 1 else None,
                title="Grouped Data Visualization",
                orientation='h',
                color_discrete_sequence=colors
            )

            fig.update_layout(
                xaxis_title="Count",
                yaxis_title=group_by_columns[0],
                plot_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(fig, use_container_width=True)

            excel_file = "grouped_data.xlsx"
            grouped_data.to_excel(excel_file, index=False)

            with open(excel_file, "rb") as f:
                st.download_button(
                    label="Download Grouped Data as Excel",
                    data=f,
                    file_name=excel_file,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

def display_group_by_table(df_selection):
    with st.expander("GROUP BY TABLE"):
        group_by_columns = st.multiselect("Select Columns for Table Grouping:", df_selection.columns.tolist())

        if group_by_columns:
            grouped_data_table = df_selection.groupby(group_by_columns).size().reset_index(name='Total')
            st.write(grouped_data_table)

            total_count = grouped_data_table['Total'].sum()
            st.write(f"**Total Count Across All Groups:** {total_count}")

def plot_boxplot(df, column):
    """
    Function to plot a box-plot for a selected numeric column with enhanced design and readability.
    """
    if column:
        plt.figure(figsize=(12, 6))  # Set the figure size
        sns.set(style="whitegrid")  # Set the style

        # Create the boxplot
        ax = sns.boxplot(x=df[column], color='skyblue', fliersize=5, linewidth=1.5)

        # Overlay a jittered scatter plot
        sns.stripplot(x=df[column], color='black', alpha=0.6, size=4, jitter=True)

        ax.set_title(f'Box-plot for {column}', fontsize=16, fontweight='bold')
        ax.set_xlabel(column, fontsize=14)
        ax.set_ylabel('Values', fontsize=14)

        # Add grid for better readability
        ax.grid(True, linestyle='--', alpha=0.7)

        # Customize ticks
        ax.tick_params(axis='both', which='major', labelsize=12)

        # Rotate x-axis labels if necessary
        plt.xticks(rotation=45)

        # Display the plot in Streamlit
        st.pyplot(plt)

        # Clear the plot to avoid overlapping plots on subsequent calls
        plt.clf()

        # Identify outliers
        outliers_df = identify_outliers(df, column)

        # Display the outliers in Streamlit
        if not outliers_df.empty:
            st.write(f"Detected Outliers in '{column}':")
            st.dataframe(outliers_df)  # Display the outliers DataFrame
        else:
            st.write(f"No outliers detected in '{column}'.")

    else:
        st.warning("Please select a numeric column for the box-plot.")
