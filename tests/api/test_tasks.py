import uuid

from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def get_auth_headers() -> dict[str, str]:
    email = f"{uuid.uuid4()}@example.com"
    password = "testpassword123"

    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )

    assert register_response.status_code in (200, 201)

    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}",
    }


def test_create_task() -> None:
    headers = get_auth_headers()

    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Learn FastAPI",
            "description": "Build TaskForge",
        },
        headers=headers,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Learn FastAPI"
    assert data["description"] == "Build TaskForge"
    assert data["completed"] is False


def test_list_tasks() -> None:
    headers = get_auth_headers()

    response = client.get(
        "/api/v1/tasks",
        headers=headers,
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_task() -> None:
    headers = get_auth_headers()

    created = client.post(
        "/api/v1/tasks",
        json={
            "title": "Get Task",
            "description": "Testing",
        },
        headers=headers,
    )

    assert created.status_code == 201

    task_id = created.json()["id"]

    response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["id"] == task_id
