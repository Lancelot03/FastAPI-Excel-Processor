from pydantic import BaseModel
from typing import List, Union

class ListTablesResponse(BaseModel):
    tables: List[str]

class TableDetailsResponse(BaseModel):
    table_name: str
    row_names: List[str]

class RowSumResponse(BaseModel):
    table_name: str
    row_name: str
    sum: Union[int, float]
