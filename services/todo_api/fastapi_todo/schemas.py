from pydantic import BaseModel

class TodoBase(BaseModel):
    title: str
    description: str | None = None
    is_done: bool = False

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int

    class Config:
        orm_mode = True