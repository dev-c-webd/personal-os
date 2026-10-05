import pytest

from app.modules.nodes.models import Node
from app.modules.nodes.service import move_node
from app.modules.workspaces.models import Workspace


def test_page_move_cannot_create_cycle(db_session):
    workspace = Workspace(name="Hierarchy Test Workspace")

    db_session.add(workspace)
    db_session.flush()

    root = Node(
        workspace_id=workspace.id,
        name="Root",
    )

    child = Node(
        workspace_id=workspace.id,
        name="Child",
    )

    db_session.add_all([root, child])
    db_session.flush()

    child.parent_id = root.id
    db_session.flush()

    with pytest.raises(ValueError, match="descendant"):
        move_node(
            workspace.id,
            root.id,
            child.id,
            db_session,
        )


def test_page_move_cannot_use_parent_from_another_workspace(db_session):
    from app.modules.nodes.service import move_node

    workspace_a = Workspace(name="Workspace A")
    workspace_b = Workspace(name="Workspace B")

    db_session.add_all([workspace_a, workspace_b])
    db_session.flush()

    page_a = Node(
        workspace_id=workspace_a.id,
        name="Page A",
    )

    page_b = Node(
        workspace_id=workspace_b.id,
        name="Page B",
    )

    db_session.add_all([page_a, page_b])
    db_session.flush()

    with pytest.raises(ValueError, match="Parent node not found"):
        move_node(
            workspace_a.id,
            page_a.id,
            page_b.id,
            db_session,
        )


def test_delete_page_removes_entire_subtree(db_session):
    from app.modules.nodes.service import delete_node

    workspace = Workspace(name="Deletion Test Workspace")

    db_session.add(workspace)
    db_session.flush()

    root = Node(
        workspace_id=workspace.id,
        name="Root",
    )

    db_session.add(root)
    db_session.flush()

    child_a = Node(
        workspace_id=workspace.id,
        name="Child A",
        parent_id=root.id,
    )

    child_b = Node(
        workspace_id=workspace.id,
        name="Child B",
        parent_id=root.id,
    )

    db_session.add_all([
        child_a,
        child_b,
    ])
    db_session.flush()

    grandchild = Node(
        workspace_id=workspace.id,
        name="Grandchild",
        parent_id=child_a.id,
    )

    db_session.add(grandchild)
    db_session.flush()

    root_id = root.id
    child_a_id = child_a.id
    child_b_id = child_b.id
    grandchild_id = grandchild.id

    deleted = delete_node(
        workspace.id,
        root_id,
        db_session,
    )

    assert deleted is True

    assert db_session.get(Node, root_id) is None
    assert db_session.get(Node, child_a_id) is None
    assert db_session.get(Node, child_b_id) is None
    assert db_session.get(Node, grandchild_id) is None


def test_delete_page_does_not_delete_unrelated_pages(db_session):
    from app.modules.nodes.service import delete_node

    workspace = Workspace(name="Deletion Isolation Workspace")
    db_session.add(workspace)
    db_session.flush()

    root_a = Node(
        workspace_id=workspace.id,
        name="Root A",
    )

    root_b = Node(
        workspace_id=workspace.id,
        name="Root B",
    )

    db_session.add_all([root_a, root_b])
    db_session.flush()

    child_a = Node(
        workspace_id=workspace.id,
        name="Child A",
        parent_id=root_a.id,
    )

    db_session.add(child_a)
    db_session.flush()

    root_a_id = root_a.id
    child_a_id = child_a.id
    root_b_id = root_b.id

    deleted = delete_node(
        workspace.id,
        root_a_id,
        db_session,
    )

    assert deleted is True

    assert db_session.get(Node, root_a_id) is None
    assert db_session.get(Node, child_a_id) is None

    assert db_session.get(Node, root_b_id) is not None

def test_page_cannot_be_its_own_parent(db_session):
    from app.modules.nodes.service import move_node

    workspace = Workspace(name="Self Parent Workspace")
    db_session.add(workspace)
    db_session.flush()

    page = Node(
        workspace_id=workspace.id,
        name="Page",
    )

    db_session.add(page)
    db_session.flush()

    with pytest.raises(ValueError, match="own parent"):
        move_node(
            workspace.id,
            page.id,
            page.id,
            db_session,
        )


def test_delete_page_cannot_delete_page_from_another_workspace(db_session):
    from app.modules.nodes.service import delete_node

    workspace_a = Workspace(name="Workspace A")
    workspace_b = Workspace(name="Workspace B")

    db_session.add_all([workspace_a, workspace_b])
    db_session.flush()

    page_a = Node(
        workspace_id=workspace_a.id,
        name="Page A",
    )

    page_b = Node(
        workspace_id=workspace_b.id,
        name="Page B",
    )

    db_session.add_all([page_a, page_b])
    db_session.flush()

    deleted = delete_node(
        workspace_a.id,
        page_b.id,
        db_session,
    )

    assert deleted is False
    assert db_session.get(Node, page_b.id) is not None