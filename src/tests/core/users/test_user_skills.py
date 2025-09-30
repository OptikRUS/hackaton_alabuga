import pytest

from src.core.competencies.exceptions import CompetencyNotFoundError
from src.core.skills.exceptions import SkillNotFoundError
from src.core.users.exceptions import UserNotFoundError
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestUserSkills(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()

    async def test_add_skill_to_user_success(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        competency = self.factory.competency(competency_id=1, name="Python", max_level=5)
        skill = self.factory.skill(skill_id=1, name="Django")

        await self.storage.insert_user(user)
        await self.storage.insert_competency(competency)
        await self.storage.insert_skill(skill)

        # Act
        await self.storage.add_skill_to_user("test_user", 1, 1, level=3)

        # Assert
        assert "test_user" in self.storage.users_skills_relations
        assert 1 in self.storage.users_skills_relations["test_user"]
        assert 1 in self.storage.users_skills_relations["test_user"][1]
        assert self.storage.users_skills_relations["test_user"][1][1] == 3

    async def test_add_skill_to_user_default_level(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        competency = self.factory.competency(competency_id=1, name="Python", max_level=5)
        skill = self.factory.skill(skill_id=1, name="Django")

        await self.storage.insert_user(user)
        await self.storage.insert_competency(competency)
        await self.storage.insert_skill(skill)

        # Act
        await self.storage.add_skill_to_user("test_user", 1, 1)

        # Assert
        assert self.storage.users_skills_relations["test_user"][1][1] == 0

    async def test_add_skill_to_user_skill_not_found(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        competency = self.factory.competency(competency_id=1, name="Python", max_level=5)

        await self.storage.insert_user(user)
        await self.storage.insert_competency(competency)

        # Act & Assert
        with pytest.raises(SkillNotFoundError):
            await self.storage.add_skill_to_user("test_user", 999, 1)

    async def test_add_skill_to_user_competency_not_found(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        skill = self.factory.skill(skill_id=1, name="Django")

        await self.storage.insert_user(user)
        await self.storage.insert_skill(skill)

        # Act & Assert
        with pytest.raises(CompetencyNotFoundError):
            await self.storage.add_skill_to_user("test_user", 1, 999)

    async def test_add_skill_to_nonexistent_user(self) -> None:
        # Arrange
        competency = self.factory.competency(competency_id=1, name="Python", max_level=5)
        skill = self.factory.skill(skill_id=1, name="Django")

        await self.storage.insert_competency(competency)
        await self.storage.insert_skill(skill)

        # Act & Assert
        with pytest.raises(UserNotFoundError):
            await self.storage.add_skill_to_user("nonexistent_user", 1, 1)

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
        await self.storage.remove_skill_from_user("test_user", 1, 1)

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
            await self.storage.remove_skill_from_user("test_user", 999, 1)

    async def test_remove_skill_from_user_competency_not_found(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        skill = self.factory.skill(skill_id=1, name="Django")

        await self.storage.insert_user(user)
        await self.storage.insert_skill(skill)

        # Act & Assert
        with pytest.raises(CompetencyNotFoundError):
            await self.storage.remove_skill_from_user("test_user", 1, 999)

    async def test_remove_skill_from_nonexistent_user(self) -> None:
        # Arrange
        competency = self.factory.competency(competency_id=1, name="Python", max_level=5)
        skill = self.factory.skill(skill_id=1, name="Django")

        await self.storage.insert_competency(competency)
        await self.storage.insert_skill(skill)

        # Act & Assert
        with pytest.raises(UserNotFoundError):
            await self.storage.remove_skill_from_user("nonexistent_user", 1, 1)

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
        await self.storage.update_user_skill_level("test_user", 1, 1, level=4)

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
            await self.storage.update_user_skill_level("test_user", 999, 1, level=3)

    async def test_update_user_skill_level_competency_not_found(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        skill = self.factory.skill(skill_id=1, name="Django")

        await self.storage.insert_user(user)
        await self.storage.insert_skill(skill)

        # Act & Assert
        with pytest.raises(CompetencyNotFoundError):
            await self.storage.update_user_skill_level("test_user", 1, 999, level=3)

    async def test_update_user_skill_level_user_not_found(self) -> None:
        # Arrange
        competency = self.factory.competency(competency_id=1, name="Python", max_level=5)
        skill = self.factory.skill(skill_id=1, name="Django")

        await self.storage.insert_competency(competency)
        await self.storage.insert_skill(skill)

        # Act & Assert
        with pytest.raises(UserNotFoundError):
            await self.storage.update_user_skill_level("nonexistent_user", 1, 1, level=3)

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
            await self.storage.update_user_skill_level("test_user", 1, 1, level=3)

    async def test_multiple_skills_per_user(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        competency1 = self.factory.competency(competency_id=1, name="Python", max_level=5)
        competency2 = self.factory.competency(competency_id=2, name="JavaScript", max_level=3)
        skill1 = self.factory.skill(skill_id=1, name="Django")
        skill2 = self.factory.skill(skill_id=2, name="React")

        await self.storage.insert_user(user)
        await self.storage.insert_competency(competency1)
        await self.storage.insert_competency(competency2)
        await self.storage.insert_skill(skill1)
        await self.storage.insert_skill(skill2)

        # Act
        await self.storage.add_skill_to_user("test_user", 1, 1, level=3)
        await self.storage.add_skill_to_user("test_user", 2, 2, level=2)

        # Assert
        assert len(self.storage.users_skills_relations["test_user"]) == 2
        assert self.storage.users_skills_relations["test_user"][1][1] == 3
        assert self.storage.users_skills_relations["test_user"][2][2] == 2

    async def test_skill_with_multiple_competencies(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        competency1 = self.factory.competency(competency_id=1, name="Python", max_level=5)
        competency2 = self.factory.competency(competency_id=2, name="Web Development", max_level=3)
        skill = self.factory.skill(skill_id=1, name="Django")

        await self.storage.insert_user(user)
        await self.storage.insert_competency(competency1)
        await self.storage.insert_competency(competency2)
        await self.storage.insert_skill(skill)

        # Act
        await self.storage.add_skill_to_user("test_user", 1, 1, level=3)
        await self.storage.add_skill_to_user("test_user", 1, 2, level=2)

        # Assert
        assert len(self.storage.users_skills_relations["test_user"][1]) == 2
        assert self.storage.users_skills_relations["test_user"][1][1] == 3
        assert self.storage.users_skills_relations["test_user"][1][2] == 2

    async def test_remove_one_competency_from_skill_keeps_others(self) -> None:
        # Arrange
        user = self.factory.user(login="test_user")
        competency1 = self.factory.competency(competency_id=1, name="Python", max_level=5)
        competency2 = self.factory.competency(competency_id=2, name="Web Development", max_level=3)
        skill = self.factory.skill(skill_id=1, name="Django")

        await self.storage.insert_user(user)
        await self.storage.insert_competency(competency1)
        await self.storage.insert_competency(competency2)
        await self.storage.insert_skill(skill)
        await self.storage.add_skill_to_user("test_user", 1, 1, level=3)
        await self.storage.add_skill_to_user("test_user", 1, 2, level=2)

        # Act
        await self.storage.remove_skill_from_user("test_user", 1, 1)

        # Assert
        assert len(self.storage.users_skills_relations["test_user"][1]) == 1
        assert 1 not in self.storage.users_skills_relations["test_user"][1]
        assert self.storage.users_skills_relations["test_user"][1][2] == 2
