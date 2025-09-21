from src.core.exceptions import BaseExceptionError


class CompetitionNotFoundError(BaseExceptionError):
    detail = "Competition not found"


class CompetitionNameAlreadyExistError(BaseExceptionError):
    detail = "Competition name already exists"


