from fastapi.testclient import TestClient

from app.main import app


def test_protected_route_rejects_missing_bearer_token():
    response = TestClient(app).post("/sessions")
    assert response.status_code == 401
