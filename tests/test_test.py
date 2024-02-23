def test_read_public_endpoint(client):
    res = client.get("/test/")
    assert res.status_code == 200
    assert res.json() == {"detail": "Hello from public endpoint!"}


def test_read_protected_endpoint_with_valid_token(authorized_client):
    res = authorized_client.get("/test/protected")
    assert res.status_code == 200
    assert res.json() == {"detail": "Hello from protected endpoint!"}


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


def test_read_admin_endpoint_with_admin_permissions(client_with_admin_permissions):
    res = client_with_admin_permissions.get("/test/admin")
    assert res.status_code == 200
    assert res.json() == {"detail": "Hello from admin endpoint!"}


def test_read_admin_endpoint_without_admin_permissions(authorized_client):
    res = authorized_client.get("/test/admin")
    assert res.status_code == 401
    assert res.json() == {"detail": "Not enough permissions"}
