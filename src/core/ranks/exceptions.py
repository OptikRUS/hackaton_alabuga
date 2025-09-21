from src.core.exceptions import BaseExceptionError


class RankNotFoundError(BaseExceptionError):
    detail = "Rank not found"


class RankNameAlreadyExistError(BaseExceptionError):
    detail = "Rank name already exists"


class RankCompetencyMinLevelTooHighError(BaseExceptionError):
    detail = "Minimum level exceeds competency max level"
