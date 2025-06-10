import pandas as pd
from typing import List, Dict, Union

class ExcelProcessor:
    """
    A service class to handle all logic related to reading and processing
    the Excel file.
    """
    def __init__(self, file_path: str):
        """
        Initializes the processor by loading all sheets from the Excel file
        into pandas DataFrames. This is done once to avoid repeated file I/O.
        
        Args:
            file_path (str): The path to the .xls file.
        
        Raises:
            FileNotFoundError: If the Excel file cannot be found at the given path.
        """
        try:
            # sheet_name=None reads all sheets into a dictionary of DataFrames
            self.data_frames: Dict[str, pd.DataFrame] = pd.read_excel(file_path, sheet_name=None)
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: The file at {file_path} was not found.")
        except Exception as e:
            raise Exception(f"An error occurred while reading the Excel file: {e}")

    def list_table_names(self) -> List[str]:
        """
        Returns a list of all table (sheet) names in the Excel file.
        """
        return list(self.data_frames.keys())

    def get_row_names(self, table_name: str) -> List[str]:
        """
        Retrieves the names of rows from the first column of a specified table.
        
        Args:
            table_name (str): The name of the table (sheet).
            
        Returns:
            A list of strings representing the row names.
            
        Raises:
            ValueError: If the table_name does not exist.
        """
        if table_name not in self.data_frames:
            raise ValueError(f"Table '{table_name}' not found in the Excel file.")
            
        df = self.data_frames[table_name]
        
        if df.empty or df.shape[1] == 0:
            return []
            
        # Return values from the first column, dropping any empty (NaN) cells.
        return df.iloc[:, 0].dropna().tolist()

    def get_row_sum(self, table_name: str, row_name: str) -> Union[int, float]:
        """
        Calculates the sum of all numerical values in a specific row of a given table.
        
        Args:
            table_name (str): The name of the table (sheet).
            row_name (str): The name of the row (found in the first column).
            
        Returns:
            The sum of numerical values in that row.
            
        Raises:
            ValueError: If the table or row does not exist.
        """
        if table_name not in self.data_frames:
            raise ValueError(f"Table '{table_name}' not found.")
            
        df = self.data_frames[table_name]
        
        # Find the row where the first column matches the given row_name.
        target_row = df[df.iloc[:, 0] == row_name]
        
        if target_row.empty:
            raise ValueError(f"Row '{row_name}' not found in table '{table_name}'.")
            
        # Extract the values from the first matching row
        row_values = target_row.iloc[0].values
        
        # Sum only the values that are numeric (int or float)
        # This elegantly ignores strings, NaNs, and other non-numeric types.
        total_sum = sum(val for val in row_values if isinstance(val, (int, float)))
        
        return total_sum
