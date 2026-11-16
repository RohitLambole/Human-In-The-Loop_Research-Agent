from datetime import UTC, datetime
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.core.auth import get_current_user
from app.core.database import get_db
from app.main import app


class FakeResult:
    def __init__(self, rows):
        self.rows = rows

    def scalars(self):
        return self

    def all(self):
        return self.rows


class FakeSession:
    def __init__(self):
        self.threads = {}

    def add(self, thread):
        if thread.thread_id is None:
            thread.thread_id = uuid4()
        if thread.created_at is None:
            thread.created_at = datetime.now(UTC)
        self.threads[thread.thread_id] = thread

    async def commit(self):
        return None

    async def refresh(self, thread):
        return None

    async def get(self, model, thread_id):
        return self.threads.get(thread_id)

    async def execute(self, statement):
        return FakeResult(list(self.threads.values()))


@pytest.fixture
def client():
    session = FakeSession()

    async def override_get_db():
        yield session

    async def user_a():
        return {"user_id": "user-a"}

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = user_a
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
