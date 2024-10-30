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
                title=f'{group_by_columns}',
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

def plot_time_series(data):
    with st.expander("TIME SERIES VISUALIZATION"):
        # Ensure '_submission_time' is in datetime format
        data['_submission_time'] = pd.to_datetime(data['_submission_time'], errors='coerce')

        # Drop rows with invalid or missing datetime entries
        data = data.dropna(subset=['_submission_time'])

        # Set the datetime column as the index
        data.set_index('_submission_time', inplace=True)

        # Resample the data to get counts of submissions per day
        daily_counts = data.resample('D').size()

        # Plot the time series chart
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(daily_counts, marker='o', linestyle='-', color='blue')

        ax.set_title('Survey Submissions Over Time', fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', fontsize=14)
        ax.set_ylabel('Number of Submissions', fontsize=14)

        # Add grid for better readability
        ax.grid(True, linestyle='--', alpha=0.7)

        # Display the plot in Streamlit
        st.pyplot(fig)


####################################################
def visualize_eligibility(filtered_data):
    # Convert the irrigated land column to numeric
    filtered_data["part_2_wheat/part_2_agriculture/part_2_irrigated_land"] = pd.to_numeric(
        filtered_data["part_2_wheat/part_2_agriculture/part_2_irrigated_land"].astype(str), errors='coerce'
    )

    # Determine eligibility
    filtered_data['eligibility'] = (
        (filtered_data["part_2_wheat/part_2_agriculture/part_2_irrigated_land"] >= 2) &
        (filtered_data["part_2_wheat/part_2_agriculture/part_2_irrigated_land"] <= 5)
    )

    # Count eligible and non-eligible households by district
    district_counts = filtered_data.groupby(['gen_info/district', 'eligibility']).size().unstack(fill_value=0)

    # Reset the index to get a DataFrame
    district_counts = district_counts.reset_index()
    district_counts.columns = ['gen_info/district', 'Non-Eligible', 'Eligible']  # Rename columns for clarity

    # Set up the figure with subplots
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Horizontal Bar Chart for Eligible and Non-Eligible Households
    district_counts_melted = district_counts.melt(id_vars='gen_info/district', value_vars=['Eligible', 'Non-Eligible'], 
                                                    var_name='Eligibility Status', value_name='Count')

    sns.barplot(data=district_counts_melted, x='Count', y='gen_info/district', hue='Eligibility Status', ax=axes[0])
    axes[0].set_title('Eligible and Non-Eligible Households by District (Horizontal Bar Chart)')
    axes[0].set_xlabel('Number of Households')
    axes[0].set_ylabel('District')
    axes[0].legend(title='Eligibility Status')

        # Pie Chart for total household counts (optional)
    total_counts = filtered_data['eligibility'].value_counts()
    axes[1].pie(total_counts, labels=total_counts.index.map({True: 'Eligible', False: 'Not Eligible'}),
                 autopct='%1.1f%%', startangle=90)
    axes[1].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    axes[1].set_title('Total Households by Eligibility (Pie Chart)')

    # Adding eligibility criteria description
    criteria_description = (
        "Eligibility Criteria:\n"
        "Irrigated Land: 2 to 5 acres"
    )

    # Positioning the text at the bottom center of the pie chart
    axes[1].text(0.5, -0.1, criteria_description, ha='center', va='center', fontsize=10, transform=axes[1].transAxes)


    # Histogram of irrigated land
    sns.histplot(filtered_data["part_2_wheat/part_2_agriculture/part_2_irrigated_land"], bins=10, ax=axes[2], kde=True)
    axes[2].set_title('Distribution of Cultivable Irrigated Land (Histogram)')
    axes[2].set_xlabel('Cultivable Irrigated Land (Jeribs)')
    axes[2].set_ylabel('Frequency')

    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)
