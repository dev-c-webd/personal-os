from sqlalchemy import select
import pytest

from app.modules.components.models import Component, ComponentPlacement
from app.modules.components.placement_service import create_placement, update_placement, delete_placement
from app.modules.components.schemas import ComponentCreate, ComponentPlacementCreate, ComponentPlacementUpdate
from app.modules.components.service import create_component
from app.modules.nodes.models import Node
from app.modules.workspaces.models import Workspace


def test_create_placement_persists_placement(db_session):
    workspace = Workspace(name="Placement Test Workspace")
    db_session.add(workspace)
    db_session.flush()

    page = Node(
        workspace_id=workspace.id,
        name="Test Page",
        sort_order=0,
    )
    db_session.add(page)
    db_session.flush()

    component = create_component(
        workspace_id=workspace.id,
        data=ComponentCreate(
            definition_key="text",
            config={"content": "Hello"},
        ),
        db=db_session,
    )

    placement = create_placement(
        workspace_id=workspace.id,
        data=ComponentPlacementCreate(
            page_id=page.id,
            component_id=component.id,
            position={"x": 100, "y": 50},
            size={"width": 300, "height": 150},
            transform={"rotation": 0},
            style={"border_radius": 20},
        ),
        db=db_session,
    )

    assert placement.id is not None
    assert placement.workspace_id == workspace.id
    assert placement.page_id == page.id
    assert placement.component_id == component.id
    assert placement.parent_placement_id is None
    assert placement.position == {"x": 100, "y": 50}
    assert placement.size == {"width": 300, "height": 150}

    persisted_placement = db_session.scalar(
        select(ComponentPlacement).where(
            ComponentPlacement.id == placement.id,
        )
    )

    assert persisted_placement is not None


def test_placement_parent_must_belong_to_same_page(db_session):
    workspace = Workspace(name="Placement Hierarchy Workspace")
    db_session.add(workspace)
    db_session.flush()

    page_a = Node(
        workspace_id=workspace.id,
        name="Page A",
        sort_order=0,
    )

    page_b = Node(
        workspace_id=workspace.id,
        name="Page B",
        sort_order=1,
    )

    db_session.add_all([page_a, page_b])
    db_session.flush()

    component = create_component(
        workspace_id=workspace.id,
        data=ComponentCreate(
            definition_key="text",
        ),
        db=db_session,
    )

    parent_placement = create_placement(
        workspace_id=workspace.id,
        data=ComponentPlacementCreate(
            page_id=page_a.id,
            component_id=component.id,
        ),
        db=db_session,
    )

    with pytest.raises(
        ValueError,
        match="Parent placement must belong to the same Page",
    ):
        create_placement(
            workspace_id=workspace.id,
            data=ComponentPlacementCreate(
                page_id=page_b.id,
                component_id=component.id,
                parent_placement_id=parent_placement.id,
            ),
            db=db_session,
        )

def test_placement_cycle_is_rejected(db_session):
    workspace = Workspace(name="Cycle Test Workspace")
    db_session.add(workspace)
    db_session.flush()

    page = Node(
        workspace_id=workspace.id,
        name="Cycle Test Page",
        sort_order=0,
    )
    db_session.add(page)
    db_session.flush()

    component = create_component(
        workspace_id=workspace.id,
        data=ComponentCreate(
            definition_key="text",
        ),
        db=db_session,
    )

    placement_a = create_placement(
        workspace_id=workspace.id,
        data=ComponentPlacementCreate(
            page_id=page.id,
            component_id=component.id,
        ),
        db=db_session,
    )

    placement_b = create_placement(
        workspace_id=workspace.id,
        data=ComponentPlacementCreate(
            page_id=page.id,
            component_id=component.id,
            parent_placement_id=placement_a.id,
        ),
        db=db_session,
    )

    placement_c = create_placement(
        workspace_id=workspace.id,
        data=ComponentPlacementCreate(
            page_id=page.id,
            component_id=component.id,
            parent_placement_id=placement_b.id,
        ),
        db=db_session,
    )

    with pytest.raises(
        ValueError,
        match="Cannot move a placement under its descendant",
    ):
        update_placement(
            workspace_id=workspace.id,
            placement_id=placement_a.id,
            data=ComponentPlacementUpdate(
                parent_placement_id=placement_c.id,
            ),
            db=db_session,
        )



def test_update_placement_can_move_to_root(db_session):
    workspace = Workspace(name="Root Reset Test Workspace")
    db_session.add(workspace)
    db_session.flush()

    page = Node(
        workspace_id=workspace.id,
        name="Root Reset Page",
        sort_order=0,
    )
    db_session.add(page)
    db_session.flush()

    component = create_component(
        workspace_id=workspace.id,
        data=ComponentCreate(
            definition_key="text",
        ),
        db=db_session,
    )

    parent = create_placement(
        workspace_id=workspace.id,
        data=ComponentPlacementCreate(
            page_id=page.id,
            component_id=component.id,
        ),
        db=db_session,
    )

    child = create_placement(
        workspace_id=workspace.id,
        data=ComponentPlacementCreate(
            page_id=page.id,
            component_id=component.id,
            parent_placement_id=parent.id,
        ),
        db=db_session,
    )

    assert child.parent_placement_id == parent.id

    updated_child = update_placement(
        workspace_id=workspace.id,
        placement_id=child.id,
        data=ComponentPlacementUpdate(
            parent_placement_id=None,
        ),
        db=db_session,
    )

    assert updated_child is not None
    assert updated_child.parent_placement_id is None


def test_delete_placement_cascades_children(db_session):
    workspace = Workspace(name="Placement Delete Test")
    db_session.add(workspace)
    db_session.flush()

    page = Node(
        workspace_id=workspace.id,
        name="Delete Test Page",
        sort_order=0,
    )
    db_session.add(page)
    db_session.flush()

    component = create_component(
        workspace_id=workspace.id,
        data=ComponentCreate(
            definition_key="text",
        ),
        db=db_session,
    )

    parent = create_placement(
        workspace_id=workspace.id,
        data=ComponentPlacementCreate(
            page_id=page.id,
            component_id=component.id,
        ),
        db=db_session,
    )

    child = create_placement(
        workspace_id=workspace.id,
        data=ComponentPlacementCreate(
            page_id=page.id,
            component_id=component.id,
            parent_placement_id=parent.id,
        ),
        db=db_session,
    )

    parent_id = parent.id
    child_id = child.id

    deleted = delete_placement(
        workspace_id=workspace.id,
        placement_id=parent_id,
        db=db_session,
    )

    assert deleted is True
    assert db_session.get(ComponentPlacement, parent_id) is None
    assert db_session.get(ComponentPlacement, child_id) is None