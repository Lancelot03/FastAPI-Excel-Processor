# FastAPI Excel

This is a Python-based API built with FastAPI that reads and processes data from a complex Excel file. It intelligently identifies distinct tables within a single spreadsheet and exposes several API endpoints to list these tables, view their contents, and perform calculations.

This project was developed to fulfill the "FastAPI Excel Assignment".

## Features

-   Parses a single Excel sheet containing multiple visually separated tables.
-   Handles duplicate table names by prioritizing the first instance.
-   Lists all identified tables from the sheet.
-   Displays row details for a specific table.
-   Calculates the numerical sum of a specific row, intelligently handling strings like currency (`$`) and percentages (`%`).

## Tech Stack

-   **FastAPI**: For building the high-performance API.
-   **Pandas**: For robust and efficient parsing of the Excel file.
-   **Uvicorn**: As the ASGI server to run the application.
-   **Python 3**

## Setup and Installation

Follow these steps to get the project running on your local machine.

**1. Clone the repository:**
```bash
git clone <your-repo-url>
cd fastapi-excel-processor
```

**2. Create and activate a virtual environment:**

-   For Windows:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
-   For macOS/Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

**3. Install the required dependencies:**
```bash
pip install -r requirements.txt
```

## How to Run the Application

Once the setup is complete, run the following command to start the server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 9090 --reload
```

The application will now be available at `http://localhost:9090`.

Interactive API documentation (Swagger UI) is also available at `http://localhost:9090/docs`.

## API Endpoints

You can test the endpoints using `curl` or any API client.

#### 1. List All Tables

Lists all the table names identified in the Excel file.

```bash
curl -X GET "http://localhost:9090/list_tables"
```

#### 2. Get Table Details

Returns the names of the rows for a selected table.

```bash
curl -X GET "http://localhost:9090/get_table_details?table_name=INITIAL%20INVESTMENT"
```

#### 3. Calculate Row Sum

Calculates the sum of all numerical data points in a specified row.

```bash
curl -X GET "http://localhost:9090/row_sum?table_name=INITIAL%20INVESTMENT&row_name=Tax%20Credit%20(if%20any%20)="
```

## Testing with Postman

A Postman collection has been provided for easy testing of all endpoints.

-   **[Click here to view the Postman Collection](https://harsh-7198357.postman.co/workspace/Harsh's-Workspace~1caff325-ac78-4e93-84c4-0c420a989929/collection/45775785-a7ba6fd7-8465-44df-83c9-78e14c247df8?action=share&creator=45775785)**
