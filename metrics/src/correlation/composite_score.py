class CompositeScoreCalculator:
    """Class to create composite scores from different centrality measures."""

    def create_composite_score(self, data_df, measures):
        """
        Creates a composite score from specified centrality measures.

        Parameters:
        data_df (pd.DataFrame): DataFrame containing centrality measures.
        measures (list): List of columns representing centrality measures.

        Returns:
        pd.DataFrame: DataFrame with an added composite score column.
        """
        data_df['composite_score'] = data_df[measures].mean(axis=1)
        return data_df
