import pytest

from src.core.artifacts.enums import ArtifactRarityEnum
from src.core.artifacts.exceptions import ArtifactNotFoundError, ArtifactTitleAlreadyExistError
from src.core.artifacts.use_cases import UpdateArtifactUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestUpdateArtifactUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = UpdateArtifactUseCase(storage=self.storage)

    async def test_update_artifact(self) -> None:
        await self.storage.insert_artifact(
            artifact=self.factory.artifact(
                artifact_id=1,
                title="TEST_ARTIFACT",
                description="Test description",
                rarity=ArtifactRarityEnum.COMMON,
                image_url="https://example.com/image.jpg",
            )
        )

        artifact = await self.use_case.execute(
            artifact=self.factory.artifact(
                artifact_id=1,
                title="UPDATED_ARTIFACT",
                description="Updated description",
                rarity=ArtifactRarityEnum.RARE,
                image_url="https://example.com/updated.jpg",
            )
        )

        assert artifact == self.factory.artifact(
            artifact_id=1,
            title="UPDATED_ARTIFACT",
            description="Updated description",
            rarity=ArtifactRarityEnum.RARE,
            image_url="https://example.com/updated.jpg",
        )

    async def test_update_artifact_title_already_exists(self) -> None:
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

        with pytest.raises(ArtifactTitleAlreadyExistError):
            await self.use_case.execute(
                artifact=self.factory.artifact(
                    artifact_id=2,
                    title="TEST_ARTIFACT_1",
                    description="Updated description",
                    rarity=ArtifactRarityEnum.EPIC,
                    image_url="https://example.com/updated.jpg",
                )
            )

    async def test_update_artifact_not_found(self) -> None:
        with pytest.raises(ArtifactNotFoundError):
            await self.use_case.execute(
                artifact=self.factory.artifact(
                    artifact_id=999,
                    title="NON_EXISTENT",
                    description="Description",
                    rarity=ArtifactRarityEnum.COMMON,
                    image_url="https://example.com/image.jpg",
                )
            )
