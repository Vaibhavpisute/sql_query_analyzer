from pydantic import BaseModel, Field
from typing import List

class QueryRequest(BaseModel):
    query: str
    database_type: str = "postgresql"

class AnalysisResponse(BaseModel):
    query: str
    issues: List[str]
    cost_estimate: float
    optimization_tips: List[str]
    execution_time_ms: float
    cached: bool = False