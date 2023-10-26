import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_todo.database import Base, TestingSessionLocal, test_engine
from fastapi_todo.main import app
from fastapi_todo import models
import pytest_asyncio

@pytest_asyncio.fixture
async def override_test_engine():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def db_session(override_test_engine) -> AsyncSession:
    async with TestingSessionLocal() as session:
        yield session

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_create_todo(client, db_session):
    response = await client.post("/todos/", json={"title": "Test Todo"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert "id" in data
    db_todo = await db_session.get(models.Todo, data["id"])
    print(db_todo)
    assert db_todo is not None
    assert db_todo.title == "Test Todo"