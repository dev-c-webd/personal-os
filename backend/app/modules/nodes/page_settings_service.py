from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.nodes.models import Node
from app.modules.nodes.page_settings_models import PageSettings
from app.modules.nodes.page_settings_schemas import PageSettingsUpdate


def get_or_create_page_settings(
    workspace_id: UUID,
    page_id: UUID,
    db: Session,
) -> PageSettings | None:
    page = db.scalar(
        select(Node).where(
            Node.id == page_id,
            Node.workspace_id == workspace_id,
        )
    )

    if page is None:
        return None

    settings = db.get(PageSettings, page_id)

    if settings is None:
        settings = PageSettings(
            page_id=page_id,
            appearance={},
            layout_config={},
            behavior_config={},
        )
        db.add(settings)
        db.commit()
        db.refresh(settings)

    return settings


def update_page_settings(
    workspace_id: UUID,
    page_id: UUID,
    data: PageSettingsUpdate,
    db: Session,
) -> PageSettings | None:
    settings = get_or_create_page_settings(
        workspace_id,
        page_id,
        db,
    )

    if settings is None:
        return None

    if data.appearance is not None:
        settings.appearance = data.appearance

    if data.layout_config is not None:
        settings.layout_config = data.layout_config

    if data.behavior_config is not None:
        settings.behavior_config = data.behavior_config

    db.commit()
    db.refresh(settings)

    return settings