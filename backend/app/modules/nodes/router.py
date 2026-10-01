from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.modules.workspaces.dependencies import get_workspace_member

# nodes(pages now) import
from app.modules.nodes.schemas import ( NodeCreate, NodeResponse, NodeUpdate, MoveNodeRequest )
from app.modules.nodes.service import ( create_node, get_nodes, get_node_by_id, update_node, move_node, delete_node )

# page settings imports
from app.modules.nodes.page_settings_schemas import (
    PageSettingsResponse,
    PageSettingsUpdate,
)
from app.modules.nodes.page_settings_service import (
    get_or_create_page_settings,
    update_page_settings,
)


# nodes (now pages) routes

router = APIRouter(
    prefix="/api/v1/workspaces/{workspace_id}/nodes",
    tags=["nodes"],
)


@router.post(
    "",
    response_model=NodeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    workspace_id: UUID,
    data: NodeCreate,
    _membership=Depends(get_workspace_member),
    db: Session = Depends(get_db),
):
    try:
        return create_node(workspace_id, data, db)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get("", response_model=list[NodeResponse])

def list_nodes(
    workspace_id: UUID,
    parent_id: UUID | None = None,
    _membership=Depends(get_workspace_member),
    db: Session = Depends(get_db),
):
    try:
        return get_nodes(workspace_id, parent_id, db)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get("/{node_id}", response_model=NodeResponse)
def get_node(
    workspace_id: UUID,
    node_id: UUID,
    _membership=Depends(get_workspace_member),
    db: Session = Depends(get_db),
):
    node = get_node_by_id(workspace_id, node_id, db)

    if node is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Node not found",
        )

    return node


@router.patch("/{node_id}", response_model=NodeResponse)
def update(
    workspace_id: UUID,
    node_id: UUID,
    data: NodeUpdate,
    _membership=Depends(get_workspace_member),
    db: Session = Depends(get_db),
):
    node = update_node(workspace_id, node_id, data, db)

    if node is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Node not found",
        )

    return node


@router.patch("/{node_id}/move", response_model=NodeResponse)
def move(
    workspace_id: UUID,
    node_id: UUID,
    data: MoveNodeRequest,
    _membership=Depends(get_workspace_member),
    db: Session = Depends(get_db),
):
    try:
        return move_node(
            workspace_id,
            node_id,
            data.parent_id,
            db,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.delete("/{node_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    workspace_id: UUID,
    node_id: UUID,
    _membership=Depends(get_workspace_member),
    db: Session = Depends(get_db),
):
    deleted = delete_node(workspace_id, node_id, db)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Node not found",
        )


# page setting routes

@router.get(
    "/{page_id}/settings",
    response_model=PageSettingsResponse,
)
def get_settings(
    workspace_id: UUID,
    page_id: UUID,
    db: Session = Depends(get_db),
    _membership=Depends(get_workspace_member),
):
    settings = get_or_create_page_settings(
        workspace_id=workspace_id,
        page_id=page_id,
        db=db,
    )

    if settings is None:
        raise HTTPException(
            status_code=404,
            detail="Page not found",
        )

    return settings


@router.patch(
    "/{page_id}/settings",
    response_model=PageSettingsResponse,
)
def update_settings(
    workspace_id: UUID,
    page_id: UUID,
    data: PageSettingsUpdate,
    db: Session = Depends(get_db),
    _membership=Depends(get_workspace_member),
):
    settings = update_page_settings(
        workspace_id=workspace_id,
        page_id=page_id,
        data=data,
        db=db,
    )

    if settings is None:
        raise HTTPException(
            status_code=404,
            detail="Page not found",
        )

    return settings