from pydantic import BaseModel
from typing import List


class RolePermission(BaseModel):

    role: str

    allowed_doc_types: List[str]

    description: str



class RoleContext(BaseModel):

    user_id: str

    username: str

    role: str



class AccessRequest(BaseModel):

    role: str

    doc_type: str



class AccessResponse(BaseModel):

    allowed: bool

    role: str

    doc_type: str

    reason: str



class DocumentMetadata(BaseModel):

    document_id: str

    document_name: str

    doc_type: str

    classification: str



class RoleConfig(BaseModel):

    roles: List[RolePermission]