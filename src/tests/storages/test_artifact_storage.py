import pytest

from src.core.artifacts.enums import ArtifactRarityEnum
from src.core.artifacts.exceptions import ArtifactNotFoundError, ArtifactTitleAlreadyExistError
from src.storages.database_storage import DatabaseStorage
from src.tests.fixtures import FactoryFixture, StorageFixture


class TestArtifactStorage(FactoryFixture, StorageFixture):
    @pytest.fixture(autouse=True)
    async def setup(self, storage: DatabaseStorage) -> None:
        self.storage = storage
        inserted_artifact = await self.storage_helper.insert_artifact(
            artifact=self.factory.artifact(
                title="TEST",
                description="TEST",
                rarity=ArtifactRarityEnum.RARE,
                image_url="https://example.com/test.jpg",
            )
        )
        assert inserted_artifact is not None
        self.created_artifact = inserted_artifact.to_schema()

    async def test_get_artifact_by_id(self) -> None:
        artifact = await self.storage.get_artifact_by_id(artifact_id=self.created_artifact.id)

        assert artifact == self.factory.artifact(
            artifact_id=self.created_artifact.id,
            title="TEST",
            description="TEST",
            rarity=ArtifactRarityEnum.RARE,
            image_url="https://example.com/test.jpg",
        )

    async def test_get_artifact_by_title(self) -> None:
        artifact = await self.storage.get_artifact_by_title(title="TEST")

        assert artifact == self.factory.artifact(
            artifact_id=self.created_artifact.id,
            title="TEST",
            description="TEST",
            rarity=ArtifactRarityEnum.RARE,
            image_url="https://example.com/test.jpg",
        )

    async def test_insert_artifact(self) -> None:
        await self.storage.insert_artifact(
            artifact=self.factory.artifact(
                title="TEST1",
                description="TEST",
                rarity=ArtifactRarityEnum.COMMON,
                image_url="TEST",
            )
        )

        artifact = await self.storage_helper.get_artifact_by_title(title="TEST1")

        assert artifact is not None
        assert artifact.title == "TEST1"
        assert artifact.description == "TEST"
        assert artifact.rarity == ArtifactRarityEnum.COMMON
        assert artifact.image_url == "TEST"

    async def test_insert_artifact_with_duplicate_title(self) -> None:
        with pytest.raises(ArtifactTitleAlreadyExistError):
            await self.storage.insert_artifact(
                artifact=self.factory.artifact(
                    title="TEST",
                    description="TEST",
                    rarity=ArtifactRarityEnum.COMMON,
                    image_url="TEST",
                )
            )

    async def test_list_artifacts(self) -> None:
        await self.storage_helper.insert_artifact(
            artifact=self.factory.artifact(
                title="TEST1",
                description="TEST1",
                rarity=ArtifactRarityEnum.COMMON,
                image_url="TEST1",
            )
        )
        await self.storage_helper.insert_artifact(
            artifact=self.factory.artifact(
                title="TEST2",
                description="TEST2",
                rarity=ArtifactRarityEnum.RARE,
                image_url="TEST2",
            )
        )

        artifacts = await self.storage.list_artifacts()

        assert len(artifacts.values) == 3
        assert artifacts.values[0] == self.created_artifact
        assert artifacts.values[1].title == "TEST1"
        assert artifacts.values[1].description == "TEST1"
        assert artifacts.values[1].rarity == ArtifactRarityEnum.COMMON
        assert artifacts.values[1].image_url == "TEST1"
        assert artifacts.values[2].title == "TEST2"
        assert artifacts.values[2].description == "TEST2"
        assert artifacts.values[2].rarity == ArtifactRarityEnum.RARE
        assert artifacts.values[2].image_url == "TEST2"

    async def test_update_artifact(self) -> None:
        await self.storage.update_artifact(
            artifact=self.factory.artifact(
                artifact_id=self.created_artifact.id,
                title="UPDATED_ARTIFACT",
                description="Updated description",
                rarity=ArtifactRarityEnum.LEGENDARY,
                image_url="https://example.com/updated.jpg",
            )
        )

        artifact = await self.storage.get_artifact_by_id(artifact_id=self.created_artifact.id)

        assert artifact == self.factory.artifact(
            artifact_id=self.created_artifact.id,
            title="UPDATED_ARTIFACT",
            description="Updated description",
            rarity=ArtifactRarityEnum.LEGENDARY,
            image_url="https://example.com/updated.jpg",
        )

    async def test_update_artifact_with_duplicate_title(self) -> None:
        artifact = await self.storage_helper.insert_artifact(
            artifact=self.factory.artifact(
                title="TEST2",
                description="TEST2",
                rarity=ArtifactRarityEnum.COMMON,
                image_url="https://example.com/test2.jpg",
            )
        )
        assert artifact is not None

        with pytest.raises(ArtifactTitleAlreadyExistError):
            await self.storage.update_artifact(
                artifact=self.factory.artifact(
                    artifact_id=artifact.id,
                    title="TEST",
                    description="Updated description",
                    rarity=ArtifactRarityEnum.COMMON,
                    image_url="https://example.com/updated.jpg",
                )
            )

    async def test_delete_artifact(self) -> None:
        await self.storage.delete_artifact(artifact_id=self.created_artifact.id)

        with pytest.raises(ArtifactNotFoundError):
            await self.storage.get_artifact_by_id(artifact_id=self.created_artifact.id)

    async def test_get_artifact_not_found_by_id(self) -> None:
        with pytest.raises(ArtifactNotFoundError):
            await self.storage.get_artifact_by_id(artifact_id=999)

    async def test_get_artifact_not_found_by_title(self) -> None:
        with pytest.raises(ArtifactNotFoundError):
            await self.storage.get_artifact_by_title(title="NONEXISTENT_ARTIFACT")

    async def test_update_artifact_not_found(self) -> None:
        with pytest.raises(ArtifactNotFoundError):
            await self.storage.update_artifact(
                artifact=self.factory.artifact(
                    artifact_id=999,
                    title="NONEXISTENT",
                    description="Description",
                    rarity=ArtifactRarityEnum.COMMON,
                    image_url="https://example.com/nonexistent.jpg",
                )
            )

    async def test_delete_artifact_not_found(self) -> None:
        with pytest.raises(ArtifactNotFoundError):
            await self.storage.delete_artifact(artifact_id=999)
