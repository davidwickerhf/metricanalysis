import pandas as pd

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

    def filter_targets(self, edges_df, valid_targets, source_col='ecli', target_col='references'):
        """
        Filters the targets in the edges DataFrame to include only valid targets.

        Parameters:
        edges_df (pd.DataFrame): DataFrame containing edge data.
        valid_targets (set): Set of valid target identifiers.
        source_col (str): The column name for sources in the edges DataFrame.
        target_col (str): The column name for targets in the edges DataFrame.

        Returns:
        pd.DataFrame: Filtered DataFrame with valid targets.
        """
        filtered_edges = []
        for index, row in edges_df.iterrows():
            source = row[source_col]
            targets = row[target_col]
            filtered_targets = [target for target in targets if target in valid_targets]
            if filtered_targets:
                for target in filtered_targets:
                    filtered_edges.append((source, target))
        
        return pd.DataFrame(filtered_edges, columns=['source', 'target'])
