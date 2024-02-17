import sys
import time

import pytest
from jose import jwt


sys.path.append("./app")


import schemas.auth  # noqa: E402
import schemas.user  # noqa: E402
from settings import settings  # noqa: E402


def test_login_inactive_user(client, inactive_test_user):
    res = client.post(
        "/auth/token", data={"username": inactive_test_user["email"], "password": inactive_test_user["password"]}
    )
    assert res.status_code == 403
    assert res.json() == {"detail": "Inactive user"}


def test_login_active_user(client, test_user):
    res = client.post("/auth/token", data={"username": test_user["email"], "password": test_user["password"]})
    assert res.status_code == 200
    token_data = schemas.auth.Token(**res.json())
    assert token_data.access_token
    assert "refresh_token" not in token_data
    assert token_data.token_type == "bearer"
    cookies = res.cookies
    assert cookies["access_token"]
    assert cookies["refresh_token"]
    assert token_data.access_token == cookies["access_token"]
    payload = jwt.decode(cookies["access_token"], settings.ACCESS_TOKEN_SECRET_KEY, algorithms=[settings.ALGORITHM])
    user_id = payload["uid"]
    assert user_id == test_user["id"]
    payload = jwt.decode(cookies["refresh_token"], settings.REFRESH_TOKEN_SECRET_KEY, algorithms=[settings.ALGORITHM])
    user_id = payload["uid"]
    assert user_id == test_user["id"]


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "password123", 401),
        ("arydlewski@cashdynasty.pl", "wrongpassword", 401),
        ("wrongemail@gmail.com", "wrongpassword", 401),
        ("wrongemail@gmail", "test_user", 401),
        (None, "password123", 422),
        ("arydlewski@cashdynasty.pl", None, 422),
    ],
)
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/auth/token", data={"username": email, "password": password})
    assert res.status_code == status_code


def test_incorrect_login_message(client):
    res = client.post("/auth/token", data={"username": "wrongemail@gmail.com", "password": "wrongpassword"})
    assert res.status_code == 401
    assert res.json() == {"detail": "Incorrect username or password"}


# TODO przetestować czas ważności tokenu
def test_refresh_token(authorized_client, test_user):
    cookies = authorized_client.cookies

    access_token = cookies["access_token"]
    refresh_token = cookies["refresh_token"]

    time.sleep(1)
    res = authorized_client.post("/auth/refresh", headers={"Authorization": f"Bearer {refresh_token}"})
    assert res.status_code == 200
    token_data = schemas.auth.Token(**res.json())
    assert token_data.access_token
    assert "refresh_token" not in token_data
    assert token_data.token_type == "bearer"
    cookies = res.cookies
    assert cookies["access_token"]
    assert cookies["refresh_token"]
    assert token_data.access_token == cookies["access_token"]
    payload = jwt.decode(cookies["access_token"], settings.ACCESS_TOKEN_SECRET_KEY, algorithms=[settings.ALGORITHM])
    user_id = payload["uid"]
    assert user_id == test_user["id"]
    payload = jwt.decode(cookies["refresh_token"], settings.REFRESH_TOKEN_SECRET_KEY, algorithms=[settings.ALGORITHM])
    user_id = payload["uid"]
    assert user_id == test_user["id"]

    old_access_token = access_token
    old_refresh_token = refresh_token

    new_access_token = res.cookies["access_token"]
    new_refresh_token = res.cookies["refresh_token"]

    res = authorized_client.get("/test/protected", headers={"Authorization": f"Bearer {old_access_token}"})
    assert res.status_code == 200
    assert res.json() == {"detail": "Hello from protected endpoint!"}

    time.sleep(1)
    res = authorized_client.post("/auth/refresh", headers={"Authorization": f"Bearer {old_refresh_token}"})
    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}

    res = authorized_client.get("/test/protected", headers={"Authorization": f"Bearer {new_access_token}"})
    assert res.status_code == 200
    assert res.json() == {"detail": "Hello from protected endpoint!"}

    time.sleep(1)
    res = authorized_client.post("/auth/refresh", headers={"Authorization": f"Bearer {new_refresh_token}"})
    assert res.status_code == 200


def test_logout_user_with_access_token(authorized_client):
    res = authorized_client.post("/auth/logout")
    assert res.status_code == 200
    assert res.json() == {"detail": "logged out"}
    cookies = res.cookies
    assert not cookies.get("access_token")
    assert not cookies.get("refresh_token")


def test_logout_user_with_refresh_token(authorized_client):
    cookies = authorized_client.cookies
    refresh_token = cookies.get("refresh_token")
    res = authorized_client.post("/auth/logout", headers={"Authorization": f"Bearer {refresh_token}"})
    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}


def test_logout_user_with_invalid_token(client_with_invalid_token):
    res = client_with_invalid_token.post("/auth/logout")
    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}


def test_logout_user_without_token(client):
    res = client.post("/auth/logout")
    assert res.status_code == 401
    assert res.json() == {"detail": "Not authenticated"}
