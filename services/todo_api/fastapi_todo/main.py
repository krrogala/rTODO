from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

from . import crud, database, models, schemas

app = FastAPI()


# Dependency to get the database session
async def get_db():
    async with database.AsyncSessionLocal() as db:
        yield db

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with database.engine.begin() as conn:
        await conn.run_async(models.Base.metadata.create_all)


@app.post("/todos/", response_model=schemas.Todo)
async def create_todo(todo: schemas.TodoCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_todo(db=db, todo=todo)


@app.get("/todos/", response_model=list[schemas.Todo])
async def read_todos(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    todos = await crud.get_todos(db, skip=skip, limit=limit)
    return todos


@app.get("/todos/{todo_id}", response_model=schemas.Todo)
async def read_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    db_todo = await crud.get_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo
