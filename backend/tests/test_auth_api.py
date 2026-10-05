def test_create_workspace_without_authentication_returns_401(
    client,
):
    response = client.post(
        "/api/v1/workspaces",
        json={
            "name": "Unauthorized Workspace",
        },
    )

    assert response.status_code == 401

def test_create_workspace_with_invalid_token_returns_401(
    client,
):
    response = client.post(
        "/api/v1/workspaces",
        headers={
            "Authorization": "Bearer definitely-not-a-real-token",
        },
        json={
            "name": "Invalid Token Workspace",
        },
    )

    assert response.status_code == 401

def test_create_workspace_with_valid_token_succeeds(
    client,
    db_session,
):
    from app.core.security import create_access_token, hash_password
    from app.modules.users.models import User

    user = User(
        username="auth_test_user",
        email="auth_test@example.com",
        password_hash=hash_password("password123"),
    )

    db_session.add(user)
    db_session.flush()

    access_token = create_access_token(str(user.id))

    response = client.post(
        "/api/v1/workspaces",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        json={
            "name": "Authenticated Workspace",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Authenticated Workspace"


def test_authenticated_user_without_workspace_membership_returns_403(
    auth_client,
    db_session,
):
    from app.core.security import create_access_token, hash_password
    from app.modules.users.models import User
    from app.modules.workspaces.models import Workspace

    user = User(
        username="member_test_user",
        email="member_test@example.com",
        password_hash=hash_password("password123"),
    )

    workspace = Workspace(
        name="Private Workspace",
    )

    db_session.add_all([user, workspace])
    db_session.flush()

    access_token = create_access_token(str(user.id))

    response = auth_client.get(
        f"/api/v1/workspaces/{workspace.id}",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 403

def test_authenticated_workspace_member_can_access_workspace(
    auth_client,
    db_session,
):
    from app.core.security import create_access_token, hash_password
    from app.modules.users.models import User
    from app.modules.workspaces.models import Workspace
    from app.modules.workspaces.membership_models import WorkspaceMember

    user = User(
        username="authorized_user",
        email="authorized@example.com",
        password_hash=hash_password("password123"),
    )

    workspace = Workspace(
        name="Authorized Workspace",
    )

    db_session.add_all([user, workspace])
    db_session.flush()

    membership = WorkspaceMember(
        workspace_id=workspace.id,
        user_id=user.id,
        role="owner",
    )

    db_session.add(membership)
    db_session.flush()

    access_token = create_access_token(str(user.id))

    response = auth_client.get(
        f"/api/v1/workspaces/{workspace.id}",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(workspace.id)
    assert data["name"] == "Authorized Workspace"


def test_user_cannot_access_another_users_workspace(
    auth_client,
    db_session,
):
    from app.core.security import create_access_token, hash_password
    from app.modules.users.models import User
    from app.modules.workspaces.models import Workspace
    from app.modules.workspaces.membership_models import WorkspaceMember

    user_a = User(
        username="user_a",
        email="user_a@example.com",
        password_hash=hash_password("password123"),
    )

    user_b = User(
        username="user_b",
        email="user_b@example.com",
        password_hash=hash_password("password123"),
    )

    workspace_a = Workspace(name="User A Workspace")
    workspace_b = Workspace(name="User B Workspace")

    db_session.add_all([
        user_a,
        user_b,
        workspace_a,
        workspace_b,
    ])
    db_session.flush()

    db_session.add_all([
        WorkspaceMember(
            workspace_id=workspace_a.id,
            user_id=user_a.id,
            role="owner",
        ),
        WorkspaceMember(
            workspace_id=workspace_b.id,
            user_id=user_b.id,
            role="owner",
        ),
    ])
    db_session.flush()

    access_token = create_access_token(str(user_a.id))

    response = auth_client.get(
        f"/api/v1/workspaces/{workspace_b.id}",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 403


def test_login_returns_access_token(client, db_session):
    from app.core.security import hash_password
    from app.modules.users.models import User

    user = User(
        username="login_test_user",
        email="login_test@example.com",
        password_hash=hash_password("password123"),
    )

    db_session.add(user)
    db_session.flush()

    response = client.post(
        "/api/v1/auth/login",
        json={
            "identifier": "login_test_user",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["access_token"], str)
    assert data["access_token"]
    assert data["token_type"] == "bearer"


def test_login_with_wrong_password_returns_401(client, db_session):
    from app.core.security import hash_password
    from app.modules.users.models import User

    user = User(
        username="wrong_password_user",
        email="wrong_password@example.com",
        password_hash=hash_password("correct-password"),
    )

    db_session.add(user)
    db_session.flush()

    response = client.post(
        "/api/v1/auth/login",
        json={
            "identifier": "wrong_password_user",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401