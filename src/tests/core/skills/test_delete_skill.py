import pytest

from src.core.skills.exceptions import SkillNotFoundError
from src.core.skills.use_cases import DeleteSkillUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestDeleteSkillUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = DeleteSkillUseCase(storage=self.storage)

    async def test_delete_skill(self) -> None:
        await self.storage.insert_skill(
            self.factory.skill(skill_id=1, name="Python", max_level=100)
        )

        await self.use_case.execute(skill_id=1)

        with pytest.raises(SkillNotFoundError):
            await self.storage.get_skill_by_id(skill_id=1)

    async def test_delete_skill_not_found(self) -> None:
        with pytest.raises(SkillNotFoundError):
            await self.use_case.execute(skill_id=999)
