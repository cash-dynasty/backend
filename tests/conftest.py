import os
import sys

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


sys.path.append("./app")

from database import Base, get_db  # noqa: E402
from main import app  # noqa: E402
from settings import settings  # noqa: E402


SQLALCHEMY_DATABASE_URL = settings.POSTGRESQL_CONNECTION_URL_TEST

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def test_mode():
    os.environ["TESTING"] = "YES"
    yield
    os.environ.pop("TESTING", None)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def inactive_test_user(client):
    user_data = {"email": "sanjeev@gmail.com", "password": "password123"}
    res = client.post("/users/create", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user(client, inactive_test_user):
    res = client.patch("/users/activate", json={"email": inactive_test_user["email"]})
    assert res.status_code == 200
    new_user = res.json()
    new_user["password"] = inactive_test_user["password"]
    assert new_user["is_active"]
    return new_user


@pytest.fixture
def authorized_client(client, test_user):
    res = client.post(
        "/auth/token",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    assert res.status_code == 200
    access_token = res.json()["access_token"]
    client.headers = {**client.headers, "Authorization": f"Bearer {access_token}"}
    return client


@pytest.fixture
def client_with_invalid_token(client, test_user):
    res = client.post(
        "/auth/token",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    assert res.status_code == 200
    access_token = res.json()["access_token"]
    client.headers = {**client.headers, "Authorization": f"Bearer {access_token}x"}
    return client
