from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.components.models import Component, ComponentPlacement
from app.modules.components.schemas import (
    ComponentPlacementCreate,
    ComponentPlacementUpdate,
)
from app.modules.nodes.models import Node


def _get_page(
    workspace_id: UUID,
    page_id: UUID,
    db: Session,
) -> Node | None:
    return db.scalar(
        select(Node).where(
            Node.id == page_id,
            Node.workspace_id == workspace_id,
        )
    )


def _get_component(
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


def _get_parent_placement(
    workspace_id: UUID,
    parent_placement_id: UUID,
    db: Session,
) -> ComponentPlacement | None:
    return db.scalar(
        select(ComponentPlacement).where(
            ComponentPlacement.id == parent_placement_id,
            ComponentPlacement.workspace_id == workspace_id,
        )
    )


def create_placement(
    workspace_id: UUID,
    data: ComponentPlacementCreate,
    db: Session,
) -> ComponentPlacement:
    page = _get_page(
        workspace_id,
        data.page_id,
        db,
    )

    if page is None:
        raise ValueError("Page not found")

    component = _get_component(
        workspace_id,
        data.component_id,
        db,
    )

    if component is None:
        raise ValueError("Component not found")

    parent_placement = None

    if data.parent_placement_id is not None:
        parent_placement = _get_parent_placement(
            workspace_id,
            data.parent_placement_id,
            db,
        )

        if parent_placement is None:
            raise ValueError("Parent placement not found")

        if parent_placement.page_id != data.page_id:
            raise ValueError(
                "Parent placement must belong to the same Page"
            )

    placement = ComponentPlacement(
        workspace_id=workspace_id,
        page_id=data.page_id,
        component_id=data.component_id,
        parent_placement_id=data.parent_placement_id,
        slot_key=data.slot_key,
        position=data.position,
        size=data.size,
        transform=data.transform,
        style=data.style,
        visible=data.visible,
        sort_order=data.sort_order,
    )

    db.add(placement)
    db.commit()
    db.refresh(placement)

    return placement


def get_placements_for_page(
    workspace_id: UUID,
    page_id: UUID,
    db: Session,
) -> list[ComponentPlacement]:
    page = _get_page(
        workspace_id,
        page_id,
        db,
    )

    if page is None:
        raise ValueError("Page not found")

    return list(
        db.scalars(
            select(ComponentPlacement)
            .where(
                ComponentPlacement.workspace_id == workspace_id,
                ComponentPlacement.page_id == page_id,
            )
            .order_by(
                ComponentPlacement.sort_order,
                ComponentPlacement.created_at,
            )
        )
    )


def get_placement_by_id(
    workspace_id: UUID,
    placement_id: UUID,
    db: Session,
) -> ComponentPlacement | None:
    return db.scalar(
        select(ComponentPlacement).where(
            ComponentPlacement.id == placement_id,
            ComponentPlacement.workspace_id == workspace_id,
        )
    )


def update_placement(
    workspace_id: UUID,
    placement_id: UUID,
    data: ComponentPlacementUpdate,
    db: Session,
) -> ComponentPlacement | None:
    placement = get_placement_by_id(
        workspace_id,
        placement_id,
        db,
    )

    if placement is None:
        return None

    if "parent_placement_id" in data.model_fields_set:
        if data.parent_placement_id is not None:
            if data.parent_placement_id == placement_id:
                raise ValueError(
                    "A placement cannot be its own parent"
                )

            parent_placement = _get_parent_placement(
                workspace_id,
                data.parent_placement_id,
                db,
            )

            if parent_placement is None:
                raise ValueError("Parent placement not found")

            if parent_placement.page_id != placement.page_id:
                raise ValueError(
                    "Parent placement must belong to the same Page"
                )

            ancestor_tree = (
                select(
                    ComponentPlacement.id,
                    ComponentPlacement.parent_placement_id,
                )
                .where(
                    ComponentPlacement.id == data.parent_placement_id,
                    ComponentPlacement.workspace_id == workspace_id,
                )
                .cte(
                    name="placement_ancestor_tree",
                    recursive=True,
                )
            )

            ancestor_tree = ancestor_tree.union_all(
                select(
                    ComponentPlacement.id,
                    ComponentPlacement.parent_placement_id,
                )
                .where(
                    ComponentPlacement.id
                    == ancestor_tree.c.parent_placement_id,
                    ComponentPlacement.workspace_id == workspace_id,
                )
            )

            cycle_exists = db.scalar(
                select(ancestor_tree.c.id).where(
                    ancestor_tree.c.id == placement_id
                )
            )

            if cycle_exists is not None:
                raise ValueError(
                    "Cannot move a placement under its descendant"
                )

        placement.parent_placement_id = data.parent_placement_id

    if "slot_key" in data.model_fields_set:
        placement.slot_key = data.slot_key

    if data.position is not None:
        placement.position = data.position

    if data.size is not None:
        placement.size = data.size

    if data.transform is not None:
        placement.transform = data.transform

    if data.style is not None:
        placement.style = data.style

    if data.visible is not None:
        placement.visible = data.visible

    if data.sort_order is not None:
        placement.sort_order = data.sort_order

    db.commit()
    db.refresh(placement)

    return placement


def delete_placement(
    workspace_id: UUID,
    placement_id: UUID,
    db: Session,
) -> bool:
    placement = get_placement_by_id(
        workspace_id,
        placement_id,
        db,
    )

    if placement is None:
        return False

    db.delete(placement)
    db.commit()

    return True