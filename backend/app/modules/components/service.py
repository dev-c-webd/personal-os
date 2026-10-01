from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.components.models import Component
from app.modules.components.schemas import ComponentCreate, ComponentUpdate


def create_component(
    workspace_id: UUID,
    data: ComponentCreate,
    db: Session,
) -> Component:
    component = Component(
        workspace_id=workspace_id,
        definition_key=data.definition_key,
        config=data.config,
        binding=data.binding,
    )

    db.add(component)
    db.commit()
    db.refresh(component)

    return component


def get_components(
    workspace_id: UUID,
    db: Session,
) -> list[Component]:
    return list(
        db.scalars(
            select(Component)
            .where(Component.workspace_id == workspace_id)
            .order_by(Component.created_at)
        )
    )


def get_component_by_id(
    workspace_id: UUID,
    component_id: UUID,
    db: Session,
) -> Component | None:
    return db.scalar(
        select(Component).where(
            Component.id == component_id,
            Component.workspace_id == workspace_id,
        )
    )


def update_component(
    workspace_id: UUID,
    component_id: UUID,
    data: ComponentUpdate,
    db: Session,
) -> Component | None:
    component = get_component_by_id(
        workspace_id,
        component_id,
        db,
    )

    if component is None:
        return None

    if data.definition_key is not None:
        component.definition_key = data.definition_key

    if data.config is not None:
        component.config = data.config

    if data.binding is not None:
        component.binding = data.binding

    db.commit()
    db.refresh(component)

    return component


def delete_component(
    workspace_id: UUID,
    component_id: UUID,
    db: Session,
) -> bool:
    component = get_component_by_id(
        workspace_id,
        component_id,
        db,
    )

    if component is None:
        return False

    db.delete(component)
    db.commit()

    return True