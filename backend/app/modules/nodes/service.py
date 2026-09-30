from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.nodes.models import Node
from app.modules.workspaces.models import Workspace
from app.modules.nodes.schemas import NodeCreate, NodeUpdate

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

def update_node(
        workspace_id:UUID,
        node_id:UUID,
        data:NodeUpdate,
        db:Session
) -> Node | None:

    node = db.scalar(
        select(Node).where(
            Node.id == node_id,
            Node.workspace_id == workspace_id
        )
    )

    if node is None:
        return None

    if data.name is not None:
        node.name = data.name

    if data.sort_order is not None:
        node.sort_order = data.sort_order

    db.commit()
    db.refresh(node)

    return node
    

def move_node(
    workspace_id: UUID,
    node_id: UUID,
    new_parent_id: UUID | None,
    db: Session,
) -> Node:
    node = db.scalar(
        select(Node).where(
            Node.id == node_id,
            Node.workspace_id == workspace_id,
        )
    )

    if node is None:
        raise ValueError("Node not found")

    if new_parent_id is None:
        node.parent_id = None

        db.commit()
        db.refresh(node)

        return node

    new_parent = db.scalar(
        select(Node).where(
            Node.id == new_parent_id,
            Node.workspace_id == workspace_id,
        )
    )

    if new_parent is None:
        raise ValueError("Parent node not found")

    if new_parent_id == node_id:
        raise ValueError("A node cannot be its own parent")

    ancestor_id = new_parent.parent_id

    while ancestor_id is not None:
        if ancestor_id == node_id:
            raise ValueError("Cannot move a node under its descendant")

        ancestor = db.scalar(
            select(Node).where(
                Node.id == ancestor_id,
                Node.workspace_id == workspace_id,
            )
        )

        if ancestor is None:
            raise ValueError("Invalid node hierarchy")

        ancestor_id = ancestor.parent_id

    node.parent_id = new_parent_id

    db.commit()
    db.refresh(node)

    return node