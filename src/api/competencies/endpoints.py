from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status

from src.api.competencies.schemas import (
    CompetenciesResponse,
    CompetencyCreateRequest,
    CompetencyResponse,
    CompetencyUpdateRequest,
)
from src.core.competencies.use_cases import (
    AddSkillToCompetencyUseCase,
    CreateCompetencyUseCase,
    DeleteCompetencyUseCase,
    GetCompetenciesUseCase,
    GetCompetencyDetailUseCase,
    RemoveSkillFromCompetencyUseCase,
    UpdateCompetencyUseCase,
)

router = APIRouter(tags=["competencies"], route_class=DishkaRoute)


@router.post(path="/competencies", status_code=status.HTTP_201_CREATED)
async def create_competency(
    body: CompetencyCreateRequest,
    use_case: FromDishka[CreateCompetencyUseCase],
) -> CompetencyResponse:
    competency = await use_case.execute(competency=body.to_schema())
    return CompetencyResponse.from_schema(competency=competency)


@router.get(path="/competencies", status_code=status.HTTP_200_OK)
async def get_competencies(
    use_case: FromDishka[GetCompetenciesUseCase],
) -> CompetenciesResponse:
    competencies = await use_case.execute()
    return CompetenciesResponse.from_schema(competencies=competencies)


@router.get(path="/competencies/{competency_id}", status_code=status.HTTP_200_OK)
async def get_competency(
    competency_id: int,
    use_case: FromDishka[GetCompetencyDetailUseCase],
) -> CompetencyResponse:
    competency = await use_case.execute(competency_id=competency_id)
    return CompetencyResponse.from_schema(competency=competency)


@router.put(path="/competencies/{competency_id}", status_code=status.HTTP_200_OK)
async def update_competency(
    competency_id: int,
    body: CompetencyUpdateRequest,
    use_case: FromDishka[UpdateCompetencyUseCase],
) -> CompetencyResponse:
    competency = await use_case.execute(competency=body.to_schema(competency_id=competency_id))
    return CompetencyResponse.from_schema(competency=competency)


@router.delete(path="/competencies/{competency_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_competency(
    competency_id: int,
    use_case: FromDishka[DeleteCompetencyUseCase],
) -> None:
    await use_case.execute(competency_id=competency_id)


@router.post(path="/competencies/{competency_id}/skills/{skill_id}", status_code=status.HTTP_200_OK)
async def add_skill_to_competency(
    competency_id: int,
    skill_id: int,
    use_case: FromDishka[AddSkillToCompetencyUseCase],
) -> CompetencyResponse:
    competency = await use_case.execute(competency_id=competency_id, skill_id=skill_id)
    return CompetencyResponse.from_schema(competency=competency)


@router.delete(
    path="/competencies/{competency_id}/skills/{skill_id}", status_code=status.HTTP_200_OK
)
async def remove_skill_from_competency(
    competency_id: int,
    skill_id: int,
    use_case: FromDishka[RemoveSkillFromCompetencyUseCase],
) -> CompetencyResponse:
    competency = await use_case.execute(competency_id=competency_id, skill_id=skill_id)
    return CompetencyResponse.from_schema(competency=competency)
