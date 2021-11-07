from typing import Optional
from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from .database import collection
from .api import TasksAPI
from .schemas import *
from .exceptions import *
from .settings import api_settings as settings

app = FastAPI(title=settings.title)


@app.get("/")
def index():
    return {"message": "Welcome to tasks API"}


@app.get(
    "/tasks",
    response_model=TasksRead,
    description="List all the tasks",
    tags=["tasks"]
)
def list_tasks():
    return TasksAPI.list()


@app.get(
    "/task/{id}",
    response_model=TaskRead,
    description="Get a single task by its unique ID",
    responses=get_exception_responses(TaskNotFoundException),
    tags=["tasks"]
)
def get_task(id: str):
    return TasksAPI.get(id)


@app.post(
    "/tasks",
    description="Create a new task",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
    responses=get_exception_responses(TaskAlreadyExistsException),
    tags=["tasks"]
)
def create_task(create: TaskCreate):
    return TasksAPI.create(create)


@app.patch(
    "/tasks/{id}",
    description="Update a single task by its unique ID, providing the fields to update",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=get_exception_responses(TaskNotFoundException,
                                      TaskAlreadyExistsException),
    tags=["tasks"]
)
def update_task(id: str, update: TaskUpdate):
    TasksAPI.update(id, update)


@app.delete(
    "/tasks/{id}",
    description="Delete a single task by its unique ID",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=get_exception_responses(TaskNotFoundException),
    tags=["tasks"]
)
def delete_task(id: str):
    TasksAPI.delete(id)


@app.exception_handler(TaskException)
async def task_exception_handler(request: Request, exc: TaskException):
    return JSONResponse(
        status_code=exc.code,
        content=exc.data.dict()
    )
