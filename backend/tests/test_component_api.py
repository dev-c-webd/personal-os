from app.modules.workspaces.models import Workspace


# Component API

def test_create_component_api(client, db_session):
    workspace = Workspace(name="API Test Workspace")

    db_session.add(workspace)
    db_session.flush()

    response = client.post(
        f"/api/v1/workspaces/{workspace.id}/components",
        json={
            "definition_key": "text",
            "config": {
                "content": "Hello API",
            },
            "binding": None,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["workspace_id"] == str(workspace.id)
    assert data["definition_key"] == "text"
    assert data["config"] == {
        "content": "Hello API",
    }
    assert data["binding"] is None

def test_get_missing_component_returns_404(client):
    response = client.get(
        "/api/v1/workspaces/00000000-0000-0000-0000-000000000000/components/"
        "00000000-0000-0000-0000-000000000001"
    )

    assert response.status_code == 404


def test_get_component_from_wrong_workspace_returns_404(client, db_session):
    from app.modules.components.models import Component

    workspace_a = Workspace(name="Workspace A")
    workspace_b = Workspace(name="Workspace B")

    db_session.add_all([workspace_a, workspace_b])
    db_session.flush()

    component = Component(
        workspace_id=workspace_a.id,
        definition_key="text",
        config={"content": "Private"},
    )

    db_session.add(component)
    db_session.flush()

    response = client.get(
        f"/api/v1/workspaces/{workspace_b.id}/components/{component.id}"
    )

    assert response.status_code == 404


def test_get_component_api(client, db_session):
    from app.modules.components.models import Component

    workspace = Workspace(name="Read Test Workspace")

    db_session.add(workspace)
    db_session.flush()

    component = Component(
        workspace_id=workspace.id,
        definition_key="text",
        config={
            "content": "Read me",
        },
    )

    db_session.add(component)
    db_session.flush()

    response = client.get(
        f"/api/v1/workspaces/{workspace.id}/components/{component.id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(component.id)
    assert data["workspace_id"] == str(workspace.id)
    assert data["definition_key"] == "text"
    assert data["config"] == {
        "content": "Read me",
    }


def test_update_component_api(client, db_session):
    from app.modules.components.models import Component

    workspace = Workspace(name="Update Test Workspace")

    db_session.add(workspace)
    db_session.flush()

    component = Component(
        workspace_id=workspace.id,
        definition_key="text",
        config={
            "content": "Before",
        },
    )

    db_session.add(component)
    db_session.flush()

    response = client.patch(
        f"/api/v1/workspaces/{workspace.id}/components/{component.id}",
        json={
            "config": {
                "content": "After",
            }
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(component.id)
    assert data["definition_key"] == "text"
    assert data["config"] == {
        "content": "After",
    }


def test_update_component_can_clear_binding_api(client, db_session):
    from app.modules.components.models import Component
    from app.modules.workspaces.models import Workspace

    workspace = Workspace(name="Clear Binding Test Workspace")

    db_session.add(workspace)
    db_session.flush()

    component = Component(
        workspace_id=workspace.id,
        definition_key="text",
        config={
            "content": "Bound component",
        },
        binding={
            "source": "user",
        },
    )

    db_session.add(component)
    db_session.flush()

    response = client.patch(
        f"/api/v1/workspaces/{workspace.id}/components/{component.id}",
        json={
            "binding": None,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["binding"] is None

def test_delete_component_api(client, db_session):
    from app.modules.components.models import Component
    from app.modules.workspaces.models import Workspace

    workspace = Workspace(name="Delete Test Workspace")

    db_session.add(workspace)
    db_session.flush()

    component = Component(
        workspace_id=workspace.id,
        definition_key="text",
        config={"content": "Delete me"},
    )

    db_session.add(component)
    db_session.flush()

    response = client.delete(
        f"/api/v1/workspaces/{workspace.id}/components/{component.id}"
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/api/v1/workspaces/{workspace.id}/components/{component.id}"
    )

    assert get_response.status_code == 404


# Placement API

def test_create_placement_api(client, db_session):
    from app.modules.components.models import Component
    from app.modules.nodes.models import Node
    from app.modules.workspaces.models import Workspace

    workspace = Workspace(name="Placement API Workspace")
    db_session.add(workspace)
    db_session.flush()

    page = Node(
        workspace_id=workspace.id,
        name="Home",
    )

    component = Component(
        workspace_id=workspace.id,
        definition_key="text",
        config={"content": "Hello"},
    )

    db_session.add_all([page, component])
    db_session.flush()

    response = client.post(
        f"/api/v1/workspaces/{workspace.id}/components/placements",
        json={
            "page_id": str(page.id),
            "component_id": str(component.id),
            "position": {
                "x": 10,
                "y": 20,
            },
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["workspace_id"] == str(workspace.id)
    assert data["page_id"] == str(page.id)
    assert data["component_id"] == str(component.id)
    assert data["parent_placement_id"] is None
    assert data["position"] == {
        "x": 10,
        "y": 20,
    }


def test_create_nested_placement_api(client, db_session):
    from app.modules.components.models import Component
    from app.modules.nodes.models import Node
    from app.modules.workspaces.models import Workspace

    workspace = Workspace(name="Nested Placement API Workspace")
    db_session.add(workspace)
    db_session.flush()

    page = Node(
        workspace_id=workspace.id,
        name="Home",
    )

    component = Component(
        workspace_id=workspace.id,
        definition_key="text",
        config={"content": "Hello"},
    )

    db_session.add_all([page, component])
    db_session.flush()

    root_response = client.post(
        f"/api/v1/workspaces/{workspace.id}/components/placements",
        json={
            "page_id": str(page.id),
            "component_id": str(component.id),
        },
    )

    assert root_response.status_code == 201

    root = root_response.json()

    child_response = client.post(
        f"/api/v1/workspaces/{workspace.id}/components/placements",
        json={
            "page_id": str(page.id),
            "component_id": str(component.id),
            "parent_placement_id": root["id"],
        },
    )

    assert child_response.status_code == 201

    child = child_response.json()

    assert child["page_id"] == str(page.id)
    assert child["component_id"] == str(component.id)
    assert child["parent_placement_id"] == root["id"]


def test_create_placement_with_parent_from_different_page_returns_400(
    client,
    db_session,
):
    from app.modules.components.models import Component
    from app.modules.nodes.models import Node
    from app.modules.workspaces.models import Workspace

    workspace = Workspace(name="Cross Page Placement API Workspace")
    db_session.add(workspace)
    db_session.flush()

    page_a = Node(
        workspace_id=workspace.id,
        name="Page A",
    )

    page_b = Node(
        workspace_id=workspace.id,
        name="Page B",
    )

    component = Component(
        workspace_id=workspace.id,
        definition_key="text",
        config={"content": "Hello"},
    )

    db_session.add_all([page_a, page_b, component])
    db_session.flush()

    parent_response = client.post(
        f"/api/v1/workspaces/{workspace.id}/components/placements",
        json={
            "page_id": str(page_b.id),
            "component_id": str(component.id),
        },
    )

    assert parent_response.status_code == 201

    parent = parent_response.json()

    response = client.post(
        f"/api/v1/workspaces/{workspace.id}/components/placements",
        json={
            "page_id": str(page_a.id),
            "component_id": str(component.id),
            "parent_placement_id": parent["id"],
        },
    )

    assert response.status_code == 400


def test_update_placement_cycle_returns_400(client, db_session):
    from app.modules.components.models import Component
    from app.modules.components.placement_service import create_placement
    from app.modules.components.schemas import ComponentPlacementCreate
    from app.modules.nodes.models import Node
    from app.modules.workspaces.models import Workspace

    workspace = Workspace(name="Cycle API Workspace")
    db_session.add(workspace)
    db_session.flush()

    page = Node(
        workspace_id=workspace.id,
        name="Home",
    )

    component = Component(
        workspace_id=workspace.id,
        definition_key="text",
        config={"content": "Hello"},
    )

    db_session.add_all([page, component])
    db_session.flush()

    root = create_placement(
        workspace.id,
        ComponentPlacementCreate(
            page_id=page.id,
            component_id=component.id,
        ),
        db_session,
    )

    child = create_placement(
        workspace.id,
        ComponentPlacementCreate(
            page_id=page.id,
            component_id=component.id,
            parent_placement_id=root.id,
        ),
        db_session,
    )

    response = client.patch(
        f"/api/v1/workspaces/{workspace.id}/components/placements/{root.id}",
        json={
            "parent_placement_id": str(child.id),
        },
    )

    assert response.status_code == 400