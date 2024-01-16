import sys


sys.path.append("./app")


def test_read_root(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"message": "Hello World"}


def test_read_protected_endpoint_by_active_user(authorized_active_client):
    res = authorized_active_client.get("/protected")
    assert res.status_code == 200
    # assert res.json()["message"] == "This is a protected endpoint."
    assert res.json() == {"message": "This is a protected endpoint."}


def test_read_protected_endpoint_by_inactive_user(authorized_client):
    res = authorized_client.get("/protected")
    assert res.status_code == 403
    # assert res.json()["detail"] == "Inactive user"
    assert res.json() == {"detail": "Inactive user"}
