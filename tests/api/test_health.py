from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_root_endpoint() -> None:
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["project"] == "TaskForge"
    assert data["docs"] == "/docs"
    assert data["health"] == "/api/v1/health"
    assert "version" in data
