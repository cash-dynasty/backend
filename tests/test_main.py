import os
import sys

from fastapi.testclient import TestClient


sys.path.append(os.getcwd())
sys.path.append("./app")

# ruff: noqa: E402
from app.main import app


client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
