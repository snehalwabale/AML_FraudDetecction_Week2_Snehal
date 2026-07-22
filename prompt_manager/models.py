from pydantic import BaseModel
from typing import List


class PromptMetadata(BaseModel):
    name: str
    version: str
    author: str
    model_compatibility: List[str]
    changelog: List[str]


class PromptTemplate(BaseModel):
    metadata: PromptMetadata
    input_variables: List[str]
    template: str


class PromptVersion(BaseModel):
    name: str
    version: str
    active: bool = False


class PromptActivationRequest(BaseModel):
    name: str
    version: str