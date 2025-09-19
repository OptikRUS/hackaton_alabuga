from src.core.exceptions import BaseExceptionError


class TaskNotFoundError(BaseExceptionError):
    detail = "Mission task not found"


class TaskNameAlreadyExistError(BaseExceptionError):
    detail = "Mission task name already exists"
