import pytest

from src.core.skills.exceptions import SkillNameAlreadyExistError, SkillNotFoundError
from src.core.skills.use_cases import UpdateSkillUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestUpdateSkillUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = UpdateSkillUseCase(storage=self.storage)

    async def test_update_skill(self) -> None:
        await self.storage.insert_skill(
            self.factory.skill(skill_id=1, name="Python", max_level=100)
        )

        updated = await self.use_case.execute(
            skill=self.factory.skill(skill_id=1, name="Python Advanced", max_level=150)
        )

        assert updated == self.factory.skill(skill_id=1, name="Python Advanced", max_level=150)

    async def test_update_skill_name_already_exists(self) -> None:
        await self.storage.insert_skill(
            self.factory.skill(skill_id=1, name="Python", max_level=100)
        )
        await self.storage.insert_skill(self.factory.skill(skill_id=2, name="SQL", max_level=50))

        with pytest.raises(SkillNameAlreadyExistError):
            await self.use_case.execute(
                skill=self.factory.skill(skill_id=2, name="Python", max_level=60)
            )

    async def test_update_skill_not_found(self) -> None:
        with pytest.raises(SkillNotFoundError):
            await self.use_case.execute(
                skill=self.factory.skill(skill_id=999, name="Unknown", max_level=10)
            )
