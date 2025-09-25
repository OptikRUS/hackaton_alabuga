from collections.abc import Callable, Coroutine
from typing import Any

from fastapi import Request, status
from fastapi.responses import JSONResponse, Response

from src.core.artifacts.exceptions import ArtifactNotFoundError, ArtifactTitleAlreadyExistError
from src.core.competencies.exceptions import (
    CompetencyLevelIncreaseTooHighError,
    CompetencyNameAlreadyExistError,
    CompetencyNotFoundError,
    CompetencySkillRelationAlreadyExistsError,
)
from src.core.exceptions import BaseExceptionError, InvalidJWTTokenError, PermissionDeniedError
from src.core.media.exceptions import MediaNotFoundError
from src.core.missions.exceptions import (
    MissionCompetencyRewardAlreadyExistsError,
    MissionNameAlreadyExistError,
    MissionNotFoundError,
    MissionSkillRewardAlreadyExistsError,
)
from src.core.ranks.exceptions import (
    RankCompetencyMinLevelTooHighError,
    RankCompetencyRequirementAlreadyExistsError,
    RankMissionRequirementAlreadyExistsError,
    RankNameAlreadyExistError,
    RankNotFoundError,
)
from src.core.seasons.exceptions import SeasonNameAlreadyExistError, SeasonNotFoundError
from src.core.skills.exceptions import (
    SkillLevelIncreaseTooHighError,
    SkillNameAlreadyExistError,
    SkillNotFoundError,
)
from src.core.tasks.exceptions import (
    TaskNameAlreadyExistError,
    TaskNotFoundError,
)
from src.core.users.exceptions import (
    UserAlreadyExistError,
    UserIncorrectCredentialsError,
    UserNotFoundError,
)


async def internal_server_error_exception_handler(_: Request, __: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "INTERNAL SERVER ERROR"},
    )


def handler(status_code: int) -> Callable[..., Coroutine[Any, Any, JSONResponse]]:
    async def error(_: Request, exc: BaseExceptionError) -> JSONResponse:
        return JSONResponse(
            status_code=status_code,
            content={"detail": exc.detail},
        )

    return error


exception_handlers: (
    dict[
        int | type[Exception],
        Callable[[Request, Any], Coroutine[Any, Any, Response]],
    ]
    | None
) = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: internal_server_error_exception_handler,
    BaseExceptionError: internal_server_error_exception_handler,
    InvalidJWTTokenError: handler(status_code=status.HTTP_401_UNAUTHORIZED),
    PermissionDeniedError: handler(status_code=status.HTTP_403_FORBIDDEN),
    UserNotFoundError: handler(status_code=status.HTTP_404_NOT_FOUND),
    UserAlreadyExistError: handler(status_code=status.HTTP_409_CONFLICT),
    UserIncorrectCredentialsError: handler(status_code=status.HTTP_401_UNAUTHORIZED),
    SeasonNameAlreadyExistError: handler(status_code=status.HTTP_409_CONFLICT),
    SeasonNotFoundError: handler(status_code=status.HTTP_404_NOT_FOUND),
    MissionNameAlreadyExistError: handler(status_code=status.HTTP_409_CONFLICT),
    MissionNotFoundError: handler(status_code=status.HTTP_404_NOT_FOUND),
    MissionCompetencyRewardAlreadyExistsError: handler(status_code=status.HTTP_409_CONFLICT),
    MissionSkillRewardAlreadyExistsError: handler(status_code=status.HTTP_409_CONFLICT),
    TaskNameAlreadyExistError: handler(status_code=status.HTTP_409_CONFLICT),
    TaskNotFoundError: handler(status_code=status.HTTP_404_NOT_FOUND),
    MediaNotFoundError: handler(status_code=status.HTTP_404_NOT_FOUND),
    ArtifactNotFoundError: handler(status_code=status.HTTP_404_NOT_FOUND),
    ArtifactTitleAlreadyExistError: handler(status_code=status.HTTP_409_CONFLICT),
    CompetencyNameAlreadyExistError: handler(status_code=status.HTTP_409_CONFLICT),
    CompetencyNotFoundError: handler(status_code=status.HTTP_404_NOT_FOUND),
    CompetencyLevelIncreaseTooHighError: handler(status_code=status.HTTP_400_BAD_REQUEST),
    CompetencySkillRelationAlreadyExistsError: handler(status_code=status.HTTP_409_CONFLICT),
    RankNameAlreadyExistError: handler(status_code=status.HTTP_409_CONFLICT),
    RankNotFoundError: handler(status_code=status.HTTP_404_NOT_FOUND),
    RankCompetencyMinLevelTooHighError: handler(status_code=status.HTTP_400_BAD_REQUEST),
    RankCompetencyRequirementAlreadyExistsError: handler(status_code=status.HTTP_409_CONFLICT),
    RankMissionRequirementAlreadyExistsError: handler(status_code=status.HTTP_409_CONFLICT),
    SkillNameAlreadyExistError: handler(status_code=status.HTTP_409_CONFLICT),
    SkillNotFoundError: handler(status_code=status.HTTP_404_NOT_FOUND),
    SkillLevelIncreaseTooHighError: handler(status_code=status.HTTP_400_BAD_REQUEST),
}
