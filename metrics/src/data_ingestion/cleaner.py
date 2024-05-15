class DataCleaner:
    """Class to handle data cleaning and preprocessing."""

    def remove_communicated_cases(self, nodes_df):
        """
        Removes communicated cases from the nodes DataFrame.

        Parameters:
        nodes_df (pd.DataFrame): DataFrame containing node data.

        Returns:
        pd.DataFrame: Cleaned DataFrame with communicated cases removed.
        """
        return nodes_df[nodes_df['doctypebranch'] != 'COMMUNICATEDCASES']

    def filter_targets(self, edges_df, valid_targets):
        """
        Filters the targets in the edges DataFrame to include only valid targets.

        Parameters:
        edges_df (pd.DataFrame): DataFrame containing edge data.
        valid_targets (set): Set of valid target identifiers.

        Returns:
        pd.DataFrame: Filtered DataFrame with valid targets.
        """
        return edges_df[edges_df['target'].isin(valid_targets)]
