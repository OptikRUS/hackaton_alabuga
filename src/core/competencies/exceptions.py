from src.core.exceptions import BaseExceptionError


class CompetencyNotFoundError(BaseExceptionError):
    detail = "Competency not found"


class CompetencyNameAlreadyExistError(BaseExceptionError):
    detail = "Competency name already exists"


class CompetencyLevelIncreaseTooHighError(BaseExceptionError):
    detail = "Level increase exceeds competency max level"


class CompetencySkillRelationAlreadyExistsError(BaseExceptionError):
    detail = "This skill is already linked to the competency"
