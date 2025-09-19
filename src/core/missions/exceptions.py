from src.core.exceptions import BaseExceptionError


class MissionBranchAlreadyExistError(BaseExceptionError):
    detail = "Mission branch already exists"


class MissionBranchNotFoundError(BaseExceptionError):
    detail = "Mission branch not found"


class MissionNotFoundError(BaseExceptionError):
    detail = "Mission not found"


class MissionAlreadyExistError(BaseExceptionError):
    detail = "Mission already exists"
