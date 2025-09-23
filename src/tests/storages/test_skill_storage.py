import pytest

from src.core.skills.exceptions import SkillNameAlreadyExistError, SkillNotFoundError
from src.storages.database_storage import DatabaseStorage
from src.tests.fixtures import FactoryFixture, StorageFixture


class TestSkillStorage(FactoryFixture, StorageFixture):
    @pytest.fixture(autouse=True)
    async def setup(self, storage: DatabaseStorage) -> None:
        self.storage = storage
        inserted = await self.storage_helper.insert_artifact(
            artifact=self.factory.artifact(title="ART", description="ART", image_url="IMG")
        )
        assert inserted is not None
        await self.storage.insert_skill(self.factory.skill(name="Python", max_level=100))
        self.created = await self.storage.get_skill_by_name(name="Python")

    async def test_get_skill_by_id(self) -> None:
        skill = await self.storage.get_skill_by_id(skill_id=self.created.id)

        assert skill == self.factory.skill(skill_id=self.created.id, name="Python", max_level=100)

    async def test_get_skill_by_name(self) -> None:
        skill = await self.storage.get_skill_by_name(name="Python")

        assert skill == self.factory.skill(skill_id=self.created.id, name="Python", max_level=100)

    async def test_insert_skill(self) -> None:
        await self.storage.insert_skill(self.factory.skill(name="SQL", max_level=50))

        skill = await self.storage.get_skill_by_name(name="SQL")
        assert skill.name == "SQL"
        assert skill.max_level == 50

    async def test_insert_skill_with_duplicate_name(self) -> None:
        with pytest.raises(SkillNameAlreadyExistError):
            await self.storage.insert_skill(self.factory.skill(name="Python", max_level=120))

    async def test_list_skills(self) -> None:
        await self.storage.insert_skill(self.factory.skill(name="SQL", max_level=50))

        skills = await self.storage.list_skills()

        assert len(skills.values) >= 2

    async def test_update_skill(self) -> None:
        await self.storage.update_skill(
            self.factory.skill(skill_id=self.created.id, name="Python Advanced", max_level=150)
        )

        updated = await self.storage.get_skill_by_id(skill_id=self.created.id)

        assert updated.name == "Python Advanced"
        assert updated.max_level == 150

    async def test_update_skill_with_duplicate_name(self) -> None:
        await self.storage.insert_skill(self.factory.skill(name="SQL", max_level=50))
        skill = await self.storage.get_skill_by_name(name="SQL")
        with pytest.raises(SkillNameAlreadyExistError):
            await self.storage.update_skill(
                self.factory.skill(skill_id=skill.id, name="Python", max_level=60)
            )

    async def test_delete_skill(self) -> None:
        await self.storage.delete_skill(skill_id=self.created.id)
        with pytest.raises(SkillNotFoundError):
            await self.storage.get_skill_by_id(skill_id=self.created.id)

    async def test_get_skill_not_found_by_id(self) -> None:
        with pytest.raises(SkillNotFoundError):
            await self.storage.get_skill_by_id(skill_id=999)

    async def test_get_skill_not_found_by_name(self) -> None:
        with pytest.raises(SkillNotFoundError):
            await self.storage.get_skill_by_name(name="NONEXISTENT")

    async def test_update_skill_not_found(self) -> None:
        with pytest.raises(SkillNotFoundError):
            await self.storage.update_skill(
                self.factory.skill(skill_id=999, name="Unknown", max_level=10)
            )

    async def test_delete_skill_not_found(self) -> None:
        with pytest.raises(SkillNotFoundError):
            await self.storage.delete_skill(skill_id=999)
