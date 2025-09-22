import pytest

from src.core.skills.exceptions import SkillNameAlreadyExistError
from src.core.skills.use_cases import CreateSkillUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestCreateSkillUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = CreateSkillUseCase(storage=self.storage)

    async def test_create_skill(self) -> None:
        skill = await self.use_case.execute(
            skill=self.factory.skill(skill_id=1, name="Python", max_level=100)
        )

        assert skill == self.factory.skill(skill_id=1, name="Python", max_level=100)

    async def test_create_skill_name_already_exist(self) -> None:
        await self.storage.insert_skill(
            self.factory.skill(skill_id=0, name="Python", max_level=100)
        )

        with pytest.raises(SkillNameAlreadyExistError):
            await self.use_case.execute(skill=self.factory.skill(skill_id=0, name="Python"))
