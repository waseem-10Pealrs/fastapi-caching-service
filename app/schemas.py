from pydantic import BaseModel
from typing import List

# Schema for validating input payload
# Why Pydantic? Built-in data validation and serialization with type hints reduce errors and ensure correctness.
class PayloadRequest(BaseModel):
    list_1: List[str]  # First list of strings
    list_2: List[str]  # Second list of strings

# Schema for output payload
class PayloadResponse(BaseModel):
    id: str  # Unique identifier for the payload
    output: str  # Generated interleaved payload
