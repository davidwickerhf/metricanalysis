import pandas as pd

class CorrelationAnalyzer:
    """Class to perform correlation analysis."""

    def compute_correlations(self, data_df, columns):
        """
        Computes Kendall correlation matrix for specified columns in the DataFrame.

        Parameters:
        data_df (pd.DataFrame): The data frame containing the data.
        columns (list): List of columns to compute correlations for.

        Returns:
        pd.DataFrame: Correlation matrix.
        """
        return data_df[columns].corr(method='kendall')
    
    def compute_importance_correlations(self, data_df, centrality_columns):
        """
        Computes the correlation between importance scores and centrality measures.

        Parameters:
        data_df (pd.DataFrame): The data frame containing the data.
        centrality_columns (list): List of centrality columns.

        Returns:
        pd.Series: Correlation values.
        """
        return data_df[centrality_columns + ['importance']].corr(method='kendall')['importance']

    def compute_court_branch_correlations(self, data_df, centrality_columns):
        """
        Computes the correlation between court branch and centrality measures.

        Parameters:
        data_df (pd.DataFrame): The data frame containing the data.
        centrality_columns (list): List of centrality columns.

        Returns:
        pd.Series: Correlation values.
        """
        data_df['court_branch_numeric'] = pd.factorize(data_df['court_branch'])[0]
        return data_df[centrality_columns + ['court_branch_numeric']].corr(method='kendall')['court_branch_numeric']
