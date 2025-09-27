from src.core.exceptions import BaseExceptionError


class MissionNotFoundError(BaseExceptionError):
    detail = "Mission not found"


class MissionNameAlreadyExistError(BaseExceptionError):
    detail = "Mission with this title already exist!"


class MissionCompetencyRewardAlreadyExistsError(BaseExceptionError):
    detail = "This competency reward already exists for the mission"


class MissionSkillRewardAlreadyExistsError(BaseExceptionError):
    detail = "This skill reward already exists for the mission"


class MissionChainNameAlreadyExistError(BaseExceptionError):
    detail = "Mission chain with this name already exist!"


class MissionChainNotFoundError(BaseExceptionError):
    detail = "Mission chain not found!"
