from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status

from src.api.auth.schemas import JwtHRUser, JwtUser
from src.api.mission_chains.schemas import (
    MissionChainCreateRequest,
    MissionChainResponse,
    MissionChainsResponse,
    MissionChainUpdateRequest,
)
from src.api.missions.schemas import MissionDependencyResponse
from src.api.openapi import openapi_extra
from src.core.mission_chains.use_cases import (
    AddMissionDependencyUseCase,
    AddMissionToChainUseCase,
    CreateMissionChainUseCase,
    DeleteMissionChainUseCase,
    GetMissionChainDetailUseCase,
    GetMissionChainsUseCase,
    RemoveMissionDependencyUseCase,
    RemoveMissionFromChainUseCase,
    UpdateMissionChainUseCase,
    UpdateMissionOrderInChainUseCase,
)

router = APIRouter(tags=["mission-chains"], route_class=DishkaRoute)


@router.post(
    path="/mission-chains",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_201_CREATED,
    summary="Создать цепочку миссий",
    description="Создает новую цепочку миссий в системе",
)
async def create_mission_chain(
    user: FromDishka[JwtHRUser],
    body: MissionChainCreateRequest,
    use_case: FromDishka[CreateMissionChainUseCase],
) -> MissionChainResponse:
    _ = user
    mission_chain = await use_case.execute(mission_chain=body.to_schema())
    return MissionChainResponse.from_schema(mission_chain=mission_chain)


@router.get(
    path="/mission-chains",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Получить список цепочек миссий",
    description="Возвращает все доступные цепочки миссий",
)
async def get_mission_chains(
    user: FromDishka[JwtUser],
    use_case: FromDishka[GetMissionChainsUseCase],
) -> MissionChainsResponse:
    _ = user
    mission_chains = await use_case.execute()
    return MissionChainsResponse.from_schema(mission_chains=mission_chains)


@router.get(
    path="/mission-chains/{chain_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Получить цепочку миссий по ID",
    description="Возвращает детальную информацию о цепочке миссий",
)
async def get_mission_chain(
    chain_id: int,
    user: FromDishka[JwtUser],
    use_case: FromDishka[GetMissionChainDetailUseCase],
) -> MissionChainResponse:
    _ = user
    mission_chain = await use_case.execute(chain_id=chain_id)
    return MissionChainResponse.from_schema(mission_chain=mission_chain)


@router.put(
    path="/mission-chains/{chain_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Обновить цепочку миссий",
    description="Обновляет данные указанной цепочки миссий",
)
async def update_mission_chain(
    chain_id: int,
    user: FromDishka[JwtHRUser],
    body: MissionChainUpdateRequest,
    use_case: FromDishka[UpdateMissionChainUseCase],
) -> MissionChainResponse:
    _ = user
    mission_chain = await use_case.execute(mission_chain=body.to_schema(chain_id=chain_id))
    return MissionChainResponse.from_schema(mission_chain=mission_chain)


@router.delete(
    path="/mission-chains/{chain_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить цепочку миссий",
    description="Удаляет указанную цепочку миссий",
)
async def delete_mission_chain(
    chain_id: int,
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[DeleteMissionChainUseCase],
) -> None:
    _ = user
    await use_case.execute(chain_id=chain_id)


@router.post(
    path="/mission-chains/{chain_id}/missions/{mission_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Добавить миссию в цепочку",
    description="Добавляет миссию в указанную цепочку",
)
async def add_mission_to_chain(
    chain_id: int,
    mission_id: int,
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[AddMissionToChainUseCase],
) -> MissionChainResponse:
    _ = user
    mission_chain = await use_case.execute(chain_id=chain_id, mission_id=mission_id)
    return MissionChainResponse.from_schema(mission_chain=mission_chain)


@router.delete(
    path="/mission-chains/{chain_id}/missions/{mission_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Удалить миссию из цепочки",
    description="Удаляет миссию из указанной цепочки",
)
async def remove_mission_from_chain(
    chain_id: int,
    mission_id: int,
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[RemoveMissionFromChainUseCase],
) -> MissionChainResponse:
    _ = user
    mission_chain = await use_case.execute(chain_id=chain_id, mission_id=mission_id)
    return MissionChainResponse.from_schema(mission_chain=mission_chain)


@router.put(
    path="/mission-chains/{chain_id}/missions/{mission_id}/order",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Обновить порядок миссии в цепочке",
    description="Обновляет порядок миссии в указанной цепочке",
)
async def update_mission_order_in_chain(
    chain_id: int,
    mission_id: int,
    new_order: int,
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[UpdateMissionOrderInChainUseCase],
) -> MissionChainResponse:
    _ = user
    mission_chain = await use_case.execute(
        chain_id=chain_id, mission_id=mission_id, new_order=new_order
    )
    return MissionChainResponse.from_schema(mission_chain=mission_chain)


@router.post(
    path="/mission-chains/{chain_id}/dependencies",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Добавить зависимость между миссиями в цепочке",
    description="Добавляет зависимость между миссиями внутри указанной цепочки",
)
async def add_mission_dependency(
    chain_id: int,
    body: MissionDependencyResponse,
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[AddMissionDependencyUseCase],
) -> MissionChainResponse:
    _ = user
    mission_chain = await use_case.execute(
        chain_id=chain_id,
        mission_id=body.mission_id,
        prerequisite_mission_id=body.prerequisite_mission_id,
    )
    return MissionChainResponse.from_schema(mission_chain=mission_chain)


@router.delete(
    path="/mission-chains/{chain_id}/dependencies",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Удалить зависимость между миссиями в цепочке",
    description="Удаляет зависимость между миссиями внутри указанной цепочки",
)
async def remove_mission_dependency(
    chain_id: int,
    body: MissionDependencyResponse,
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[RemoveMissionDependencyUseCase],
) -> MissionChainResponse:
    _ = user
    mission_chain = await use_case.execute(
        chain_id=chain_id,
        mission_id=body.mission_id,
        prerequisite_mission_id=body.prerequisite_mission_id,
    )
    return MissionChainResponse.from_schema(mission_chain=mission_chain)
