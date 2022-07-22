import toml
from fastapi.testclient import TestClient

from server.clients import JiraClient, KlassClient
from server.api import app, get_jira_client, get_klass_client
from pathlib import Path
from server import __version__

client = TestClient(app)
jira_client_mock = JiraClient("dummy-path")
klass_client_mock = KlassClient("dummy-path")


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


def test_org_info():
    app.dependency_overrides[get_klass_client] = lambda: klass_client_mock

    klass_versions_response = {
        "versions": [
            {
                "validFrom": "2000-01-01",
                "_links": {
                    "self": {
                        "href": "https://data.ssb.no/api/klass/v1/versions/1"
                    }
                }
            },
            {
                "validFrom": "2010-01-01",
                "_links": {
                    "self": {
                        "href": "https://data.ssb.no/api/klass/v1/versions/2"
                    }
                }
            }
        ]
    }
    klass_latest_version_response = {
        "classificationItems": [
            {
                "code": "1",
                "name": "Avdeling 1",
                "level": "1"
            },
            {
                "code": "11",
                "parentCode": "1",
                "name": "Seksjon 11",
                "level": "2"
            },
            {
                "code": "12",
                "parentCode": "1",
                "name": "Seksjon 12",
                "level": "2"
            }
        ]
    }

    klass_client_mock.get_sectional_division_versions = lambda arg: klass_versions_response
    klass_client_mock.get_latest_sectional_division_version = lambda arg: klass_latest_version_response

    client_response = [
        {
            "code": "11",
            "name": "Seksjon 11",
            "parent_code": "1"
        },
        {
            "code": "12",
            "name": "Seksjon 12",
            "parent_code": "1"
        }
    ]

    response = client.get("/org_info")

    assert response.status_code == 200
    assert response.json() == client_response
