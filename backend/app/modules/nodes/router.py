from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.modules.users.models import User
from app.modules.auth.dependencies import get_current_user
from app.modules.workspaces.dependencies import get_workspace_member

from app.modules.nodes.schemas import NodeCreate, NodeResponse, NodeUpdate, MoveNodeRequest
from app.modules.nodes.service import create_node, get_nodes, get_node_by_id, update_node, move_node


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
    current_user: User = Depends(get_current_user),
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