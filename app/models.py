from typing import List, Dict, Any, Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):

    message: str

    session_id: Optional[str] = None


class AMLResponse(BaseModel):

    response: str

    risk_score: float = 0

    action: str = ""

    tool_used: str = ""

    citations: List[Dict[str, Any]] = []

    retrieval_trace: List[Dict[str, Any]] = []


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