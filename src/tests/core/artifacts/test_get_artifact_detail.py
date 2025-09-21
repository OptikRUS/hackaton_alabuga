import pytest

from src.core.artifacts.enums import ArtifactRarityEnum
from src.core.artifacts.exceptions import ArtifactNotFoundError
from src.core.artifacts.use_cases import GetArtifactDetailUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestGetArtifactDetailUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = GetArtifactDetailUseCase(storage=self.storage)

    async def test_get_artifact(self) -> None:
        await self.storage.insert_artifact(
            artifact=self.factory.artifact(
                artifact_id=1,
                title="TEST_ARTIFACT",
                description="Test description",
                rarity=ArtifactRarityEnum.COMMON,
                image_url="https://example.com/image.jpg",
            )
        )

        artifact = await self.use_case.execute(artifact_id=1)
        assert artifact == self.factory.artifact(
            artifact_id=1,
            title="TEST_ARTIFACT",
            description="Test description",
            rarity=ArtifactRarityEnum.COMMON,
            image_url="https://example.com/image.jpg",
        )

    async def test_get_artifact_not_found(self) -> None:
        with pytest.raises(ArtifactNotFoundError):
            await self.use_case.execute(artifact_id=999)
