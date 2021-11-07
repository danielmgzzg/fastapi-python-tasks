from datetime import date, datetime
from pydantic import BaseModel, Field
from typing import Optional, List


class BaseModel(BaseModel):
    """All data models inherit from this class"""

    def dict(self, include_nulls=False, **kwargs):
        """Override the super dict method by removing null keys from the dict, unless include_nulls=True"""
        kwargs["exclude_none"] = not include_nulls
        return super().dict(**kwargs)


class TaskFields:
    name = Field(
        description="Full name of this task",
        example="Esse quasi qui quam sunt sit sed.",

    )
    description = Field(
        description="Description text of the task",
        example="""Facere consequatur saepe fugit ipsum repellendus quisquam deleniti. 
                Commodi numquam odit laudantium consequatur. Minima et quo autem sed magni architecto quo. 
                Ipsam numquam cum in sapiente aut nesciunt.""",
    )

    completed = Field(
        description="Status of the Task",
        example=False
    )
    deadline = Field(
        description="Deadline of the Task to be completed",
        example="2021-11-07"
    )
    id = Field(
        description="Unique identifier of this task in the database",
        example="0dbb6101-0d94-56af-91fe-75d9805a7c05",
        alias="_id"
    )
    """The id is the _id field of Mongo documents, and is set on TasksAPI.create"""

    created = Field(
        alias="created",
        description="When the task was registered (Unix timestamp)",

    )
    """Created is set on TasksAPI.create"""
    updated = Field(
        alias="updated",
        description="When the task was updated for the last time (Unix timestamp)",

    )
    """Created is set on TasksAPI.update (and initially on create)"""


class TaskUpdate(BaseModel):
    """Body of Task PATCH requests"""
    name: Optional[str] = TaskFields.name
    description: Optional[str] = TaskFields.description
    deadline: Optional[date] = TaskFields.deadline
    completed: Optional[bool] = TaskFields.completed


class TaskCreate(TaskUpdate):
    """Body of Task POST requests"""
    name: str = TaskFields.name
    completed: Optional[bool] = TaskFields.completed
    description: Optional[str] = TaskFields.description
    deadline: Optional[date] = TaskFields.deadline


class TaskRead(TaskCreate):
    """Body of Task GET and POST responses"""
    id: str = TaskFields.id
    name: str = TaskFields.name
    description: Optional[str] = TaskFields.description
    deadline: Optional[date] = TaskFields.deadline
    completed: Optional[bool] = TaskFields.completed
    created: datetime = TaskFields.created
    updated: datetime = TaskFields.updated


TasksRead = List[TaskRead]


class BaseError(BaseModel):
    message: str = Field(..., description="Error message or description")


class BaseIdentifiedError(BaseError):
    identifier: str = Field(...,
                            description="Unique identifier which this error references to")


class NotFoundError(BaseIdentifiedError):
    """The entity does not exist"""
    pass


class AlreadyExistsError(BaseIdentifiedError):
    """An entity being created already exists"""
    pass
