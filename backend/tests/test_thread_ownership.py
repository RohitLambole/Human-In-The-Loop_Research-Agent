from uuid import UUID


def test_owner_can_create_and_read_session(client):
    created = client.post("/sessions")
    assert created.status_code == 201
    thread_id = created.json()["thread_id"]
    UUID(thread_id)

    state = client.get(f"/sessions/{thread_id}/state")
    assert state.status_code == 200
    assert state.json()["thread_id"] == thread_id
    assert state.json()["status"] == "running"


def test_other_user_cannot_read_or_resume_another_users_thread(client):
    created = client.post("/sessions")
    thread_id = created.json()["thread_id"]

    async def user_b():
        return {"user_id": "user-b"}

    from app.core.auth import get_current_user
    from app.main import app

    app.dependency_overrides[get_current_user] = user_b

    assert client.get(f"/sessions/{thread_id}/state").status_code == 404
    assert client.get(f"/sessions/{thread_id}/stream").status_code == 404
    assert client.post(f"/sessions/{thread_id}/resume", json={}).status_code == 404


def test_unknown_thread_is_not_disclosed(client):
    response = client.get("/sessions/00000000-0000-0000-0000-000000000001/state")
    assert response.status_code == 404
