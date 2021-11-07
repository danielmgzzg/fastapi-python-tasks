from .schemas import *
from .exceptions import *
from .database import collection
from .utils import get_time, get_uuid
from fastapi.responses import JSONResponse


class TasksAPI:
    @staticmethod
    def get(task_id: str) -> TaskRead:
        """Retrieve a single Task by its unique id"""
        document = collection.find_one({"_id": task_id})
        if not document:
            raise TaskNotFoundException(task_id)
        return TaskRead(**document)

    @staticmethod
    def list() -> TaskRead:
        """Retrieve all the available tasks"""
        cursor = collection.find()
        return [TaskRead(**document) for document in cursor]

    @staticmethod
    def create(create: TaskCreate) -> TaskRead:
        """Create a task and return its Read object"""
        document = create.dict()
        document["created"] = document["updated"] = get_time()
        document["_id"] = get_uuid()
        if "deadline" in document:
            document["deadline"] = document.pop("deadline").isoformat()

        result = collection.insert_one(document)
        assert result.acknowledged

        return TasksAPI.get(result.inserted_id)

    @staticmethod
    def update(task_id: str, update: TaskUpdate):
        """Update a task by giving only the fields to update"""
        document = update.dict()
        document["updated"] = get_time()
        if "deadline" in document:
            document["deadline"] = document.pop("deadline").isoformat()

        result = collection.update_one({"_id": task_id}, {"$set": document})
        assert result.acknowledged
        if not result.modified_count:
            raise TaskNotFoundException(task_id)

        return TasksAPI.get(task_id)

    @staticmethod
    def delete(task_id: str):
        """Delete a task given its unique id"""
        result = collection.delete_one({"_id": task_id})
        if not result.deleted_count:
            raise TaskNotFoundException(task_id)
        return JSONResponse(
            status_code=200,
            content={"_id": task_id}
        )
