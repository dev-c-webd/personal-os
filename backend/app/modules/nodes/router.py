from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.nodes.schemas import NodeCreate, NodeResponse
from app.modules.nodes.service import create_node
from app.modules.users.models import User
from app.modules.workspaces.dependencies import get_workspace_member

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