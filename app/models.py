from pydantic import BaseModel
from typing import List

class GrammarIssue(BaseModel):
    wrong: str
    corrected: str
    error_type: str

class GrammarCheckRequest(BaseModel):
    text: str

class GrammarCheckResponse(BaseModel):
    issues: List[GrammarIssue]

class HealthResponse(BaseModel):
    status: str
    ollama_connected: bool
