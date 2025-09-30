import pytest

from src.core.competencies.exceptions import CompetencyNotFoundError
from src.core.users.exceptions import UserNotFoundError
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestUserCompetencies(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()

    async def test_add_competency_to_user_success(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        competency = self.factory.competency(competency_id=1, name="Python", max_level=5)

        await self.storage.insert_user(user)
        await self.storage.insert_competency(competency)

        # Act
        await self.storage.add_competency_to_user("test_user", 1, level=3)

        # Assert
        assert "test_user" in self.storage.users_competencies_relations
        assert 1 in self.storage.users_competencies_relations["test_user"]
        assert self.storage.users_competencies_relations["test_user"][1] == 3

    async def test_add_competency_to_user_default_level(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        competency = self.factory.competency(competency_id=1, name="Python", max_level=5)

        await self.storage.insert_user(user)
        await self.storage.insert_competency(competency)

        # Act
        await self.storage.add_competency_to_user("test_user", 1)

        # Assert
        assert self.storage.users_competencies_relations["test_user"][1] == 0

    async def test_add_competency_to_user_not_found(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        await self.storage.insert_user(user)

        # Act & Assert
        with pytest.raises(CompetencyNotFoundError):
            await self.storage.add_competency_to_user("test_user", 999)

    async def test_add_competency_to_nonexistent_user(self) -> None:
        # Arrange
        competency = self.factory.competency(competency_id=1, name="Python", max_level=5)
        await self.storage.insert_competency(competency)

        # Act & Assert
        with pytest.raises(UserNotFoundError):
            await self.storage.add_competency_to_user("nonexistent_user", 1)

    async def test_remove_competency_from_user_success(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        competency = self.factory.competency(competency_id=1, name="Python", max_level=5)

        await self.storage.insert_user(user)
        await self.storage.insert_competency(competency)
        await self.storage.add_competency_to_user("test_user", 1, level=3)

        # Act
        await self.storage.remove_competency_from_user("test_user", 1)

        # Assert
        assert "test_user" not in self.storage.users_competencies_relations

    async def test_remove_competency_from_user_not_found(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        await self.storage.insert_user(user)

        # Act & Assert
        with pytest.raises(CompetencyNotFoundError):
            await self.storage.remove_competency_from_user("test_user", 999)

    async def test_remove_competency_from_nonexistent_user(self) -> None:
        # Arrange
        competency = self.factory.competency(competency_id=1, name="Python", max_level=5)
        await self.storage.insert_competency(competency)

        # Act & Assert
        with pytest.raises(UserNotFoundError):
            await self.storage.remove_competency_from_user("nonexistent_user", 1)

    async def test_update_user_competency_level_success(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        competency = self.factory.competency(competency_id=1, name="Python", max_level=5)

        await self.storage.insert_user(user)
        await self.storage.insert_competency(competency)
        await self.storage.add_competency_to_user("test_user", 1, level=2)

        # Act
        await self.storage.update_user_competency_level("test_user", 1, level=4)

        # Assert
        assert self.storage.users_competencies_relations["test_user"][1] == 4

    async def test_update_user_competency_level_not_found(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        await self.storage.insert_user(user)

        # Act & Assert
        with pytest.raises(CompetencyNotFoundError):
            await self.storage.update_user_competency_level("test_user", 999, level=3)

    async def test_update_user_competency_level_user_not_found(self) -> None:
        # Arrange
        competency = self.factory.competency(competency_id=1, name="Python", max_level=5)
        await self.storage.insert_competency(competency)

        # Act & Assert
        with pytest.raises(UserNotFoundError):
            await self.storage.update_user_competency_level("nonexistent_user", 1, level=3)

    async def test_update_user_competency_level_competency_not_assigned(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        competency = self.factory.competency(competency_id=1, name="Python", max_level=5)

        await self.storage.insert_user(user)
        await self.storage.insert_competency(competency)

        # Act & Assert
        with pytest.raises(UserNotFoundError):
            await self.storage.update_user_competency_level("test_user", 1, level=3)

    async def test_multiple_competencies_per_user(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        competency1 = self.factory.competency(competency_id=1, name="Python", max_level=5)
        competency2 = self.factory.competency(competency_id=2, name="JavaScript", max_level=3)

        await self.storage.insert_user(user)
        await self.storage.insert_competency(competency1)
        await self.storage.insert_competency(competency2)

        # Act
        await self.storage.add_competency_to_user("test_user", 1, level=3)
        await self.storage.add_competency_to_user("test_user", 2, level=2)

        # Assert
        assert len(self.storage.users_competencies_relations["test_user"]) == 2
        assert self.storage.users_competencies_relations["test_user"][1] == 3
        assert self.storage.users_competencies_relations["test_user"][2] == 2

    async def test_remove_one_competency_keeps_others(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        competency1 = self.factory.competency(competency_id=1, name="Python", max_level=5)
        competency2 = self.factory.competency(competency_id=2, name="JavaScript", max_level=3)

        await self.storage.insert_user(user)
        await self.storage.insert_competency(competency1)
        await self.storage.insert_competency(competency2)
        await self.storage.add_competency_to_user("test_user", 1, level=3)
        await self.storage.add_competency_to_user("test_user", 2, level=2)

        # Act
        await self.storage.remove_competency_from_user("test_user", 1)

        # Assert
        assert len(self.storage.users_competencies_relations["test_user"]) == 1
        assert 1 not in self.storage.users_competencies_relations["test_user"]
        assert self.storage.users_competencies_relations["test_user"][2] == 2
