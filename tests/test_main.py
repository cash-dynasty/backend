import sys

from fastapi.testclient import TestClient


sys.path.append("./app")


from main import app  # noqa: E402


client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
