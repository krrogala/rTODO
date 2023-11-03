from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .models import Base, Todo
from .schemas import TodoCreate, Todo
from .database import engine, SessionLocal
from . import crud

app = FastAPI()

Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/todos/")
def todos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return todos

@app.get("/todos/{todo_id}")
def todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.get_do(db, todo_id=todo_id)
    return todo

@app.post("/todos/")
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    return crud.create_do(db=db, todo=todo)
