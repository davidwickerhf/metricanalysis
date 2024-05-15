from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

class RegressionModel:
    """Class to perform regression analysis."""

    def perform_regression(self, data_df, target_column):
        """
        Performs regression analysis on the data.

        Parameters:
        data_df (pd.DataFrame): DataFrame containing the data.
        target_column (str): The target column for regression.

        Returns:
        dict: Dictionary containing regression results and performance metrics.
        """
        X = data_df.drop(columns=[target_column])
        y = data_df[target_column]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        
        report = classification_report(y_test, y_pred, output_dict=True)
        
        return {'model': model, 'report': report}
