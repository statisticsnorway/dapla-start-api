import toml
from fastapi.testclient import TestClient

from server.clients import JiraClient
from server.api import app, get_jira_client
from pathlib import Path
from server import __version__

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


def test_versions_are_in_sync():
    """Checks if the pyproject.toml and package.__init__.py __version__ are in sync."""

    path = Path(__file__).resolve().parents[1] / "pyproject.toml"
    pyproject = toml.loads(open(str(path)).read())
    pyproject_version = pyproject["tool"]["poetry"]["version"]

    package_init_version = __version__

    assert package_init_version == pyproject_version


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
        "manager": {
            "name": "Magnus Manager",
            "email_short": "mma@ssb.no",
            "email": "magnus.manager@ssb.no"
        }
    })
    assert response.status_code == 201
    assert response.json() == jira_response
