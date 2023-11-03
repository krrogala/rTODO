from fastapi import Depends, FastAPI, HTTPException


app = FastAPI()


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
