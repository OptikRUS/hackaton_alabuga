import pytest

from src.core.missions.enums import MissionCategoryEnum
from src.core.missions.exceptions import MissionNotFoundError
from src.core.missions.use_cases import GetMissionUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestGetMissionUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = GetMissionUseCase(storage=self.storage)

    async def test_get_mission(self) -> None:
        await self.storage.insert_mission(
            mission=(
                self.factory.mission(
                    mission_id=1,
                    title="TEST_MISSION",
                    description="Test description",
                    reward_xp=100,
                    reward_mana=50,
                    rank_requirement=1,
                    branch_id=1,
                    category=MissionCategoryEnum.QUEST,
                )
            )
        )

        mission = await self.use_case.execute(mission_id=1)

        assert mission == self.factory.mission(
            mission_id=1,
            title="TEST_MISSION",
            description="Test description",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            branch_id=1,
            category=MissionCategoryEnum.QUEST,
        )

    async def test_get_mission_not_found(self) -> None:
        with pytest.raises(MissionNotFoundError):
            await self.use_case.execute(mission_id=999)
