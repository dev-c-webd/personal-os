from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.users.models import User
from app.modules.workspaces.membership_models import WorkspaceMember
from app.modules.workspaces.models import Workspace
from app.modules.workspaces.schemas import WorkspaceCreate


def create_workspace(
    data: WorkspaceCreate,
    current_user: User,
    db: Session,
) -> Workspace:
    workspace = Workspace(
        name=data.name,
    )

    db.add(workspace)
    db.flush()

    membership = WorkspaceMember(
        workspace_id=workspace.id,
        user_id=current_user.id,
        role="owner",
    )

    db.add(membership)

    db.commit()
    db.refresh(workspace)

    return workspace

def get_workspace_by_id(
    workspace_id: UUID,
    db: Session,
) -> Workspace | None:
    return db.scalar(
        select(Workspace).where(Workspace.id == workspace_id)
    )


def get_user_workspaces(
        user_id:UUID,
        db: Session,
) -> list[Workspace]:

    statement = (
        select(Workspace)
        .join(
            WorkspaceMember,
            WorkspaceMember.workspace_id == Workspace.id
        )
        .where(WorkspaceMember.user_id == user_id,)
        .order_by(Workspace.created_at)
    )

    return list(db.scalars(statement).all())