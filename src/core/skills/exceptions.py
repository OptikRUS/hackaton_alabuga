from src.core.exceptions import BaseExceptionError


class SkillNotFoundError(BaseExceptionError):
    detail = "Skill not found"


class SkillNameAlreadyExistError(BaseExceptionError):
    detail = "Skill name already exists"


class SkillLevelIncreaseTooHighError(BaseExceptionError):
    detail = "Level increase exceeds skill max level"
