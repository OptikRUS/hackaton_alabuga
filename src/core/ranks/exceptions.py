from src.core.exceptions import BaseExceptionError


class RankNotFoundError(BaseExceptionError):
    detail = "Rank not found"


class RankNameAlreadyExistError(BaseExceptionError):
    detail = "Rank name already exists"


class RankCompetencyMinLevelTooHighError(BaseExceptionError):
    detail = "Minimum level exceeds competency max level"


class RankCompetencyRequirementAlreadyExistsError(BaseExceptionError):
    detail = "This competency requirement already exists for the rank"


class RankMissionRequirementAlreadyExistsError(BaseExceptionError):
    detail = "This mission requirement already exists for the rank"
