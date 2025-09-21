from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status

from src.api.artifacts.schemas import (
    ArtifactCreateRequest,
    ArtifactResponse,
    ArtifactsResponse,
    ArtifactUpdateRequest,
)
from src.core.artifacts.use_cases import (
    CreateArtifactUseCase,
    DeleteArtifactUseCase,
    GetArtifactDetailUseCase,
    GetArtifactsUseCase,
    UpdateArtifactUseCase,
)

router = APIRouter(tags=["artifacts"], route_class=DishkaRoute)


@router.post(path="/artifacts", status_code=status.HTTP_201_CREATED)
async def create_artifact(
    body: ArtifactCreateRequest,
    use_case: FromDishka[CreateArtifactUseCase],
) -> ArtifactResponse:
    artifact = await use_case.execute(artifact=body.to_schema())
    return ArtifactResponse.from_schema(artifact=artifact)


@router.get(path="/artifacts", status_code=status.HTTP_200_OK)
async def get_artifacts(
    use_case: FromDishka[GetArtifactsUseCase],
) -> ArtifactsResponse:
    artifacts = await use_case.execute()
    return ArtifactsResponse.from_schema(artifacts=artifacts)


@router.get(path="/artifacts/{artifact_id}", status_code=status.HTTP_200_OK)
async def get_artifact(
    artifact_id: int,
    use_case: FromDishka[GetArtifactDetailUseCase],
) -> ArtifactResponse:
    artifact = await use_case.execute(artifact_id=artifact_id)
    return ArtifactResponse.from_schema(artifact=artifact)


@router.put(path="/artifacts/{artifact_id}", status_code=status.HTTP_200_OK)
async def update_artifact(
    artifact_id: int,
    body: ArtifactUpdateRequest,
    use_case: FromDishka[UpdateArtifactUseCase],
) -> ArtifactResponse:
    artifact = await use_case.execute(artifact=body.to_schema(artifact_id=artifact_id))
    return ArtifactResponse.from_schema(artifact=artifact)


@router.delete(path="/artifacts/{artifact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_artifact(
    artifact_id: int,
    use_case: FromDishka[DeleteArtifactUseCase],
) -> None:
    await use_case.execute(artifact_id=artifact_id)
