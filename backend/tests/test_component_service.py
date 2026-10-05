from sqlalchemy import select

from app.modules.components.models import Component, ComponentPlacement
from app.modules.components.schemas import ComponentCreate, ComponentUpdate
from app.modules.components.service import (
    create_component,
    get_component_by_id,
    update_component,
    delete_component
)
from app.modules.workspaces.models import Workspace
from app.modules.nodes.models import Node


def test_create_component_persists_component(db_session):
    workspace = Workspace(name="Test Workspace")

    db_session.add(workspace)
    db_session.flush()

    component = create_component(
        workspace_id=workspace.id,
        data=ComponentCreate(
            definition_key="text",
            config={"content": "Hello"},
        ),
        db=db_session,
    )

    assert component.id is not None
    assert component.workspace_id == workspace.id
    assert component.definition_key == "text"
    assert component.config == {"content": "Hello"}

    persisted_component = db_session.scalar(
        select(Component).where(
            Component.id == component.id,
        )
    )

    assert persisted_component is not None




def test_component_cannot_cross_workspace(db_session):
    workspace_a = Workspace(name="Workspace A")
    workspace_b = Workspace(name="Workspace B")

    db_session.add_all([workspace_a, workspace_b])
    db_session.flush()

    component = create_component(
        workspace_id=workspace_a.id,
        data=ComponentCreate(
            definition_key="text",
        ),
        db=db_session,
    )

    same_workspace_result = get_component_by_id(
        workspace_id=workspace_a.id,
        component_id=component.id,
        db=db_session,
    )

    other_workspace_result = get_component_by_id(
        workspace_id=workspace_b.id,
        component_id=component.id,
        db=db_session,
    )

    assert same_workspace_result is not None
    assert other_workspace_result is None

def test_update_component_persists_changes(db_session):
    workspace = Workspace(name="Update Test Workspace")

    db_session.add(workspace)
    db_session.flush()

    component = create_component(
        workspace_id=workspace.id,
        data=ComponentCreate(
            definition_key="text",
            config={"content": "Before"},
            binding={"type": "test"},
        ),
        db=db_session,
    )

    updated_component = update_component(
        workspace_id=workspace.id,
        component_id=component.id,
        data=ComponentUpdate(
            config={"content": "After"},
        ),
        db=db_session,
    )

    assert updated_component is not None
    assert updated_component.config == {
        "content": "After",
    }
    assert updated_component.binding == {
        "type": "test",
    }



def test_delete_component_cascades_placements(db_session):
    workspace = Workspace(name="Delete Test Workspace")

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
        ),
        db=db_session,
    )

    placement = ComponentPlacement(
        workspace_id=workspace.id,
        page_id=page.id,
        component_id=component.id,
        position={},
        size={},
        transform={},
        style={},
        visible=True,
        sort_order=0,
    )

    db_session.add(placement)
    db_session.flush()

    placement_id = placement.id
    component_id = component.id

    deleted = delete_component(
        workspace_id=workspace.id,
        component_id=component.id,
        db=db_session,
    )

    assert deleted is True

    assert db_session.get(Component, component_id) is None
    assert db_session.get(ComponentPlacement, placement_id) is None