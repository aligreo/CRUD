from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db import get_db, Task


app = FastAPI()

templates = Jinja2Templates(directory="templates")

class TaskCheck(BaseModel):
    title: str
    is_completed: bool 

    class Config:
        from_attributes = True

#create a new task
@app.post("/add_task", response_model=TaskCheck)
def add_task(task: TaskCheck, db=Depends(get_db)):
    new_task = Task(title=task.title, is_completed=task.is_completed)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
    
# read all tasks
@app.get("/")
def index(request: Request, db=Depends(get_db)):
    all_tasks = db.query(Task).all()
    return templates.TemplateResponse(name="index.html",
                                      context= {"request": request, "tasks": all_tasks})

@app.get("/task/{task_id}")
def get_task(request: Request, task_id: int, db=Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    return templates.TemplateResponse(name="task.html",
                                      context= {"request": request, "task": task})

# update a task
@app.put("/update_task/{task_id}", response_model=TaskCheck)
def update_task(task_id: int, task: TaskCheck, db=Depends(get_db)):
    selected_task = db.query(Task).filter(Task.id == task_id).first()
    if selected_task:
        selected_task.title = task.title
        selected_task.is_completed = task.is_completed
        db.commit()
        db.refresh(selected_task)
        return selected_task
    return {"error": "Task not found"}