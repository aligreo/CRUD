from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db import get_db, Task, User


app = FastAPI()

templates = Jinja2Templates(directory="templates")

class TaskCheck(BaseModel):
    title: str
    is_completed: bool

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: str

    class Config:
        from_attributes = True

# Create a new user
@app.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get all users
@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# Get user by ID
@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Create a new task for a user
@app.post("/users/{user_id}/tasks", response_model=TaskCheck)
def create_task_for_user(user_id: int, task: TaskCheck, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_task = Task(title=task.title, is_completed=task.is_completed, owner_id=user_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# Get all tasks for a user
@app.get("/users/{user_id}/tasks")
def get_tasks_by_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    tasks = db.query(Task).filter(Task.owner_id == user_id).all()
    return tasks

# Read all tasks (across all users)
@app.get("/")
def index(request: Request, db=Depends(get_db)):
    all_tasks = db.query(Task).all()
    all_users = db.query(User).all()
    print(all_tasks)
    return templates.TemplateResponse(name="index.html",
                                      context={"request": request, "tasks": all_tasks, "users": all_users})

# Get tasks for a specific user (for the form in index.html)
@app.get("/user-tasks")
def get_user_tasks(request: Request, user_id: int = None, db: Session = Depends(get_db)):
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        tasks = db.query(Task).filter(Task.owner_id == user_id).all()
    else:
        tasks = db.query(Task).all()
    
    all_users = db.query(User).all()
    return templates.TemplateResponse(name="index.html",
                                      context={"request": request, "tasks": tasks, "users": all_users})

@app.get("/task/{task_id}")
def get_task(request: Request, task_id: int, db=Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    return templates.TemplateResponse(name="task.html",
                                      context={"request": request, "task": task})

# Update a task
@app.put("/update_task/{task_id}", response_model=TaskCheck)
def update_task(task_id: int, task: TaskCheck, db=Depends(get_db)):
    selected_task = db.query(Task).filter(Task.id == task_id).first()
    if selected_task:
        for key, value in task.dict().items():
            setattr(selected_task, key, value)
        db.commit()
        db.refresh(selected_task)
        return selected_task
    return {"error": "Task not found"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()
    return {"message": f"Task {task_id} deleted successfully"}