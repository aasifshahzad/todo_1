from fastapi import FastAPI, Depends
from todo_sub.db_connect import engine, create_database_table, get_session
from todo_sub.models import Todo

from sqlmodel import Session, select
from fastapi import HTTPException

app = FastAPI(
    title="FastAPI Todo App",
    description="A simple todo app built with FastAPI",
    version="0.1.0",
    servers = [
        {   
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {   
            "url": "kashan.org",
            "description": "Production server"
        }
    ]
)

@app.get("/")
def get_root():
    return {"Application Status": "Todo App is UP!"}

@app.on_event("startup")
def startup_event():
    create_database_table(engine)

@app.get("/todos") # Retrieve
def get_todos(session: Session = Depends(get_session)):
    all_todos = session.exec(select(Todo)).all()
    return all_todos

@app.post("/create_todo") # Create
def create_todo(todo: Todo, session: Session = Depends(get_session)):
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@app.delete("/delete_todo/{title}") # Delete
def delete_todo(title: str, session: Session = Depends(get_session)):
    todo = session.exec(select(Todo).where(Todo.title == title)).first()
    if todo:
        session.delete(todo)
        session.commit()
        return {"message": "Todo deleted successfully"}
    else:
        return {"message": "Todo not found"}
    
    
@app.put("/update_todo/{title}") # Update
def update_todo(title: str, todo: Todo, session: Session = Depends(get_session)):
    existing_todo = session.exec(select(Todo).where(Todo.title == title)).first()
    if existing_todo:
        existing_todo.title = todo.title
        existing_todo.description = todo.description
        existing_todo.completed = todo.completed
        existing_todo.category = todo.category
        session.commit()
        session.refresh(existing_todo)
        return existing_todo
    else:
        return {"message": "Todo not found"}
    
    
@app.patch("/update_todo_value/{title}") #Update single column value
def update_todo_value(title: str, todo: Todo, session: Session = Depends(get_session)):
    existing_todo = session.exec(select(Todo).where(Todo.title == title)).first()
    if not existing_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
