# hitl/models.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class HITLTask(BaseModel):

    task_id: str

    trigger: str

    query: str

    recommendation: str

    role: str = "analyst"

    status: str = "PENDING"

    created_at: datetime = datetime.now()

    decision: Optional[str] = None

    reviewer_comments: Optional[str] = None