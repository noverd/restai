from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "REST AI API, so many 'A's and 'I's, so little time..."


def test_getProjects():
    response = client.get("/projects")
    assert response.status_code == 200
    assert response.json() == {"projects": []}


def test_createProject():
    response = client.post("/projects", json={"name": "test",  "embeddings": "openai"})
    assert response.status_code == 200


def test_getProject():
    response = client.get("/projects/test")
    assert response.status_code == 200


def test_ingestURL():
    response = client.post("/projects/test/ingest/url",
                           json={"url": "https://www.google.com"})
    assert response.status_code == 200


def test_getProjectAfterIngest():
    response = client.get("/projects/test")
    assert response.status_code == 200
    assert response.json() == {"project": "test", "embeddings": "openai", "documents": 1, "metadatas": 1}


def test_deleteProject():
    response = client.delete("/projects/test")
    assert response.status_code == 200
    assert response.json() == {"project": "test"}


def test_getProjectAfterDelete():
    response = client.get("/projects/test")
    assert response.status_code == 404


def test_getProjectsAfterDelete():
    response = client.get("/projects")
    assert response.status_code == 200
    assert response.json() == {"projects": []}
