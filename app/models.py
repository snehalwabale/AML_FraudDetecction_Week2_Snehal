from pydantic import BaseModel


# =====================================================
# REQUEST MODEL
# =====================================================

class ChatRequest(BaseModel):

    message: str


# =====================================================
# RESPONSE MODEL
# =====================================================

class AMLResponse(BaseModel):

    response: str

    risk_score: int = 0

    action: str = "Review"

    tool_used: str = "None"


# =====================================================
# HEALTH MODEL
# =====================================================

class HealthResponse(BaseModel):

    status: str

    uptime: str

    model: str

    version: str