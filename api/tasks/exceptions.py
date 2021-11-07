from typing import Type
from fastapi import status
from pydantic import BaseModel, Field
from .schemas import *


class TaskException(Exception):
    """Base error for custom API exceptions"""
    message = "Generic error"
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    model = BaseError

    def __init__(self, **kwargs):
        kwargs.setdefault("message", self.message)
        self.message = kwargs["message"]
        self.data = self.model(**kwargs)

    @classmethod
    def response_model(cls):
        return {cls.code: {"model": cls.model}}


class BaseIdentifiedException(TaskException):
    """Base error for exceptions related with entities, uniquely identified"""
    message = "Entity error"
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    model = BaseIdentifiedError

    def __init__(self, identifier, **kwargs):
        super().__init__(identifier=identifier, **kwargs)


class NotFoundException(BaseIdentifiedException):
    """Base error for exceptions raised because an entity does not exist"""
    message = "The entity does not exist"
    code = status.HTTP_404_NOT_FOUND
    model = NotFoundError


class AlreadyExistsException(BaseIdentifiedException):
    """Base error for exceptions raised because an entity already exists"""
    message = "The entity already exists"
    code = status.HTTP_409_CONFLICT
    model = AlreadyExistsError


class TaskNotFoundException(NotFoundException):
    """Error raised when a task does not exist"""
    message = "The task does not exist"


class TaskAlreadyExistsException(AlreadyExistsException):
    """Error raised when a task already exists"""
    message = "The task already exists"


def get_exception_responses(*args: Type[TaskException]) -> dict:
    """Given TaskException classes, return a dict of responses used on FastAPI endpoint definition, with the format:
    {statuscode: schema, statuscode: schema, ...}"""
    responses = dict()
    for cls in args:
        responses.update(cls.response_model())
    return responses
