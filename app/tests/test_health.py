from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_datasets_requires_auth():
    response = client.get("/api/v1/datasets")
    assert response.status_code == 401


def test_login_not_implemented():
    response = client.post("/auth/token?username=test&password=test")
    assert response.status_code == 501
