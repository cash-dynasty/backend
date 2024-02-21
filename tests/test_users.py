from unittest.mock import patch

import schemas.auth
import schemas.user
from utils.commons import get_current_time


def test_create_user(client, user_data):
    with patch(
        "routers.users.generate_activation_token",
        return_value={"token": "test_token", "expiration_date": get_current_time()},
    ):
        with patch("routers.users.send_user_create_activation_email") as mocked_function:
            res = client.post("/users/create", json=user_data)
            mocked_function.assert_called_once_with("test@test.pl", "test_token")
    new_user = schemas.user.UserCreateRes(**res.json())
    assert res.status_code == 201
    assert new_user.email == "test@test.pl"


def test_create_user_that_already_exists(client, inactive_user):
    res = client.post("/users/create", json={"email": inactive_user["email"], "password": inactive_user["password"]})
    assert res.status_code == 409
    assert res.json() == {"detail": "User already exists"}


def test_create_user_with_wrong_email(client):
    res = client.post("/users/create", json={"email": "hello123@gmail", "password": "password123"})
    assert res.status_code == 422
    # assert res.json() == ''  # TODO dodać po usystematyzowaniu responsów pydantica


# TODO test_create_user_with_wrong_password


def test_activate_user_with_correct_email_and_token(client, inactive_user):
    res = client.patch("/users/activate", json={"email": inactive_user["email"], "token": "test_token"})
    assert res.status_code == 200
    assert res.json() == {"email": inactive_user["email"], "is_active": True}


def test_activate_user_with_wrong_email_and_correct_token(client):
    res = client.patch("/users/activate", json={"email": "nouser@test.com", "token": "test_token"})
    assert res.status_code == 404
    assert res.json() == {"detail": "User not found"}  # TODO ukryć to info?


def test_activate_user_with_correct_email_and_wrong_token(client, inactive_user):
    res = client.patch("/users/activate", json={"email": inactive_user["email"], "token": "wrong_token"})
    assert res.status_code == 400
    assert res.json() == {"detail": "Invalid token"}


def test_activate_user_with_correct_email_and_expired_token(client, inactive_user_with_expired_activation_token):
    res = client.patch(
        "/users/activate",
        json={"email": inactive_user_with_expired_activation_token["email"], "token": "test_token"},
    )
    assert res.status_code == 400
    assert res.json() == {"detail": "Token expired"}


def test_activate_already_activated_user(client, user):
    res = client.patch("/users/activate", json={"email": user["email"], "token": "test_token"})
    assert res.status_code == 400
    assert res.json() == {"detail": "User already activated"}  # TODO ukryć to info?
