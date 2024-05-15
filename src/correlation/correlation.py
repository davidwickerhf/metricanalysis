import pandas as pd

class CorrelationAnalyzer:
    """Class to perform correlation analysis."""

    def compute_correlations(self, data_df, columns):
        """
        Computes the correlation matrix for the specified columns in the DataFrame.

        Parameters:
        data_df (pd.DataFrame): DataFrame containing the data.
        columns (list): List of columns to compute correlations for.

        Returns:
        pd.DataFrame: Correlation matrix.
        """
        return data_df[columns].corr(method='kendall')
