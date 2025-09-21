import pytest

from src.core.artifacts.enums import ArtifactRarityEnum
from src.core.artifacts.use_cases import GetArtifactsUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestGetArtifactsUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = GetArtifactsUseCase(storage=self.storage)

    async def test_get_artifacts(self) -> None:
        await self.storage.insert_artifact(
            artifact=self.factory.artifact(
                artifact_id=1,
                title="TEST_ARTIFACT_1",
                description="Test description 1",
                rarity=ArtifactRarityEnum.COMMON,
                image_url="https://example.com/1.jpg",
            )
        )
        await self.storage.insert_artifact(
            artifact=self.factory.artifact(
                artifact_id=2,
                title="TEST_ARTIFACT_2",
                description="Test description 2",
                rarity=ArtifactRarityEnum.RARE,
                image_url="https://example.com/2.jpg",
            )
        )

        artifacts = await self.use_case.execute()

        assert artifacts == self.factory.artifacts(
            values=[
                self.factory.artifact(
                    artifact_id=1,
                    title="TEST_ARTIFACT_1",
                    description="Test description 1",
                    rarity=ArtifactRarityEnum.COMMON,
                    image_url="https://example.com/1.jpg",
                ),
                self.factory.artifact(
                    artifact_id=2,
                    title="TEST_ARTIFACT_2",
                    description="Test description 2",
                    rarity=ArtifactRarityEnum.RARE,
                    image_url="https://example.com/2.jpg",
                ),
            ]
        )

    async def test_get_artifacts_empty_list(self) -> None:
        artifacts = await self.use_case.execute()

        assert artifacts == self.factory.artifacts(values=[])
