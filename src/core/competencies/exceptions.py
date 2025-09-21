from src.core.exceptions import BaseExceptionError


class CompetencyNotFoundError(BaseExceptionError):
    detail = "Competency not found"


class CompetencyNameAlreadyExistError(BaseExceptionError):
    detail = "Competency name already exists"


class CompetencyLevelIncreaseTooHighError(BaseExceptionError):
    detail = "Level increase exceeds competency max level"
