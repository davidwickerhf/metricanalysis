import matplotlib.pyplot as plt
import seaborn as sns
import utils.logger as logger


class PlotGenerator:
    """Class to generate various plots for data visualization."""

    def __init__(self):
        logger.basicConfig(level=logger.INFO)

    def plot_correlation(self, data_df, x_col, y_col, output_path):
        """
        Plots the correlation between two columns.

        Parameters:
        - data_df (pd.DataFrame): DataFrame containing the data.
        - x_col (str): The column name for the x-axis (e.g., centrality measure).
        - y_col (str): The column name for the y-axis (e.g., ground truth measure).
        - output_path (str): Path to save the plot.
        """
        try:
            logger.info(f"Generating correlation plot for {x_col} vs {y_col}")
            plt.figure(figsize=(10, 6))
            sns.regplot(x=x_col, y=y_col, data=data_df, scatter_kws={'s':10}, line_kws={"color":"r","alpha":0.7,"lw":2})
            plt.title(f'Correlation between {x_col} and {y_col}')
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.grid(True)
            plt.savefig(output_path)
            plt.close()
            logger.info(f"Plot saved to {output_path}")
        except Exception as e:
            logger.error(f"Failed to generate plot for {x_col} vs {y_col}: {e}")