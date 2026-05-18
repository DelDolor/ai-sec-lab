from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "ai-gateway"


def test_chat_placeholder():
    response = client.post(
        "/chat",
        json={
            "message": "What is in the documents?",
            "session_id": "test-session",
            "user_id": "local-user",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["session_id"] == "test-session"
    assert data["policy_decision"] == "allowed"
