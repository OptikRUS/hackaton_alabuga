import pytest

from src.core.skills.exceptions import SkillNotFoundError
from src.core.skills.use_cases import GetSkillDetailUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestGetSkillDetailUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = GetSkillDetailUseCase(storage=self.storage)

    async def test_get_skill_detail(self) -> None:
        await self.storage.insert_skill(
            self.factory.skill(skill_id=1, name="Python", max_level=100)
        )

        skill = await self.use_case.execute(skill_id=1)

        assert skill == self.factory.skill(skill_id=1, name="Python", max_level=100)

    async def test_get_skill_not_found(self) -> None:
        with pytest.raises(SkillNotFoundError):
            await self.use_case.execute(skill_id=999)
