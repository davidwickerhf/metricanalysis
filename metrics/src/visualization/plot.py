import matplotlib.pyplot as plt
import seaborn as sns

class PlotGenerator:
    """Class to generate various plots for data visualization."""

    def plot_centrality_distribution(self, data_df, measure):
        """
        Plots the distribution of a centrality measure.

        Parameters:
        data_df (pd.DataFrame): DataFrame containing centrality measures.
        measure (str): The centrality measure to plot.
        """
        sns.histplot(data_df[measure])
        plt.title(f'Distribution of {measure}')
        plt.xlabel(measure)
        plt.ylabel('Frequency')
        plt.show()

    def plot_correlation_matrix(self, correlation_matrix):
        """
        Plots a correlation matrix.

        Parameters:
        correlation_matrix (pd.DataFrame): The correlation matrix to plot.
        """
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
        plt.title('Correlation Matrix')
        plt.show()
