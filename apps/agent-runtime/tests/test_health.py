from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "agent-runtime"


def test_agent_run_placeholder():
    response = client.post(
        "/agent/run",
        json={
            "query": "Summarise the key findings.",
            "session_id": "test-session",
            "user_id": "local-user",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert isinstance(data["sources"], list)
    assert isinstance(data["tool_calls_made"], list)
