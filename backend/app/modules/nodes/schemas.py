from uuid import UUID

from pydantic import BaseModel, Field


class NodeCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    parent_id: UUID | None = None
    sort_order: int = 0


class NodeResponse(BaseModel):
    id: UUID
    workspace_id: UUID
    parent_id: UUID | None
    name: str
    sort_order: int


class NodeUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    sort_order: int | None = None


class MoveNodeRequest(BaseModel):
    parent_id: UUID | None