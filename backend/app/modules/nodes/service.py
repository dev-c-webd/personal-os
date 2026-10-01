from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app.modules.nodes.models import Node
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

    ancestor_tree = (
        select(Node.id, Node.parent_id)
        .where(
            Node.id == new_parent_id,
            Node.workspace_id == workspace_id,
        )
        .cte(name="ancestor_tree", recursive=True)
    )

    ancestor_tree = ancestor_tree.union_all(
        select(Node.id, Node.parent_id)
        .where(
            Node.id == ancestor_tree.c.parent_id,
            Node.workspace_id == workspace_id,
        )
    )

    cycle_exists = db.scalar(
        select(ancestor_tree.c.id).where(
            ancestor_tree.c.id == node_id
        )
    )

    if cycle_exists is not None:
        raise ValueError("Cannot move a node under its descendant")

    node.parent_id = new_parent_id

    db.commit()
    db.refresh(node)

    return node


def delete_node(
    workspace_id: UUID,
    node_id: UUID,
    db: Session,
) -> bool:
    descendants = (
        select(Node.id)
        .where(
            Node.id == node_id,
            Node.workspace_id == workspace_id,
        )
        .cte(name="node_tree", recursive=True)
    )

    descendants = descendants.union_all(
        select(Node.id)
        .where(
            Node.parent_id == descendants.c.id,
            Node.workspace_id == workspace_id,
        )
    )

    statement = delete(Node).where(
        Node.workspace_id == workspace_id,
        Node.id.in_(select(descendants.c.id)),
    )

    result = db.execute(statement)
    db.commit()

    return result.rowcount > 0