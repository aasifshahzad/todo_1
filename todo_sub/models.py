from sqlmodel import Field, SQLModel

class Todo(SQLModel, table=True):
    id: int = Field(default=None, index=True, nullable=False, primary_key=True)
    title: str
    description: str
    completed: bool = False
    category: str
