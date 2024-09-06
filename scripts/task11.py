import pandas as pd
import numpy as np


def replace_outliers_with_mean(column):
    # Ensure the column is numeric
    column = pd.to_numeric(column, errors='coerce')
    Q1 = column.quantile(0.25)
    Q3 = column.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    # Replacing outliers with the mean of the column
    mean_value = column.mean()  # Ensure this works only for numeric data
    column = np.where((column < lower_bound) | (column > upper_bound), mean_value, column)
    return column



def dispersion_metrics(column):
    mean = column.mean()
    median = column.median()
    variance = column.var()
    std_dev = column.std()
    return {'Mean': mean, 'Median': median, 'Variance': variance, 'Std Dev': std_dev}
