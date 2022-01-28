from fastapi.testclient import TestClient

from server.clients import JiraClient
from server.api import app, get_jira_client

client = TestClient(app)
jira_client_mock = JiraClient("dummy-path")


def test_health_liveness():
    response = client.get("/health/liveness")
    assert response.status_code == 200
    assert response.json() == {
        "name": "dapla-start-api",
        "status": "UP"
    }


def test_health_readiness():
    response = client.get("/health/readiness")
    assert response.status_code == 200
    assert response.json() == {
        "name": "dapla-start-api",
        "status": "UP"
    }


def test_create_issue():
    # https://fastapi.tiangolo.com/advanced/testing-dependencies/?h=override
    app.dependency_overrides[get_jira_client] = lambda: jira_client_mock
    jira_response = {
        "id": "112",
        "key": "DS-1",
        "self": "https://statistics-norway.atlassian.net/rest/api/3/issue/112"
    }
    jira_client_mock.create_issue = lambda arg: jira_response

    response = client.post("/create_jira", json={
        "display_team_name": "My team",
        "manager": "mymanager"
    })
    assert response.status_code == 201
    assert response.json() == jira_response
