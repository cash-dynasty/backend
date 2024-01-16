import sys

import pytest
from jose import jwt


sys.path.append("./app")


import schemas.auth  # noqa: E402
import schemas.user  # noqa: E402
from settings import settings  # noqa: E402


def test_create_user(client):
    res = client.post(
        "/users/create",
        json={"email": "hello123@gmail.com", "password": "password123"},
    )

    new_user = schemas.user.UserOut(**res.json())
    assert res.status_code == 201
    assert new_user.email == "hello123@gmail.com"

    res = client.post(
        "/users/create",
        json={"email": "hello123@gmail.com", "password": "password123"},
    )
    assert res.status_code == 409
    # assert res.json()["detail"] == "User already exists"
    assert res.json() == {"detail": "User already exists"}

    res = client.post(
        "/users/create",
        json={"email": "hello123@gmail", "password": "password123"},
    )

    assert res.status_code == 422
    # assert res.json() == ''  # TODO dodać po usystematyzowaniu responsów pydantica


def test_login_user(test_user, client):
    res = client.post(
        "/auth/token",
        data={"username": test_user["email"], "password": test_user["password"]},
        # data={"username": "aaa@aaa.pl", "password": "aaa"},
    )
    print(res.json())
    login_res = schemas.auth.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.ACCESS_TOKEN_SECRET_KEY, algorithms=[settings.ALGORITHM])
    email = payload.get("sub")
    assert res.status_code == 200
    assert email == test_user["email"]
    # assert email == "aaa@aaa.pl"
    assert login_res.token_type == "bearer"


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "password123", 401),  # TODO 403
        ("sanjeev@gmail.com", "wrongpassword", 401),  # TODO 403
        ("wrongemail@gmail.com", "wrongpassword", 401),  # TODO 403
        (None, "password123", 422),
        ("sanjeev@gmail.com", None, 422),
    ],
)
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/auth/token", data={"username": email, "password": password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'


# def test_refresh_token(client, refresh_token):
#     client.cookies.get('refres')
#     client.headers = {**client.headers, "Authorization": f"Bearer {refresh_token}"}
#     res = client.post("/auth/refresh")
#     assert res.status_code == 200
#
#     # res = client.post("/auth/refresh", data={"username": email, "password": password})
#     # client.headers = {**client.headers, "Authorization": f"Bearer {access_token}"}
#     # return client
