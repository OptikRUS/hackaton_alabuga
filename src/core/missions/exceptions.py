from src.core.exceptions import BaseExceptionError


class MissionBranchNameAlreadyExistError(BaseExceptionError):
    detail = "Mission branch name already exists"


class MissionBranchNotFoundError(BaseExceptionError):
    detail = "Mission branch not found"


class MissionNotFoundError(BaseExceptionError):
    detail = "Mission not found"


class MissionNameAlreadyExistError(BaseExceptionError):
    detail = "Mission name already exists"
