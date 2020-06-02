from .main import app

from fastapi.testclient import TestClient

client = TestClient(app)


def test_abc():
    response = client.get("/request04")
    assert response.status_code == 422