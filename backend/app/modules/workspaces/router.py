from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.users.models import User
from app.modules.workspaces.dependencies import get_workspace_member
from app.modules.workspaces.schemas import WorkspaceCreate, WorkspaceResponse
from app.modules.workspaces.service import (
    create_workspace,
    get_user_workspaces,
    get_workspace_by_id,
)


router = APIRouter(
    prefix="/api/v1/workspaces",
    tags=["workspaces"],
)


# create workspace
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


# get the workspace
@router.get(
    "/{workspace_id}",
    response_model=WorkspaceResponse,
)
def get_workspace(
    workspace_id: UUID,
    _membership=Depends(get_workspace_member),
    db: Session = Depends(get_db),
):
    workspace = get_workspace_by_id(workspace_id, db)

    if workspace is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )

    return workspace


@router.get("", response_model=list[WorkspaceResponse])
def list_workspaces(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_user_workspaces(current_user.id, db)