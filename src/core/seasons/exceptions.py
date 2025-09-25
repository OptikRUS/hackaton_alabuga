from src.core.exceptions import BaseExceptionError


class SeasonNameAlreadyExistError(BaseExceptionError):
    detail = "Mission season name already exists"


class SeasonNotFoundError(BaseExceptionError):
    detail = "Mission season not found"
