from src.core.exceptions import BaseExceptionError


class MissionNotFoundError(BaseExceptionError):
    detail = "Mission not found"


class MissionNameAlreadyExistError(BaseExceptionError):
    detail = "Mission with this title already exist!"


class MissionCompetencyRewardAlreadyExistsError(BaseExceptionError):
    detail = "This competency reward already exists for the mission"


class MissionSkillRewardAlreadyExistsError(BaseExceptionError):
    detail = "This skill reward already exists for the mission"


class PrerequisiteMissionNotFoundError(BaseExceptionError):
    detail = "Prerequisite mission not found!"


class MissionNotCompletedError(BaseExceptionError):
    detail = "Mission is not completed yet"
