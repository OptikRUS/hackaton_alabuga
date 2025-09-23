import pytest

from src.core.skills.use_cases import GetSkillsUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestGetSkillsUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = GetSkillsUseCase(storage=self.storage)

    async def test_get_skills(self) -> None:
        await self.storage.insert_skill(
            self.factory.skill(skill_id=1, name="Python", max_level=100)
        )
        await self.storage.insert_skill(self.factory.skill(skill_id=2, name="SQL", max_level=50))

        skills = await self.use_case.execute()

        assert len(skills.values) == 2
        assert skills.values[0] == self.factory.skill(skill_id=1, name="Python", max_level=100)
        assert skills.values[1] == self.factory.skill(skill_id=2, name="SQL", max_level=50)
