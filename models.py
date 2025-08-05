from pydantic import BaseModel
from typing import List

class InputData(BaseModel):
    documents: str  # URL to the document (PDF, etc.)
    questions: List[str]  # List of natural language queries

class OutputData(BaseModel):
    answers: List[str]  # List of structured, explainable answers