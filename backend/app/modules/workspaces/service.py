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