from pydantic import BaseModel


class ChatRequest(BaseModel):

    message: str


class AMLResponse(BaseModel):

    response: str

    risk_score: int = 0

    action: str = "Review"

    tool_used: str = "None"


class HealthResponse(BaseModel):

    status: str

    uptime: str

    model: str

    version: str