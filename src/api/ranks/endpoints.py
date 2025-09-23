from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status

from src.api.ranks.schemas import (
    RankCreateRequest,
    RankResponse,
    RanksResponse,
    RankUpdateRequest,
)
from src.core.ranks.use_cases import (
    AddRequiredCompetencyToRankUseCase,
    AddRequiredMissionToRankUseCase,
    CreateRankUseCase,
    DeleteRankUseCase,
    GetRankDetailUseCase,
    GetRanksUseCase,
    RemoveRequiredCompetencyFromRankUseCase,
    RemoveRequiredMissionFromRankUseCase,
    UpdateRankUseCase,
)

router = APIRouter(tags=["ranks"], route_class=DishkaRoute)


@router.post(
    path="/ranks",
    status_code=status.HTTP_201_CREATED,
    summary="Создать ранг",
    description="Создает новый ранг в системе",
)
async def create_rank(
    body: RankCreateRequest,
    use_case: FromDishka[CreateRankUseCase],
) -> RankResponse:
    rank = await use_case.execute(rank=body.to_schema())
    return RankResponse.from_schema(rank=rank)


@router.get(
    path="/ranks",
    status_code=status.HTTP_200_OK,
    summary="Получить список рангов",
    description="Возвращает все доступные ранги",
)
async def get_ranks(
    use_case: FromDishka[GetRanksUseCase],
) -> RanksResponse:
    ranks = await use_case.execute()
    return RanksResponse.from_schema(ranks=ranks)


@router.get(
    path="/ranks/{rank_id}",
    status_code=status.HTTP_200_OK,
    summary="Получить ранг по ID",
    description="Возвращает детальную информацию о ранге",
)
async def get_rank(
    rank_id: int,
    use_case: FromDishka[GetRankDetailUseCase],
) -> RankResponse:
    rank = await use_case.execute(rank_id=rank_id)
    return RankResponse.from_schema(rank=rank)


@router.put(
    path="/ranks/{rank_id}",
    status_code=status.HTTP_200_OK,
    summary="Обновить ранг",
    description="Обновляет данные указанного ранга",
)
async def update_rank(
    rank_id: int,
    body: RankUpdateRequest,
    use_case: FromDishka[UpdateRankUseCase],
) -> RankResponse:
    rank = await use_case.execute(rank=body.to_schema(rank_id=rank_id))
    return RankResponse.from_schema(rank=rank)


@router.delete(
    path="/ranks/{rank_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить ранг",
    description="Удаляет указанный ранг",
)
async def delete_rank(
    rank_id: int,
    use_case: FromDishka[DeleteRankUseCase],
) -> None:
    await use_case.execute(rank_id=rank_id)


@router.post(
    path="/ranks/{rank_id}/missions/{mission_id}",
    status_code=status.HTTP_200_OK,
    summary="Добавить обязательную миссию к рангу",
    description="Назначает миссию как обязательное требование для получения ранга",
)
async def add_required_mission_to_rank(
    rank_id: int,
    mission_id: int,
    use_case: FromDishka[AddRequiredMissionToRankUseCase],
) -> RankResponse:
    rank = await use_case.execute(rank_id=rank_id, mission_id=mission_id)
    return RankResponse.from_schema(rank=rank)


@router.delete(
    path="/ranks/{rank_id}/missions/{mission_id}",
    status_code=status.HTTP_200_OK,
    summary="Удалить обязательную миссию из ранга",
    description="Убирает миссию из обязательных требований для получения ранга",
)
async def remove_required_mission_from_rank(
    rank_id: int,
    mission_id: int,
    use_case: FromDishka[RemoveRequiredMissionFromRankUseCase],
) -> RankResponse:
    rank = await use_case.execute(rank_id=rank_id, mission_id=mission_id)
    return RankResponse.from_schema(rank=rank)


@router.post(
    path="/ranks/{rank_id}/competencies/{competency_id}",
    status_code=status.HTTP_200_OK,
    summary="Добавить обязательную компетенцию к рангу",
    description="Назначает компетенцию как обязательное требование для получения ранга",
)
async def add_required_competency_to_rank(
    rank_id: int,
    competency_id: int,
    min_level: int,
    use_case: FromDishka[AddRequiredCompetencyToRankUseCase],
) -> RankResponse:
    rank = await use_case.execute(
        rank_id=rank_id,
        competency_id=competency_id,
        min_level=min_level,
    )
    return RankResponse.from_schema(rank=rank)


@router.delete(
    path="/ranks/{rank_id}/competencies/{competency_id}",
    status_code=status.HTTP_200_OK,
    summary="Удалить обязательную компетенцию из ранга",
    description="Убирает компетенцию из обязательных требований для получения ранга",
)
async def remove_required_competency_from_rank(
    rank_id: int,
    competency_id: int,
    use_case: FromDishka[RemoveRequiredCompetencyFromRankUseCase],
) -> RankResponse:
    rank = await use_case.execute(rank_id=rank_id, competency_id=competency_id)
    return RankResponse.from_schema(rank=rank)
