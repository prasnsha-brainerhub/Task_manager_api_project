from fastapi.testclient import TestClient
from main import app
from db.session import engine
from db.models import Base
import pytest         


def init_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client


def test_create_task(test_client):
    response = test_client.post(
        "/tasks/",
        json={"title": "Test Task", "description": "Testing task creation", "deadline": "2024-05-15", "status": "todo"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"
    assert response.json()["description"] == "Testing task creation"
    assert response.json()["status"] == "todo"

def test_read_tasks(test_client):
    response = test_client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_task(test_client):
    # First, create a task
    response = test_client.post(
        "/tasks/",
        json={"title": "Test Task", "description": "Testing task creation", "deadline": "2024-05-15", "status": "todo"},
    )
    task_id = response.json()["id"]

    # Then, update the task
    response = test_client.put(
        f"/tasks/{task_id}",
        json={"title": "Updated Task", "description": "Testing task update", "deadline": "2024-05-20", "status": "in progress"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"
    assert response.json()["description"] == "Testing task update"
    assert response.json()["status"] == "in progress"

def test_delete_task(test_client):
    # First, create a task
    response = test_client.post(
        "/tasks/",
        json={"title": "Test Task", "description": "Testing task creation", "deadline": "2024-05-15", "status": "todo"},
    )
    task_id = response.json()["id"]

    # Then, delete the task
    response = test_client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200