from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status

from src.api.missions.schemas import (
    MissionBranchCreateRequest,
    MissionBranchesResponse,
    MissionBranchResponse,
)
from src.core.missions.use_cases import CreateMissionBranchUseCase, GetMissionBranchesUseCase

router = APIRouter(tags=["missions"], route_class=DishkaRoute)


@router.post(path="/missions/branches", status_code=status.HTTP_201_CREATED)
async def create_mission_branch(
    body: MissionBranchCreateRequest,
    use_case: FromDishka[CreateMissionBranchUseCase],
) -> MissionBranchResponse:
    branch = await use_case.execute(branch=body.to_schema())
    return MissionBranchResponse.from_schema(branch=branch)


@router.get(path="/missions/branches", status_code=status.HTTP_200_OK)
async def get_mission_branches(
    use_case: FromDishka[GetMissionBranchesUseCase],
) -> MissionBranchesResponse:
    branches = await use_case.execute()
    return MissionBranchesResponse.from_schema(branches=branches)
