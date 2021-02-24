from typing import Optional
from pydantic import BaseModel

class Todo(BaseModel):
    id: int
    name: str
    description: str

class CreateTodo(BaseModel):
    name: str
    description: str

class UpdateTodo(BaseModel):
    name: Optional[str]
    description: Optional[str]