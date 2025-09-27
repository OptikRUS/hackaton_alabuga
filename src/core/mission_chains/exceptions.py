from src.core.exceptions import BaseExceptionError


class MissionChainNotFoundError(BaseExceptionError):
    message = "Цепочка миссий не найдена"


class MissionChainNameAlreadyExistError(BaseExceptionError):
    message = "Цепочка миссий с таким названием уже существует"
