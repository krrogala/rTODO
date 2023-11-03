from pydantic import BaseModel

class TodoBase(BaseModel):
    title: str
    description: str
    done: bool = False

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int

    class ConfigDict:
        from_attributes = True