from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status

from src.api.artifacts.schemas import (
    ArtifactCreateRequest,
    ArtifactResponse,
    ArtifactsResponse,
    ArtifactUpdateRequest,
)
from src.api.auth.schemas import JwtHRUser, JwtUser
from src.api.openapi import openapi_extra
from src.core.artifacts.use_cases import (
    CreateArtifactUseCase,
    DeleteArtifactUseCase,
    GetArtifactDetailUseCase,
    GetArtifactsUseCase,
    UpdateArtifactUseCase,
)

router = APIRouter(tags=["artifacts"], route_class=DishkaRoute)


@router.post(
    path="/artifacts",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_201_CREATED,
    summary="Создать артефакт",
    description="Создает новый артефакт в системе",
)
async def create_artifact(
    body: ArtifactCreateRequest,
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[CreateArtifactUseCase],
) -> ArtifactResponse:
    _ = user
    artifact = await use_case.execute(artifact=body.to_schema())
    return ArtifactResponse.from_schema(artifact=artifact)


@router.get(
    path="/artifacts",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Получить список артефактов",
    description="Возвращает все доступные артефакты",
)
async def get_artifacts(
    user: FromDishka[JwtUser],
    use_case: FromDishka[GetArtifactsUseCase],
) -> ArtifactsResponse:
    _ = user
    artifacts = await use_case.execute()
    return ArtifactsResponse.from_schema(artifacts=artifacts)


@router.get(
    path="/artifacts/{artifact_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Получить артефакт по ID",
    description="Возвращает детальную информацию об артефакте",
)
async def get_artifact(
    artifact_id: int,
    user: FromDishka[JwtUser],
    use_case: FromDishka[GetArtifactDetailUseCase],
) -> ArtifactResponse:
    _ = user
    artifact = await use_case.execute(artifact_id=artifact_id)
    return ArtifactResponse.from_schema(artifact=artifact)


@router.put(
    path="/artifacts/{artifact_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_200_OK,
    summary="Обновить артефакт",
    description="Обновляет данные указанного артефакта",
)
async def update_artifact(
    artifact_id: int,
    user: FromDishka[JwtHRUser],
    body: ArtifactUpdateRequest,
    use_case: FromDishka[UpdateArtifactUseCase],
) -> ArtifactResponse:
    _ = user
    artifact = await use_case.execute(artifact=body.to_schema(artifact_id=artifact_id))
    return ArtifactResponse.from_schema(artifact=artifact)


@router.delete(
    path="/artifacts/{artifact_id}",
    openapi_extra=openapi_extra,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить артефакт",
    description="Удаляет указанный артефакт",
)
async def delete_artifact(
    artifact_id: int,
    user: FromDishka[JwtHRUser],
    use_case: FromDishka[DeleteArtifactUseCase],
) -> None:
    _ = user
    await use_case.execute(artifact_id=artifact_id)
