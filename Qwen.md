# CRUD Application Summary

## Project Overview
This is a simple CRUD (Create, Read, Update, Delete) web application built with FastAPI and SQLAlchemy. The application manages tasks with basic operations like adding, viewing, updating, and deleting tasks.

## Technologies Used
- **FastAPI**: Modern, fast web framework for building APIs with Python 3.7+
- **SQLAlchemy**: SQL toolkit and Object Relational Mapping (ORM) library
- **SQLite**: Lightweight disk-based database used for storing tasks
- **Jinja2 Templates**: Template engine for rendering HTML pages
- **Uvicorn**: ASGI server for running the FastAPI application

## Project Structure
```
CRUD/
├── db.py              # Database setup and model definition
├── main.py            # Main application with API routes
├── README.md          # Basic project description
├── requirements.txt   # Project dependencies
├── templates/         # HTML templates for frontend
│   ├── index.html     # Main page showing all tasks
│   └── task.html      # Individual task view/edit page
├── db/                # Directory containing SQLite database file
└── venv/              # Virtual environment (if activated)
```

## Features
- **Create**: Add new tasks via POST request to `/add_task`
- **Read**: View all tasks on the homepage `/` or individual task at `/task/{task_id}`
- **Update**: Modify existing tasks via PUT request to `/update_task/{task_id}`
- **Delete**: Remove tasks via DELETE request to `/tasks/{task_id}`

## Data Model
The application uses a single `Task` model with the following fields:
- `id`: Integer, primary key with auto-increment
- `title`: String, the task title
- `is_completed`: Boolean, completion status (defaults to False)

## API Endpoints
- `GET /` - Displays all tasks using index.html template
- `GET /task/{task_id}` - Shows details of a specific task using task.html template
- `POST /add_task` - Creates a new task
- `PUT /update_task/{task_id}` - Updates an existing task
- `DELETE /tasks/{task_id}` - Deletes a task

## Setup Instructions
1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `uvicorn main:app --reload`
3. Access the application at `http://localhost:8000`

## Database
The application creates an SQLite database file at `./db/tasks.db` and automatically creates the required tables on startup.