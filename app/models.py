from typing import List, Dict, Any, Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):

    message: str

    session_id: Optional[str] = None



class AMLResponse(BaseModel):

    response: str

    risk_score: float = 0

    risk_level: str = "LOW"

    action: str = ""

    tool_used: str = ""

    intent: str = ""

    recommendation: str = ""

    decision: str = ""

    evidence: List[Dict[str, Any]] = Field(
        default_factory=list
    )

    citations: List[Dict[str, Any]] = Field(
        default_factory=list
    )

    retrieval_trace: List[Dict[str, Any]] = Field(
        default_factory=list
    )



class HealthResponse(BaseModel):

    status: str

    uptime: str

    model: str

    version: str



class SourceResponse(BaseModel):

    doc_id: str

    chunks: int



class IngestResponse(BaseModel):

    job_id: str

    status: str



class EvaluationResponse(BaseModel):

    status: str

    score: float

    details: Dict[str, Any]