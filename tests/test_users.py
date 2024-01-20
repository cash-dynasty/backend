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

# TODO test_activate_user
# 1. email i token zgodny - user aktywowany
# 2. niepoprawny email
# 3. nie ma takiego maila w bazie
# 4. niepoprawny token dla danego usera
