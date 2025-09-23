from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status

from src.api.skills.schemas import (
    SkillCreateRequest,
    SkillResponse,
    SkillsResponse,
    SkillUpdateRequest,
)
from src.core.skills.use_cases import (
    CreateSkillUseCase,
    DeleteSkillUseCase,
    GetSkillDetailUseCase,
    GetSkillsUseCase,
    UpdateSkillUseCase,
)

router = APIRouter(tags=["skills"], route_class=DishkaRoute)


@router.post(
    path="/skills",
    status_code=status.HTTP_201_CREATED,
    summary="Создать навык",
    description="Создает новый навык в системе",
)
async def create_skill(
    body: SkillCreateRequest,
    use_case: FromDishka[CreateSkillUseCase],
) -> SkillResponse:
    skill = await use_case.execute(skill=body.to_schema())
    return SkillResponse.from_schema(skill=skill)


@router.get(
    path="/skills",
    status_code=status.HTTP_200_OK,
    summary="Получить список навыков",
    description="Возвращает все доступные навыки",
)
async def get_skills(
    use_case: FromDishka[GetSkillsUseCase],
) -> SkillsResponse:
    skills = await use_case.execute()
    return SkillsResponse.from_schema(skills=skills)


@router.get(
    path="/skills/{skill_id}",
    status_code=status.HTTP_200_OK,
    summary="Получить навык по ID",
    description="Возвращает детальную информацию о навыке",
)
async def get_skill(
    skill_id: int,
    use_case: FromDishka[GetSkillDetailUseCase],
) -> SkillResponse:
    skill = await use_case.execute(skill_id=skill_id)
    return SkillResponse.from_schema(skill=skill)


@router.put(
    path="/skills/{skill_id}",
    status_code=status.HTTP_200_OK,
    summary="Обновить навык",
    description="Обновляет данные указанного навыка",
)
async def update_skill(
    skill_id: int,
    body: SkillUpdateRequest,
    use_case: FromDishka[UpdateSkillUseCase],
) -> SkillResponse:
    skill = await use_case.execute(skill=body.to_schema(skill_id=skill_id))
    return SkillResponse.from_schema(skill=skill)


@router.delete(
    path="/skills/{skill_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить навык",
    description="Удаляет указанный навык",
)
async def delete_skill(
    skill_id: int,
    use_case: FromDishka[DeleteSkillUseCase],
) -> None:
    await use_case.execute(skill_id=skill_id)
