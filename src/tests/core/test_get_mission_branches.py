import pytest

from src.core.missions.use_cases import GetMissionBranchesUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestGetMissionBranchesUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = GetMissionBranchesUseCase(storage=self.storage)

    async def test_get_mission_branches(self) -> None:
        branch1 = self.factory.mission_branch(branch_id=1, name="BRANCH_1")
        branch2 = self.factory.mission_branch(branch_id=2, name="BRANCH_2")

        await self.storage.insert_mission_branch(branch=branch1)
        await self.storage.insert_mission_branch(branch=branch2)

        result = await self.use_case.execute()

        assert len(result.values) == 2
        assert result.values[0].name == "BRANCH_1"
        assert result.values[1].name == "BRANCH_2"

    async def test_get_empty_mission_branches(self) -> None:
        result = await self.use_case.execute()

        assert len(result.values) == 0
