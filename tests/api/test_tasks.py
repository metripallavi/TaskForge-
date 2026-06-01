from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_create_task() -> None:
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Learn FastAPI",
            "description": "Build TaskForge",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Learn FastAPI"
    assert data["description"] == "Build TaskForge"
    assert data["completed"] is False


def test_list_tasks() -> None:
    response = client.get("/api/v1/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_task() -> None:
    created = client.post(
        "/api/v1/tasks",
        json={
            "title": "Get Task",
            "description": "Testing",
        },
    )

    task_id = created.json()["id"]

    response = client.get(f"/api/v1/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["id"] == task_id
