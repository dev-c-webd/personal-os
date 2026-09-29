from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.nodes.models import Node
from app.modules.workspaces.models import Workspace
from app.modules.nodes.schemas import NodeCreate

def create_node(
    workspace_id: UUID,
    data,
    db: Session,
) -> Node:

    if data.parent_id is not None:
        parent = db.scalar(
            select(Node).where(
                Node.id == data.parent_id,
                Node.workspace_id == workspace_id,
            )
        )

        if parent is None:
            raise ValueError("Parent node not found")

    node = Node(
        workspace_id=workspace_id,
        parent_id=data.parent_id,
        name=data.name,
        type=data.type,
        sort_order=data.sort_order,
    )

    db.add(node)
    db.commit()
    db.refresh(node)

    return node

def get_nodes(
        workspace_id: UUID,
        parent_id: UUID | None,
        db: Session
) -> list[Node]:
    
    if parent_id is not None:
        parent = db.scalar(
            select(Node).where(
                Node.id == parent_id,
                Node.workspace_id == workspace_id,
            )
        )

        if parent is None:
            raise ValueError("Parent node not found")


    statement = (
        select(Node)
        .where(
            Node.workspace_id == workspace_id,
            Node.parent_id == parent_id,
        )
        .order_by(Node.sort_order, Node.created_at)
    )

    return list(db.scalars(statement).all())


def get_node_by_id(
    workspace_id: UUID,
    node_id: UUID,
    db: Session,
) -> Node | None:
    statement = select(Node).where(
        Node.id == node_id,
        Node.workspace_id == workspace_id,
    )

    return db.scalar(statement)
