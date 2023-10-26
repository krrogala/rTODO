from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from . import models, schemas


async def get_todo(db: AsyncSession, todo_id: int):
    result = await db.execute(select(models.Todo).filter_by(id=todo_id))
    return await result.scalar()


async def get_todos(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.Todo).offset(skip).limit(limit))
    return result.scalars().all()


async def create_todo(db: AsyncSession, todo: schemas.TodoCreate):
    db_todo = models.Todo(**todo.model_dump())
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo
