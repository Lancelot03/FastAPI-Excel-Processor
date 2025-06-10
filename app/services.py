import pandas as pd
from typing import List, Dict, Union
import numpy as np

class ExcelProcessor:
    """
    A service class to handle all logic related to reading and processing
    the Excel file. This version uses a robust row-by-row parsing strategy
    and handles duplicate table names by keeping only the first instance.
    """
    def __init__(self, file_path: str):
        self.tables: Dict[str, pd.DataFrame] = self._parse_sheet_into_tables(file_path)

    def _parse_sheet_into_tables(self, file_path: str) -> Dict[str, pd.DataFrame]:
        """
        Parses a single Excel sheet to find and extract multiple tables.
        It identifies a table by a title row (first cell is all-caps) and
        ignores any subsequent tables with a name that has already been seen.
        """
        try:
            df = pd.read_excel(file_path, sheet_name=0, header=None)
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: The file at {file_path} was not found.")
        except Exception as e:
            raise Exception(f"An error occurred while reading the Excel file: {e}")

        tables = {}
        current_table_rows = []
        current_table_name = None

        for index, row in df.iterrows():
            first_cell_value = row.iloc[0]
            is_blank_row = row.isnull().all()

            is_title_row = (
                isinstance(first_cell_value, str) and
                first_cell_value.isupper()
            )

            if is_title_row:
                # First, finalize the PREVIOUS table if it exists and is not a duplicate.
                if current_table_name and current_table_rows:
                    # *** FIX: Only add the table if its name is not already taken ***
                    if current_table_name not in tables:
                        tables[current_table_name] = pd.DataFrame(current_table_rows)

                # Start the NEW table
                current_table_name = first_cell_value.strip()
                current_table_rows = []
            
            elif is_blank_row:
                # On a blank row, finalize the current table (if it's not a duplicate)
                if current_table_name and current_table_rows:
                    if current_table_name not in tables:
                        tables[current_table_name] = pd.DataFrame(current_table_rows)
                
                # Reset for the next section
                current_table_name = None
                current_table_rows = []

            elif current_table_name and not is_blank_row and first_cell_value is not np.nan:
                # If we are inside a table, append the current row's data.
                current_table_rows.append(row)

        # After the loop, save the very last table if it exists and is not a duplicate
        if current_table_name and current_table_rows:
            if current_table_name not in tables:
                tables[current_table_name] = pd.DataFrame(current_table_rows)
        
        for name, table_df in tables.items():
            table_df.columns = range(table_df.shape[1])
            tables[name] = table_df.reset_index(drop=True)

        return tables

    def list_table_names(self) -> List[str]:
        return list(self.tables.keys())

    def get_row_names(self, table_name: str) -> List[str]:
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' not found. Available tables: {self.list_table_names()}")
        df = self.tables[table_name]
        return df.iloc[:, 0].dropna().astype(str).tolist()

    def get_row_sum(self, table_name: str, row_name: str) -> Union[int, float]:
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' not found.")
        df = self.tables[table_name]
        target_row = df[df.iloc[:, 0].astype(str).str.strip() == row_name.strip()]
        if target_row.empty:
            raise ValueError(f"Row '{row_name}' not found in table '{table_name}'.")

        row_values = target_row.iloc[0].values
        total_sum = 0
        for val in row_values:
            if isinstance(val, (int, float)) and not np.isnan(val):
                total_sum += val
            elif isinstance(val, str):
                cleaned_val = val.replace('$', '').replace(',', '').replace('%', '').strip()
                try:
                    total_sum += float(cleaned_val)
                except (ValueError, TypeError):
                    continue
        return total_sum
