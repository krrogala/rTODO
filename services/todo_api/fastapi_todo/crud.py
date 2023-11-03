from sqlalchemy.orm import Session
from . import models, schemas

def get_todos(db: Session, skip: int = 0, limit: int = 10):
    print(skip, limit)
    return db.query(models.Todo).offset(skip).limit(limit).all()

def get_do(db: Session, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()

def create_do(db: Session, todo: schemas.TodoCreate):
    db_todo = models.Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_do(db: Session, todo_id: int):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    db.delete(db_todo)
    db.commit()
    return db_todo