import pytest

from src.core.competencies.exceptions import CompetencyNotFoundError
from src.core.skills.exceptions import SkillNotFoundError
from src.core.users.exceptions import UserNotFoundError
from src.core.users.use_cases import UpdateUserSkillLevelUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestUpdateUserSkillLevelUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = UpdateUserSkillLevelUseCase(storage=self.storage)

    async def test_update_user_skill_level_success(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        competency = self.factory.competency(competency_id=1, name="Python", max_level=5)
        skill = self.factory.skill(skill_id=1, name="Django")

        await self.storage.insert_user(user)
        await self.storage.insert_competency(competency)
        await self.storage.insert_skill(skill)
        await self.storage.add_skill_to_user("test_user", 1, 1, level=2)

        # Act
        await self.use_case.execute("test_user", 1, 1, level=4)

        # Assert
        assert self.storage.users_skills_relations["test_user"][1][1] == 4

    async def test_update_user_skill_level_skill_not_found(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        competency = self.factory.competency(competency_id=1, name="Python", max_level=5)

        await self.storage.insert_user(user)
        await self.storage.insert_competency(competency)

        # Act & Assert
        with pytest.raises(SkillNotFoundError):
            await self.use_case.execute("test_user", 999, 1, level=3)

    async def test_update_user_skill_level_competency_not_found(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        skill = self.factory.skill(skill_id=1, name="Django")

        await self.storage.insert_user(user)
        await self.storage.insert_skill(skill)

        # Act & Assert
        with pytest.raises(CompetencyNotFoundError):
            await self.use_case.execute("test_user", 1, 999, level=3)

    async def test_update_user_skill_level_user_not_found(self) -> None:
        # Arrange
        competency = self.factory.competency(competency_id=1, name="Python", max_level=5)
        skill = self.factory.skill(skill_id=1, name="Django")

        await self.storage.insert_competency(competency)
        await self.storage.insert_skill(skill)

        # Act & Assert
        with pytest.raises(UserNotFoundError):
            await self.use_case.execute("nonexistent_user", 1, 1, level=3)

    async def test_update_user_skill_level_skill_not_assigned(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        competency = self.factory.competency(competency_id=1, name="Python", max_level=5)
        skill = self.factory.skill(skill_id=1, name="Django")

        await self.storage.insert_user(user)
        await self.storage.insert_competency(competency)
        await self.storage.insert_skill(skill)

        # Act & Assert
        with pytest.raises(UserNotFoundError):
            await self.use_case.execute("test_user", 1, 1, level=3)

