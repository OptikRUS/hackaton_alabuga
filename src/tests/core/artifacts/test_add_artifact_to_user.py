import pytest

from src.core.artifacts.enums import ArtifactRarityEnum
from src.core.artifacts.exceptions import ArtifactNotFoundError
from src.core.artifacts.use_cases import AddArtifactToUserUseCase
from src.core.users.exceptions import UserNotFoundError
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestAddArtifactToUserUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = AddArtifactToUserUseCase(storage=self.storage, user_storage=self.storage)
        await self.storage.insert_user(
            user=self.factory.user(
                login="testuser",
                password="password",
            )
        )
        await self.storage.insert_artifact(
            artifact=self.factory.artifact(
                artifact_id=1,
                title="TEST",
                description="TEST",
                rarity=ArtifactRarityEnum.COMMON,
                image_url="https://example.com/image.jpg",
            )
        )

    async def test_execute_success(self):
        result = await self.use_case.execute(user_login="testuser", artifact_id=1)

        assert result == self.factory.user(
            login="testuser",
            password="password",
        )

    async def test_execute_user_not_found(self):
        with pytest.raises(UserNotFoundError):
            await self.use_case.execute(user_login="nonexistent", artifact_id=1)

    async def test_execute_artifact_not_found(self):
        with pytest.raises(ArtifactNotFoundError):
            await self.use_case.execute(user_login="testuser", artifact_id=999)
