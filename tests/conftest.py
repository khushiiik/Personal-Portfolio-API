import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.database import Base
from app.dependencies import get_db
from app.models import user, project, skill, association_tables, experience


# Fixture 1: db.
@pytest.fixture(scope="function")
def db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db_session = TestingSessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
        Base.metadata.drop_all(bind=engine)


# Fixture 2: client.
@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


# Fixture 3: user_token.
@pytest.fixture(scope="function")
def user_token(client):
    client.post(
        "/auth/register",
        json={
            "name": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
        },
    )

    response = client.post(
        "/auth/login", data={"username": "test@example.com", "password": "testpass123"}
    )
    return response.json()["access_token"]


# Fixture 4 : auth_headers.
@pytest.fixture(scope="function")
def auth_headers(user_token):
    return {"Authorization": f"Bearer {user_token}"}
