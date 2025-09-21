from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status

from src.api.competitions.schemas import (
    CompetitionCreateRequest,
    CompetitionResponse,
    CompetitionsResponse,
    CompetitionUpdateRequest,
)
from src.core.competitions.use_cases import (
    AddSkillToCompetitionUseCase,
    CreateCompetitionUseCase,
    DeleteCompetitionUseCase,
    GetCompetitionDetailUseCase,
    GetCompetitionsUseCase,
    RemoveSkillFromCompetitionUseCase,
    UpdateCompetitionUseCase,
)

router = APIRouter(tags=["competitions"], route_class=DishkaRoute)


@router.post(path="/competitions", status_code=status.HTTP_201_CREATED)
async def create_competition(
    body: CompetitionCreateRequest,
    use_case: FromDishka[CreateCompetitionUseCase],
) -> CompetitionResponse:
    competition = await use_case.execute(competition=body.to_schema())
    return CompetitionResponse.from_schema(competition=competition)


@router.get(path="/competitions", status_code=status.HTTP_200_OK)
async def get_competitions(
    use_case: FromDishka[GetCompetitionsUseCase],
) -> CompetitionsResponse:
    competitions = await use_case.execute()
    return CompetitionsResponse.from_schema(competitions=competitions)


@router.get(path="/competitions/{competition_id}", status_code=status.HTTP_200_OK)
async def get_competition(
    competition_id: int,
    use_case: FromDishka[GetCompetitionDetailUseCase],
) -> CompetitionResponse:
    competition = await use_case.execute(competition_id=competition_id)
    return CompetitionResponse.from_schema(competition=competition)


@router.put(path="/competitions/{competition_id}", status_code=status.HTTP_200_OK)
async def update_competition(
    competition_id: int,
    body: CompetitionUpdateRequest,
    use_case: FromDishka[UpdateCompetitionUseCase],
) -> CompetitionResponse:
    competition = await use_case.execute(competition=body.to_schema(competition_id=competition_id))
    return CompetitionResponse.from_schema(competition=competition)


@router.delete(path="/competitions/{competition_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_competition(
    competition_id: int,
    use_case: FromDishka[DeleteCompetitionUseCase],
) -> None:
    await use_case.execute(competition_id=competition_id)


@router.post(
    path="/competitions/{competition_id}/skills/{skill_id}", status_code=status.HTTP_200_OK
)
async def add_skill_to_competition(
    competition_id: int,
    skill_id: int,
    use_case: FromDishka[AddSkillToCompetitionUseCase],
) -> CompetitionResponse:
    competition = await use_case.execute(competition_id=competition_id, skill_id=skill_id)
    return CompetitionResponse.from_schema(competition=competition)


@router.delete(
    path="/competitions/{competition_id}/skills/{skill_id}", status_code=status.HTTP_200_OK
)
async def remove_skill_from_competition(
    competition_id: int,
    skill_id: int,
    use_case: FromDishka[RemoveSkillFromCompetitionUseCase],
) -> CompetitionResponse:
    competition = await use_case.execute(competition_id=competition_id, skill_id=skill_id)
    return CompetitionResponse.from_schema(competition=competition)
