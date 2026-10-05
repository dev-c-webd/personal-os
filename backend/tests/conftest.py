import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+psycopg://localhost:5432/personal_os_test",
)

from app.db.database import engine, get_db
from app.main import app
from app.modules.workspaces.dependencies import get_workspace_member


@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()

    session = Session(
        bind=connection,
        join_transaction_mode="create_savepoint",
    )

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    def override_get_workspace_member():
        return None

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_workspace_member] = (
        override_get_workspace_member
    )

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def auth_client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()