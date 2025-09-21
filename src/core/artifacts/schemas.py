from dataclasses import dataclass

from src.core.artifacts.enums import ArtifactRarityEnum


@dataclass
class Artifact:
    id: int
    title: str
    description: str
    rarity: ArtifactRarityEnum
    image_url: str


@dataclass
class Artifacts:
    values: list[Artifact]
