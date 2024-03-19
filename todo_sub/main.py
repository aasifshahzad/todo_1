from fastapi import FastAPI, Depends
from todo_sub.db_connect import engine, create_database_table, get_session
from todo_sub.models import Todo

from sqlmodel import Session, select

app = FastAPI(
    title="FastAPI Todo App",
    description="A simple todo app built with FastAPI",
    version="0.1.0",
    servers = [
        {   
            "url": "http://127.0.0.1:8000",
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

@app.get("/todos")
def get_todos(session: Session = Depends(get_session)):
    all_todos = session.exec(select(Todo)).all()
    return all_todos

@app.post("/add_todo")
def create_todo(todo: Todo, session: Session = Depends(get_session)):
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo