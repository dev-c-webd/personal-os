from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modules.components.placement_service import (
    create_placement,
    delete_placement,
    get_placement_by_id,
    get_placements_for_page,
    update_placement,
)
from app.modules.components.schemas import (
    ComponentCreate,
    ComponentPlacementCreate,
    ComponentPlacementResponse,
    ComponentPlacementUpdate,
    ComponentResponse,
    ComponentUpdate,
)
from app.modules.components.service import (
    create_component,
    delete_component,
    get_component_by_id,
    get_components,
    update_component,
)
from app.modules.workspaces.dependencies import get_workspace_member


router = APIRouter(
    prefix="/api/v1/workspaces/{workspace_id}/components",
    tags=["components"],
)


# ---------------------------------------------------------
# Placement routes
# ---------------------------------------------------------
# These are intentionally defined before /{component_id}
# so "placements" is not interpreted as a component UUID.


@router.post(
    "/placements",
    response_model=ComponentPlacementResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_component_placement(
    workspace_id: UUID,
    data: ComponentPlacementCreate,
    _membership=Depends(get_workspace_member),
    db: Session = Depends(get_db),
):
    try:
        return create_placement(
            workspace_id,
            data,
            db,
        )
    except ValueError as exc:
        message = str(exc)

        if message.endswith("not found"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message,
            ) from exc

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        ) from exc


@router.get(
    "/placements",
    response_model=list[ComponentPlacementResponse],
)
def list_component_placements(
    workspace_id: UUID,
    page_id: UUID = Query(...),
    _membership=Depends(get_workspace_member),
    db: Session = Depends(get_db),
):
    try:
        return get_placements_for_page(
            workspace_id,
            page_id,
            db,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/placements/{placement_id}",
    response_model=ComponentPlacementResponse,
)
def get_component_placement(
    workspace_id: UUID,
    placement_id: UUID,
    _membership=Depends(get_workspace_member),
    db: Session = Depends(get_db),
):
    placement = get_placement_by_id(
        workspace_id,
        placement_id,
        db,
    )

    if placement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Placement not found",
        )

    return placement


@router.patch(
    "/placements/{placement_id}",
    response_model=ComponentPlacementResponse,
)
def update_component_placement(
    workspace_id: UUID,
    placement_id: UUID,
    data: ComponentPlacementUpdate,
    _membership=Depends(get_workspace_member),
    db: Session = Depends(get_db),
):
    try:
        placement = update_placement(
            workspace_id,
            placement_id,
            data,
            db,
        )
    except ValueError as exc:
        message = str(exc)

        if message.endswith("not found"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message,
            ) from exc

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        ) from exc

    if placement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Placement not found",
        )

    return placement


@router.delete(
    "/placements/{placement_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_component_placement(
    workspace_id: UUID,
    placement_id: UUID,
    _membership=Depends(get_workspace_member),
    db: Session = Depends(get_db),
):
    deleted = delete_placement(
        workspace_id,
        placement_id,
        db,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Placement not found",
        )


# ---------------------------------------------------------
# Component routes
# ---------------------------------------------------------


@router.post(
    "",
    response_model=ComponentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_component_route(
    workspace_id: UUID,
    data: ComponentCreate,
    _membership=Depends(get_workspace_member),
    db: Session = Depends(get_db),
):
    return create_component(
        workspace_id,
        data,
        db,
    )


@router.get(
    "",
    response_model=list[ComponentResponse],
)
def list_component_route(
    workspace_id: UUID,
    _membership=Depends(get_workspace_member),
    db: Session = Depends(get_db),
):
    return get_components(
        workspace_id,
        db,
    )


@router.get(
    "/{component_id}",
    response_model=ComponentResponse,
)
def get_component_route(
    workspace_id: UUID,
    component_id: UUID,
    _membership=Depends(get_workspace_member),
    db: Session = Depends(get_db),
):
    component = get_component_by_id(
        workspace_id,
        component_id,
        db,
    )

    if component is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Component not found",
        )

    return component


@router.patch(
    "/{component_id}",
    response_model=ComponentResponse,
)
def update_component_route(
    workspace_id: UUID,
    component_id: UUID,
    data: ComponentUpdate,
    _membership=Depends(get_workspace_member),
    db: Session = Depends(get_db),
):
    component = update_component(
        workspace_id,
        component_id,
        data,
        db,
    )

    if component is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Component not found",
        )

    return component


@router.delete(
    "/{component_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_component_route(
    workspace_id: UUID,
    component_id: UUID,
    _membership=Depends(get_workspace_member),
    db: Session = Depends(get_db),
):
    deleted = delete_component(
        workspace_id,
        component_id,
        db,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Component not found",
        )