from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status

from src.api.auth.schemas import JwtHRUser, JwtUser
from src.api.openapi import openapi_extra
from src.api.seasons.schemas import (
    SeasonCreateRequest,
    SeasonResponse,
    SeasonsResponse,
    SeasonUpdateRequest,
)
from src.core.missions.use_cases import (
    CreateMissionBranchUseCase,
    DeleteMissionBranchUseCase,
    GetMissionBranchDetailUseCase,
    GetMissionBranchesUseCase,
    UpdateMissionBranchUseCase,
)

router = APIRouter(tags=["seasons"], route_class=DishkaRoute)


@router.post(
    path="/seasons",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_201_CREATED,
    summary="Создать сезон",
    description="Создает новый сезон миссий в системе",
)
async def create_season(
    user: FromDishka[JwtHRUser],
    body: SeasonCreateRequest,
    use_case: FromDishka[CreateMissionBranchUseCase],
) -> SeasonResponse:
    _ = user
    branch = await use_case.execute(branch=body.to_schema())
    return SeasonResponse.from_schema(branch=branch)


@router.get(
    path="/seasons",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Получить список сезонов",
    description="Возвращает все доступные сезоны миссий",
)
async def get_seasons(
    user: FromDishka[JwtUser],
    use_case: FromDishka[GetMissionBranchesUseCase],
) -> SeasonsResponse:
    _ = user
    branches = await use_case.execute()
    return SeasonsResponse.from_schema(branches=branches)


@router.get(
    path="/seasons/{season_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Получить сезон по ID",
    description="Возвращает детальную информацию о сезоне миссий",
)
async def get_season(
    season_id: int,
    user: FromDishka[JwtUser],
    use_case: FromDishka[GetMissionBranchDetailUseCase],
) -> SeasonResponse:
    _ = user
    branch = await use_case.execute(branch_id=season_id)
    return SeasonResponse.from_schema(branch=branch)


@router.put(
    path="/seasons/{season_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Обновить сезон",
    description="Обновляет данные указанного сезона миссий",
)
async def update_season(
    season_id: int,
    user: FromDishka[JwtHRUser],
    body: SeasonUpdateRequest,
    use_case: FromDishka[UpdateMissionBranchUseCase],
) -> SeasonResponse:
    _ = user
    branch = await use_case.execute(branch=body.to_schema(branch_id=season_id))
    return SeasonResponse.from_schema(branch=branch)


@router.delete(
    path="/seasons/{season_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить сезон",
    description="Удаляет указанный сезон миссий",
)
async def delete_season(
    season_id: int,
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[DeleteMissionBranchUseCase],
) -> None:
    _ = user
    await use_case.execute(branch_id=season_id)
