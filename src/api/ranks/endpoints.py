from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status

from src.api.ranks.schemas import (
    RankCreateRequest,
    RankResponse,
    RankUpdateRequest,
    RanksResponse,
)
from src.core.ranks.use_cases import (
    CreateRankUseCase,
    DeleteRankUseCase,
    GetRankDetailUseCase,
    GetRanksUseCase,
    UpdateRankUseCase,
)


router = APIRouter(tags=["ranks"], route_class=DishkaRoute)


@router.post(path="/ranks", status_code=status.HTTP_201_CREATED)
async def create_rank(
    body: RankCreateRequest,
    use_case: FromDishka[CreateRankUseCase],
) -> RankResponse:
    rank = await use_case.execute(rank=body.to_schema())
    return RankResponse.from_schema(rank=rank)


@router.get(path="/ranks", status_code=status.HTTP_200_OK)
async def get_ranks(
    use_case: FromDishka[GetRanksUseCase],
) -> RanksResponse:
    ranks = await use_case.execute()
    return RanksResponse.from_schema(ranks=ranks)


@router.get(path="/ranks/{rank_id}", status_code=status.HTTP_200_OK)
async def get_rank(
    rank_id: int,
    use_case: FromDishka[GetRankDetailUseCase],
) -> RankResponse:
    rank = await use_case.execute(rank_id=rank_id)
    return RankResponse.from_schema(rank=rank)


@router.put(path="/ranks/{rank_id}", status_code=status.HTTP_200_OK)
async def update_rank(
    rank_id: int,
    body: RankUpdateRequest,
    use_case: FromDishka[UpdateRankUseCase],
) -> RankResponse:
    rank = await use_case.execute(rank=body.to_schema(rank_id=rank_id))
    return RankResponse.from_schema(rank=rank)


@router.delete(path="/ranks/{rank_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rank(
    rank_id: int,
    use_case: FromDishka[DeleteRankUseCase],
) -> None:
    await use_case.execute(rank_id=rank_id)




