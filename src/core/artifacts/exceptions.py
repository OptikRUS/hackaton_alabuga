from src.core.exceptions import BaseExceptionError


class ArtifactNotFoundError(BaseExceptionError):
    detail = "Artifact not found error"


class ArtifactTitleAlreadyExistError(BaseExceptionError):
    detail = "Artifact title already exists"
