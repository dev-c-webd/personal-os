from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PageSettingsUpdate(BaseModel):
    appearance: dict[str, Any] | None = None
    layout_config: dict[str, Any] | None = None
    behavior_config: dict[str, Any] | None = None


class PageSettingsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    page_id: UUID
    appearance: dict[str, Any]
    layout_config: dict[str, Any]
    behavior_config: dict[str, Any]
    created_at: datetime
    updated_at: datetime