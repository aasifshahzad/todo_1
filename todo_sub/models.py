from sqlmodel import Field, SQLModel
from typing import Optional


class Todo(SQLModel, table=True):
    id: int = Field(default=None, index=True, nullable=False, primary_key=True)
    title: str
    description: str
    completed: bool = False
    category: str
    

class TodoUpdate(SQLModel):
    title: Optional[str] | None = None
    description: Optional[str] | None = None
    completed: Optional[bool] | None = None
    category: Optional[str] | None = None