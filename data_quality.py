import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def detect_outliers_and_plot_box(filtered_df, column_name):
    """
    Detect outliers in the specified column, display descriptive statistics,
    and plot a box plot.
    
    Parameters:
    - filtered_df: The filtered DataFrame
    - column_name: The column to perform outlier detection on
    
    Returns:
    - None: Displays a box plot and descriptive statistics on Streamlit
    """
    # Convert the column to numeric, forcing errors to NaN
    filtered_df[column_name] = pd.to_numeric(filtered_df[column_name], errors='coerce')

    # Drop rows with NaN values in the selected column
    numeric_df = filtered_df.dropna(subset=[column_name])

    # Descriptive statistics
    st.subheader(f"Descriptive Statistics for '{column_name}'")
    description = numeric_df[column_name].describe()
    st.write(f"**Number of entries:** {description['count']}")
    st.write(f"**Average value:** {description['mean']}")
    st.write(f"**Standard deviation:** {description['std']}")
    st.write(f"**Minimum value:** {description['min']}")
    st.write(f"**25th percentile (25% of values are below this):** {description['25%']}")
    st.write(f"**Median (50% of values are below this):** {description['50%']}")
    st.write(f"**75th percentile (75% of values are below this):** {description['75%']}")
    st.write(f"**Maximum value:** {description['max']}")

    # Percentile calculation
    percentiles = [0.9, 0.99]  # 90th and 99th percentiles
    percentile_values = numeric_df[column_name].quantile(percentiles)
    st.write(f"**90th percentile (90% of values are below this):** {percentile_values[0.9]}")
    st.write(f"**99th percentile (99% of values are below this):** {percentile_values[0.99]}")

    # Draw the box plot using matplotlib
    fig, ax = plt.subplots(figsize=(12, 8))
    box = ax.boxplot(numeric_df[[column_name]].values, vert=False, patch_artist=True, labels=[column_name])

    # Customize the box plot
    ax.set_title(f'Box Plot for {column_name}', fontsize=16)
    ax.set_xlabel(f'Number of {column_name}', fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.7)

    # Set colors for the box plot elements
    colors = ['#FF9999']
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)

    # Customize whiskers and medians
    for whisker in box['whiskers']:
        whisker.set(color='#7570b3', linewidth=2)
    for cap in box['caps']:
        cap.set(color='#7570b3', linewidth=2)
    for median in box['medians']:
        median.set(color='orange', linewidth=2)
    for flier in box['fliers']:
        flier.set(marker='o', color='#e7298a', alpha=0.5)

    # Display the plot in Streamlit
    st.pyplot(fig)
