import matplotlib.pyplot as plt
import seaborn as sns

class ErrorBarPlotter:
    """Class to generate error bar plots."""

    def plot_error_bars(self, data_df, measure, category):
        """
        Plots error bars for each centrality measure per ground truth category.

        Parameters:
        data_df (pd.DataFrame): DataFrame containing centrality measures and categories.
        measure (str): The centrality measure to plot.
        category (str): The ground truth category to plot.
        """
        sns.barplot(x=category, y=measure, data=data_df, ci="sd")
        plt.title(f'Error Bars for {measure} by {category}')
        plt.xlabel(category)
        plt.ylabel(measure)
        plt.show()
