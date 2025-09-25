import pytest

from src.core.missions.enums import MissionCategoryEnum
from src.core.missions.use_cases import GetMissionsUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestGetMissionsUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = GetMissionsUseCase(storage=self.storage)

    async def test_get_missions(self) -> None:
        await self.storage.insert_mission(
            mission=(
                self.factory.mission(
                    mission_id=1,
                    title="MISSION_1",
                    description="Description 1",
                    reward_xp=100,
                    reward_mana=50,
                    rank_requirement=1,
                    season_id=1,
                    category=MissionCategoryEnum.QUEST,
                )
            )
        )
        await self.storage.insert_mission(
            mission=(
                self.factory.mission(
                    mission_id=2,
                    title="MISSION_2",
                    description="Description 2",
                    reward_xp=200,
                    reward_mana=100,
                    rank_requirement=2,
                    season_id=1,
                    category=MissionCategoryEnum.SIMULATOR,
                )
            )
        )

        missions = await self.use_case.execute()

        assert len(missions.values) == 2
        assert missions == self.factory.missions(
            values=[
                self.factory.mission(
                    mission_id=1,
                    title="MISSION_1",
                    description="Description 1",
                    reward_xp=100,
                    reward_mana=50,
                    rank_requirement=1,
                    season_id=1,
                    category=MissionCategoryEnum.QUEST,
                ),
                self.factory.mission(
                    mission_id=2,
                    title="MISSION_2",
                    description="Description 2",
                    reward_xp=200,
                    reward_mana=100,
                    rank_requirement=2,
                    season_id=1,
                    category=MissionCategoryEnum.SIMULATOR,
                ),
            ]
        )

    async def test_get_empty_missions(self) -> None:
        result = await self.use_case.execute()
        assert len(result.values) == 0
