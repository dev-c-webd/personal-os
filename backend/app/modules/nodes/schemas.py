from uuid import UUID
from typing import Literal

from pydantic import BaseModel, Field

NodeType = Literal["folder", "file", "note", "task", "goal"]

class NodeCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    type: NodeType
    parent_id: UUID | None = None
    sort_order: int = 0

class NodeResponse(BaseModel):
    id: UUID
    workspace_id: UUID
    parent_id: UUID | None
    name: str
    type: NodeType
    sort_order: int