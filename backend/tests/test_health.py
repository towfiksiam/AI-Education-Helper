import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_ok():
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("status") == "ok"
    assert "service" in data
    assert "version" in data
