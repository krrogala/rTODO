# fastapi_todo/crud.py

from sqlalchemy.future import select

from .database import AsyncSessionLocal
from .models import Todo


async def create_todo(todo: dict):
    async with AsyncSessionLocal() as session:
        new_todo = Todo(**todo)
        session.add(new_todo)
        await session.commit()
        await session.refresh(new_todo)
        return new_todo


async def get_todos():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Todo))
        todos = result.scalars().all()
        return todos
