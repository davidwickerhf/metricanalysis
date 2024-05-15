import pandas as pd
import json

class FileReader:
    """Class to handle reading of different file formats."""

    def read_json(self, file_path):
        """
        Reads a JSON file and returns a DataFrame.

        Parameters:
        file_path (str): Path to the JSON file.

        Returns:
        pd.DataFrame: DataFrame containing the data.
        """
        with open(file_path, 'r') as f:
            data = json.load(f)
        return pd.DataFrame(data)

    def read_csv(self, file_path):
        """
        Reads a CSV file and returns a DataFrame.

        Parameters:
        file_path (str): Path to the CSV file.

        Returns:
        pd.DataFrame: DataFrame containing the data.
        """
        return pd.read_csv(file_path)

    def read_excel(self, file_path):
        """
        Reads an Excel file and returns a DataFrame.

        Parameters:
        file_path (str): Path to the Excel file.

        Returns:
        pd.DataFrame: DataFrame containing the data.
        """
        return pd.read_excel(file_path)