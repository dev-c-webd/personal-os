from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ComponentCreate(BaseModel):
    definition_key: str = Field(min_length=1, max_length=255)
    config: dict[str, Any] = Field(default_factory=dict)
    binding: dict[str, Any] | None = None


class ComponentUpdate(BaseModel):
    definition_key: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    config: dict[str, Any] | None = None
    binding: dict[str, Any] | None = None


class ComponentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    workspace_id: UUID
    definition_key: str
    config: dict[str, Any]
    binding: dict[str, Any] | None
    created_at: datetime
    updated_at: datetime


class ComponentPlacementCreate(BaseModel):
    page_id: UUID
    component_id: UUID
    parent_placement_id: UUID | None = None
    slot_key: str | None = Field(
        default=None,
        max_length=255,
    )
    position: dict[str, Any] = Field(default_factory=dict)
    size: dict[str, Any] = Field(default_factory=dict)
    transform: dict[str, Any] = Field(default_factory=dict)
    style: dict[str, Any] = Field(default_factory=dict)
    visible: bool = True
    sort_order: int = 0


class ComponentPlacementUpdate(BaseModel):
    parent_placement_id: UUID | None = None
    slot_key: str | None = Field(
        default=None,
        max_length=255,
    )
    position: dict[str, Any] | None = None
    size: dict[str, Any] | None = None
    transform: dict[str, Any] | None = None
    style: dict[str, Any] | None = None
    visible: bool | None = None
    sort_order: int | None = None


class ComponentPlacementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    workspace_id: UUID
    page_id: UUID
    component_id: UUID
    parent_placement_id: UUID | None
    slot_key: str | None
    position: dict[str, Any]
    size: dict[str, Any]
    transform: dict[str, Any]
    style: dict[str, Any]
    visible: bool
    sort_order: int
    created_at: datetime
    updated_at: datetime