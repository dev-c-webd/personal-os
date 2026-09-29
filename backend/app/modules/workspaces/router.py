from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.users.models import User
from app.modules.workspaces.dependencies import get_workspace_member
from app.modules.workspaces.models import Workspace
from app.modules.workspaces.schemas import WorkspaceCreate, WorkspaceResponse
from app.modules.workspaces.service import create_workspace


router = APIRouter(
    prefix="/api/v1/workspaces",
    tags=["workspaces"],
)

@router.post(
    "",
    response_model=WorkspaceResponse,
    status_code=status.HTTP_201_CREATED,
)

def create(
    data : WorkspaceCreate,
    current_user: User =  Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_workspace(data, current_user, db)



@router.get(
    "/{workspace_id}",
    response_model=WorkspaceResponse,
)
def get_workspace(
    workspace_id: UUID,
    membership=Depends(get_workspace_member),
    db: Session = Depends(get_db),
):
    workspace = db.scalar(
        select(Workspace).where(Workspace.id == workspace_id)
    )

    if workspace is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )

    return workspace