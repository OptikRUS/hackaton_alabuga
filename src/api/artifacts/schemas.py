from pydantic import Field

from src.api.boundary import BoundaryModel
from src.core.artifacts.enums import ArtifactRarityEnum
from src.core.artifacts.schemas import Artifact, Artifacts


class ArtifactCreateRequest(BoundaryModel):
    title: str = Field(default=..., description="Название артефакта")
    description: str = Field(default=..., description="Описание артефакта")
    rarity: ArtifactRarityEnum = Field(default=..., description="Редкость артефакта")
    image_url: str = Field(default=..., description="URL изображения артефакта")

    def to_schema(self) -> Artifact:
        return Artifact(
            id=0,
            title=self.title,
            description=self.description,
            rarity=self.rarity,
            image_url=self.image_url,
        )


class ArtifactUpdateRequest(BoundaryModel):
    title: str = Field(default=..., description="Название артефакта")
    description: str = Field(default=..., description="Описание артефакта")
    rarity: ArtifactRarityEnum = Field(default=..., description="Редкость артефакта")
    image_url: str = Field(default=..., description="URL изображения артефакта")

    def to_schema(self, artifact_id: int) -> Artifact:
        return Artifact(
            id=artifact_id,
            title=self.title,
            description=self.description,
            rarity=self.rarity,
            image_url=self.image_url,
        )


class ArtifactResponse(BoundaryModel):
    id: int = Field(default=..., description="Идентификатор артефакта")
    title: str = Field(default=..., description="Название артефакта")
    description: str = Field(default=..., description="Описание артефакта")
    rarity: ArtifactRarityEnum = Field(default=..., description="Редкость артефакта")
    image_url: str = Field(default=..., description="URL изображения артефакта")

    @classmethod
    def from_schema(cls, artifact: Artifact) -> "ArtifactResponse":
        return cls(
            id=artifact.id,
            title=artifact.title,
            description=artifact.description,
            rarity=artifact.rarity,
            image_url=artifact.image_url,
        )


class ArtifactsResponse(BoundaryModel):
    values: list[ArtifactResponse]

    @classmethod
    def from_schema(cls, artifacts: Artifacts) -> "ArtifactsResponse":
        return cls(
            values=[
                ArtifactResponse.from_schema(artifact=artifact) for artifact in artifacts.values
            ]
        )
