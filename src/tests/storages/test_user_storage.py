import pytest

from src.core.artifacts.enums import ArtifactRarityEnum
from src.core.users.exceptions import UserAlreadyExistError
from src.storages.database_storage import DatabaseStorage
from src.tests.fixtures import FactoryFixture, StorageFixture


class TestUserStorage(FactoryFixture, StorageFixture):
    @pytest.fixture(autouse=True)
    async def setup(self, storage: DatabaseStorage) -> None:
        self.storage = storage

    async def test_get_user(self) -> None:
        await self.storage_helper.insert_user(
            user=self.factory.user(
                login="TEST",
                password="TEST",
                first_name="TEST",
                last_name="TEST",
            )
        )

        user = await self.storage.get_user_by_login(login="TEST")

        assert user is not None
        assert user == self.factory.user(
            login="TEST",
            first_name="TEST",
            last_name="TEST",
            password="TEST",
            artifacts=[],
        )

    async def test_get_user_with_artifacts(self) -> None:
        await self.storage_helper.insert_user(
            user=self.factory.user(
                login="TEST",
                password="TEST",
                first_name="TEST",
                last_name="TEST",
            )
        )
        artifact_1 = await self.storage_helper.insert_artifact(
            artifact=self.factory.artifact(
                title="TEST",
                description="TEST",
                rarity=ArtifactRarityEnum.COMMON,
                image_url="TEST",
            )
        )
        artifact_2 = await self.storage_helper.insert_artifact(
            artifact=self.factory.artifact(
                title="TEST2",
                description="TEST2",
                rarity=ArtifactRarityEnum.RARE,
                image_url="TEST2",
            )
        )
        assert artifact_1 is not None
        assert artifact_2 is not None

        await self.storage.add_artifact_to_user(user_login="TEST", artifact_id=artifact_1.id)
        await self.storage.add_artifact_to_user(user_login="TEST", artifact_id=artifact_2.id)

        user = await self.storage.get_user_by_login(login="TEST")

        assert user is not None
        assert user == self.factory.user(
            login="TEST",
            first_name="TEST",
            last_name="TEST",
            password="TEST",
            artifacts=[artifact_1.to_schema(), artifact_2.to_schema()],
        )

    async def test_insert_user(self) -> None:
        await self.storage.insert_user(
            user=self.factory.user(
                login="TEST",
                password="TEST",
                first_name="TEST",
                last_name="TEST",
            )
        )

        user = await self.storage_helper.get_user_by_login(login="TEST")
        assert user is not None

    async def test_insert_already_registered(self) -> None:
        await self.storage_helper.insert_user(
            user=self.factory.user(
                login="TEST",
                password="TEST",
                first_name="TEST",
                last_name="TEST",
            )
        )

        with pytest.raises(UserAlreadyExistError):
            await self.storage.insert_user(
                user=self.factory.user(
                    login="TEST",
                    password="TEST",
                    first_name="TEST",
                    last_name="TEST",
                )
            )
