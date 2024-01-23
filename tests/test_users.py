import sys


sys.path.append("./app")


import schemas.auth  # noqa: E402
import schemas.user  # noqa: E402


def test_create_user(client):
    res = client.post("/users/create", json={"email": "hello123@gmail.com", "password": "password123"})
    new_user = schemas.user.UserCreateRes(**res.json())
    assert res.status_code == 201
    assert new_user.email == "hello123@gmail.com"


def test_create_user_that_already_exists(client, inactive_test_user):
    res = client.post(
        "/users/create", json={"email": inactive_test_user["email"], "password": inactive_test_user["password"]}
    )
    assert res.status_code == 409
    assert res.json() == {"detail": "User already exists"}


def test_create_user_with_wrong_email(client):
    res = client.post("/users/create", json={"email": "hello123@gmail", "password": "password123"})
    assert res.status_code == 422
    # assert res.json() == ''  # TODO dodać po usystematyzowaniu responsów pydantica


# TODO test_create_user_with_wrong_password


def test_activate_user_with_correct_email_and_token(client, inactive_test_user):
    res = client.patch("/users/activate", json={"email": inactive_test_user["email"], "token": "test_token"})
    assert res.status_code == 200
    assert res.json() == {"email": inactive_test_user["email"], "is_active": True}


def test_activate_user_with_wrong_email_and_correct_token(client):
    res = client.patch("/users/activate", json={"email": "nouser@test.com", "token": "test_token"})
    assert res.status_code == 404
    assert res.json() == {"detail": "User not found"}


def test_activate_user_with_wrong_token_and_correct_email(client, inactive_test_user):
    res = client.patch("/users/activate", json={"email": inactive_test_user["email"], "token": "wrong_token"})
    assert res.status_code == 400
    assert res.json() == {"detail": "Invalid token"}


def test_activate_user_with_correct_email_and_expired_token(client, inactive_expired_token_test_user):
    res = client.patch(
        "/users/activate", json={"email": inactive_expired_token_test_user["email"], "token": "test_token"}
    )
    assert res.status_code == 400
    assert res.json() == {"detail": "Token expired"}


def test_activate_already_active_user(client, test_user):
    res = client.patch("/users/activate", json={"email": test_user["email"], "token": "test_token"})
    assert res.status_code == 400
    assert res.json() == {"detail": "User already activated"}
