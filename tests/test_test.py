import sys


sys.path.append("./app")


def test_read_public_endpoint(client):
    res = client.get("/test/")
    assert res.status_code == 200
    assert res.json() == {"message": "Hello from public endpoint!"}


def test_read_protected_endpoint(authorized_client):
    res = authorized_client.get("/test/protected")
    assert res.status_code == 200
    assert res.json() == {"message": "Hello from protected endpoint!"}


def test_read_protected_endpoint_with_invalid_token(client_with_invalid_token):
    res = client_with_invalid_token.get("/test/protected")
    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}


def test_read_protected_endpoint_with_expired_token(client_with_expired_token):
    res = client_with_expired_token.get("/test/protected")
    assert res.status_code == 401
    assert res.json() == {"detail": "Token has expired."}


def test_read_protected_endpoint_without_token(client):
    res = client.get("/test/protected")
    assert res.status_code == 401
    assert res.json() == {"detail": "Not authenticated"}
