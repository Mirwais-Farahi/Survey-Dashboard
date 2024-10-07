import pandas as pd

def calculate_statistics(df_selection, selected_columns):
    total_2_mean = total_2_median = total_3_min = total_3_max = total_4 = 0

    if selected_columns:
        total_2_mean = float(df_selection[selected_columns[0]].mean())
        total_2_median = float(df_selection[selected_columns[0]].median())

        if len(selected_columns) > 1:
            total_3_min = float(df_selection[selected_columns[1]].min())
            total_3_max = float(df_selection[selected_columns[1]].max())

        if len(selected_columns) > 2:
            col_data = df_selection[selected_columns[2]]
            q1 = col_data.quantile(0.25)
            q3 = col_data.quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            total_4 = ((col_data < lower_bound) | (col_data > upper_bound)).sum()

    return total_2_mean, total_2_median, total_3_min, total_3_max, total_4
