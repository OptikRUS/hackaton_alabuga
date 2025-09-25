from src.core.exceptions import BaseExceptionError


class MissionNotFoundError(BaseExceptionError):
    detail = "Mission not found"


class MissionNameAlreadyExistError(BaseExceptionError):
    detail = "Mission name already exists"


class MissionCompetencyRewardAlreadyExistsError(BaseExceptionError):
    detail = "This competency reward already exists for the mission"


class MissionSkillRewardAlreadyExistsError(BaseExceptionError):
    detail = "This skill reward already exists for the mission"
