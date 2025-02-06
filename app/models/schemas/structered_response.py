from pydantic import BaseModel
from typing import Any, Optional

class StructuredResponse(BaseModel):
    data: Optional[Any] = None  
    status_code: int
    detail: str
    error: Optional[Any] = None 