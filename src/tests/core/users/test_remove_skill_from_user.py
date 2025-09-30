import pytest

from src.core.competencies.exceptions import CompetencyNotFoundError
from src.core.skills.exceptions import SkillNotFoundError
from src.core.users.exceptions import UserNotFoundError
from src.core.users.use_cases import RemoveSkillFromUserUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestRemoveSkillFromUserUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = RemoveSkillFromUserUseCase(storage=self.storage)

    async def test_remove_skill_from_user_success(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        competency = self.factory.competency(competency_id=1, name="Python", max_level=5)
        skill = self.factory.skill(skill_id=1, name="Django")

        await self.storage.insert_user(user)
        await self.storage.insert_competency(competency)
        await self.storage.insert_skill(skill)
        await self.storage.add_skill_to_user("test_user", 1, 1, level=3)

        # Act
        await self.use_case.execute("test_user", 1, 1)

        # Assert
        assert "test_user" not in self.storage.users_skills_relations

    async def test_remove_skill_from_user_skill_not_found(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        competency = self.factory.competency(competency_id=1, name="Python", max_level=5)

        await self.storage.insert_user(user)
        await self.storage.insert_competency(competency)

        # Act & Assert
        with pytest.raises(SkillNotFoundError):
            await self.use_case.execute("test_user", 999, 1)

    async def test_remove_skill_from_user_competency_not_found(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        skill = self.factory.skill(skill_id=1, name="Django")

        await self.storage.insert_user(user)
        await self.storage.insert_skill(skill)

        # Act & Assert
        with pytest.raises(CompetencyNotFoundError):
            await self.use_case.execute("test_user", 1, 999)

    async def test_remove_skill_from_nonexistent_user(self) -> None:
        # Arrange
        competency = self.factory.competency(competency_id=1, name="Python", max_level=5)
        skill = self.factory.skill(skill_id=1, name="Django")

        await self.storage.insert_competency(competency)
        await self.storage.insert_skill(skill)

        # Act & Assert
        with pytest.raises(UserNotFoundError):
            await self.use_case.execute("nonexistent_user", 1, 1)
