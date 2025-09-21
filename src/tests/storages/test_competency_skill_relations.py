import pytest

from src.storages.database_storage import DatabaseStorage
from src.tests.fixtures import FactoryFixture, StorageFixture


class TestCompetencySkillRelations(FactoryFixture, StorageFixture):
    @pytest.fixture(autouse=True)
    async def setup(self, storage: DatabaseStorage) -> None:
        self.storage = storage
        competency = await self.storage_helper.insert_competency(
            competency=self.factory.competency(name="TEST_COMPETENCY", max_level=100)
        )
        assert competency is not None
        self.inserted_competency = competency

    async def test_add_skill_to_competency(self) -> None:
        skill = await self.storage_helper.insert_skill(
            skill=self.factory.skill(name="TEST_SKILL", max_level=50)
        )
        assert skill is not None
        await self.storage.add_skill_to_competency(
            competency_id=self.inserted_competency.id,
            skill_id=skill.id,
        )

        competency_model = await self.storage_helper.get_competency_by_id_with_entities(
            competency_id=self.inserted_competency.id
        )
        competency = competency_model.to_schema() if competency_model else None

        assert competency is not None
        assert competency.name == "TEST_COMPETENCY"
        assert competency.max_level == 100
        assert competency.skills == [skill.to_schema()]

    async def test_remove_skill_from_competency(self) -> None:
        skill = await self.storage_helper.insert_skill(
            skill=self.factory.skill(name="TEST_SKILL", max_level=50)
        )
        assert skill is not None
        await self.storage.add_skill_to_competency(
            competency_id=self.inserted_competency.id,
            skill_id=skill.id,
        )

        await self.storage.remove_skill_from_competency(
            competency_id=self.inserted_competency.id,
            skill_id=skill.id,
        )

        competency_model = await self.storage_helper.get_competency_by_id_with_entities(
            competency_id=self.inserted_competency.id
        )
        competency = competency_model.to_schema() if competency_model else None
        assert competency is not None
        assert competency.skills is not None
        assert len(competency.skills) == 0

    async def test_add_multiple_skills_to_competency(self) -> None:
        skill_1 = await self.storage_helper.insert_skill(
            skill=self.factory.skill(name="TEST_SKILL_1", max_level=50)
        )
        skill_2 = await self.storage_helper.insert_skill(
            skill=self.factory.skill(name="TEST_SKILL_2", max_level=75)
        )
        assert skill_1 is not None
        assert skill_2 is not None

        await self.storage.add_skill_to_competency(
            competency_id=self.inserted_competency.id,
            skill_id=skill_1.id,
        )
        await self.storage.add_skill_to_competency(
            competency_id=self.inserted_competency.id,
            skill_id=skill_2.id,
        )

        competency_model = await self.storage_helper.get_competency_by_id_with_entities(
            competency_id=self.inserted_competency.id
        )
        assert competency_model is not None
        competency = competency_model.to_schema()
        assert competency is not None
        assert competency.skills is not None
        assert len(competency.skills) == 2
        assert competency.skills == [skill_1.to_schema(), skill_2.to_schema()]
