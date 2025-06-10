from fastapi import FastAPI, HTTPException, Query
from app.services import ExcelProcessor
from app.models import ListTablesResponse, TableDetailsResponse, RowSumResponse
import os

# --- Application Setup ---

# Define the path to the Excel file
# Using an absolute path relative to this file's location is robust
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCEL_FILE_PATH = os.path.join(BASE_DIR, "Data", "capbudg.xls")

# Initialize the FastAPI app
app = FastAPI(
    title="FastAPI Excel Processor",
    description="An API to read and process data from an Excel sheet.",
    version="1.0.0"
)

# --- Global Service Instantiation ---
# The Excel file is loaded once when the application starts up.
# This avoids re-reading the file on every request, making the API fast.
try:
    processor = ExcelProcessor(file_path=EXCEL_FILE_PATH)
except Exception as e:
    # If the file can't be loaded on startup, the app is not functional.
    # We can raise an error here to prevent the app from starting in a broken state.
    raise RuntimeError(f"Failed to initialize ExcelProcessor: {e}") from e


# --- API Endpoints ---

@app.get("/list_tables", 
         response_model=ListTablesResponse,
         summary="List all tables",
         tags=["Tables"])
async def list_tables():
    """
    Lists all the table names (sheets) present in the specified Excel file.
    """
    table_names = processor.list_table_names()
    return {"tables": table_names}


@app.get("/get_table_details", 
         response_model=TableDetailsResponse,
         summary="Get details of a specific table",
         tags=["Tables"])
async def get_table_details(
    table_name: str = Query(..., description="The name of the table to retrieve details for.")
):
    """
    Returns the names of the rows for the selected table.
    These row names are the values found in the first column of that table.
    """
    try:
        row_names = processor.get_row_names(table_name)
        return {"table_name": table_name, "row_names": row_names}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/row_sum", 
         response_model=RowSumResponse,
         summary="Calculate the sum of a row",
         tags=["Calculations"])
async def row_sum(
    table_name: str = Query(..., description="The name of the table containing the row."),
    row_name: str = Query(..., description="The name of the row to sum.")
):
    """
    Calculates and returns the sum of all numerical data points
    in the specified row of the specified table.
    """
    try:
        total_sum = processor.get_row_sum(table_name, row_name)
        return {"table_name": table_name, "row_name": row_name, "sum": total_sum}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
