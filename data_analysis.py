import pandas as pd

def calculate_statistics(df_selection, selected_columns):
    total_2_mean = total_2_median = total_3_min = total_3_max = total_4 = 0

    if selected_columns:
        # Convert the first selected column to numeric before calculating mean and median
        col_data = pd.to_numeric(df_selection[selected_columns[0]].str.strip(), errors='coerce')
        
        total_2_mean = float(col_data.mean())
        total_2_median = float(col_data.median())

        if len(selected_columns) > 1:
            # Convert the second selected column to numeric for min and max
            col_data_2 = pd.to_numeric(df_selection[selected_columns[1]].str.strip(), errors='coerce')
            total_3_min = float(col_data_2.min())
            total_3_max = float(col_data_2.max())

        if len(selected_columns) > 2:
            # Convert the third selected column to numeric for outlier calculation
            col_data_3 = pd.to_numeric(df_selection[selected_columns[2]].str.strip(), errors='coerce')
            q1 = col_data_3.quantile(0.25)
            q3 = col_data_3.quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            total_4 = ((col_data_3 < lower_bound) | (col_data_3 > upper_bound)).sum()

    return total_2_mean, total_2_median, total_3_min, total_3_max, total_4
