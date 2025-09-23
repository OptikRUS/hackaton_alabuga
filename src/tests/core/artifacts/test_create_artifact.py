import pytest

from src.core.artifacts.enums import ArtifactRarityEnum
from src.core.artifacts.exceptions import ArtifactTitleAlreadyExistError
from src.core.artifacts.use_cases import CreateArtifactUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestCreateArtifactUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = CreateArtifactUseCase(storage=self.storage)

    async def test_create_artifact(self) -> None:
        artifact = await self.use_case.execute(
            artifact=self.factory.artifact(
                artifact_id=1,
                title="TEST",
                description="TEST",
                rarity=ArtifactRarityEnum.COMMON,
                image_url="https://example.com/image.jpg",
            )
        )

        assert artifact == self.factory.artifact(
            artifact_id=1,
            title="TEST",
            description="TEST",
            rarity=ArtifactRarityEnum.COMMON,
            image_url="https://example.com/image.jpg",
        )

    async def test_create_artifact_title_already_exists(self) -> None:
        await self.storage.insert_artifact(
            artifact=self.factory.artifact(
                artifact_id=0,
                title="TEST",
                description="Test description",
                rarity=ArtifactRarityEnum.COMMON,
                image_url="https://example.com/image.jpg",
            )
        )

        with pytest.raises(ArtifactTitleAlreadyExistError):
            await self.use_case.execute(artifact=self.factory.artifact(artifact_id=0, title="TEST"))
