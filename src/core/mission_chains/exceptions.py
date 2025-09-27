from src.core.exceptions import BaseExceptionError


class MissionChainNameAlreadyExistError(BaseExceptionError):
    detail = "Mission chain with this name already exist!"


class MissionChainNotFoundError(BaseExceptionError):
    detail = "Mission chain not found!"


class MissionChainMissionAlreadyExistsError(BaseExceptionError):
    detail = "This mission is already in the mission chain!"


class MissionDependencyAlreadyExistsError(BaseExceptionError):
    detail = "This mission dependency already exists!"
