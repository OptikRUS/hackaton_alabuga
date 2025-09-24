from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status

from src.api.auth.schemas import JwtHRUser, JwtUser
from src.api.competencies.schemas import (
    CompetenciesResponse,
    CompetencyCreateRequest,
    CompetencyResponse,
    CompetencyUpdateRequest,
)
from src.api.openapi import openapi_extra
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


@router.post(
    path="/competencies",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_201_CREATED,
    summary="Создать компетенцию",
    description="Создает новую компетенцию в системе",
)
async def create_competency(
    body: CompetencyCreateRequest,
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[CreateCompetencyUseCase],
) -> CompetencyResponse:
    _ = user
    competency = await use_case.execute(competency=body.to_schema())
    return CompetencyResponse.from_schema(competency=competency)


@router.get(
    path="/competencies",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Получить список компетенций",
    description="Возвращает все доступные компетенции",
)
async def get_competencies(
    user: FromDishka[JwtUser],
    use_case: FromDishka[GetCompetenciesUseCase],
) -> CompetenciesResponse:
    _ = user
    competencies = await use_case.execute()
    return CompetenciesResponse.from_schema(competencies=competencies)


@router.get(
    path="/competencies/{competency_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Получить компетенцию по ID",
    description="Возвращает детальную информацию о компетенции",
)
async def get_competency(
    competency_id: int,
    user: FromDishka[JwtUser],
    use_case: FromDishka[GetCompetencyDetailUseCase],
) -> CompetencyResponse:
    _ = user
    competency = await use_case.execute(competency_id=competency_id)
    return CompetencyResponse.from_schema(competency=competency)


@router.put(
    path="/competencies/{competency_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Обновить компетенцию",
    description="Обновляет данные указанной компетенции",
)
async def update_competency(
    competency_id: int,
    user: FromDishka[JwtHRUser],
    body: CompetencyUpdateRequest,
    use_case: FromDishka[UpdateCompetencyUseCase],
) -> CompetencyResponse:
    _ = user
    competency = await use_case.execute(competency=body.to_schema(competency_id=competency_id))
    return CompetencyResponse.from_schema(competency=competency)


@router.delete(
    path="/competencies/{competency_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить компетенцию",
    description="Удаляет указанную компетенцию",
)
async def delete_competency(
    competency_id: int,
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[DeleteCompetencyUseCase],
) -> None:
    _ = user
    await use_case.execute(competency_id=competency_id)


@router.post(
    path="/competencies/{competency_id}/skills/{skill_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Добавить навык к компетенции",
    description="Назначает навык указанной компетенции",
)
async def add_skill_to_competency(
    competency_id: int,
    skill_id: int,
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[AddSkillToCompetencyUseCase],
) -> CompetencyResponse:
    _ = user
    competency = await use_case.execute(competency_id=competency_id, skill_id=skill_id)
    return CompetencyResponse.from_schema(competency=competency)


@router.delete(
    path="/competencies/{competency_id}/skills/{skill_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Удалить навык из компетенции",
    description="Убирает навык из указанной компетенции",
)
async def remove_skill_from_competency(
    competency_id: int,
    skill_id: int,
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[RemoveSkillFromCompetencyUseCase],
) -> CompetencyResponse:
    _ = user
    competency = await use_case.execute(competency_id=competency_id, skill_id=skill_id)
    return CompetencyResponse.from_schema(competency=competency)
