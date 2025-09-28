from src.core.exceptions import BaseExceptionError


class MissionChainNameAlreadyExistError(BaseExceptionError):
    detail = "Mission chain with this name already exist!"


class MissionChainNotFoundError(BaseExceptionError):
    detail = "Mission chain not found!"


class MissionChainMissionAlreadyExistsError(BaseExceptionError):
    detail = "This mission is already in the mission chain!"


class MissionDependencyAlreadyExistsError(BaseExceptionError):
    detail = "This mission dependency already exists!"


class InvalidMissionOrderError(BaseExceptionError):
    detail = (
        "Invalid mission order! Order must be between 1 and the number of missions in the chain."
    )


class CircularDependencyError(BaseExceptionError):
    detail = (
        "Circular dependency detected! Mission cannot depend on itself "
        "or create circular dependencies."
    )
