from fastapi.testclient import TestClient
from server.api import app
client = TestClient(app)


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
