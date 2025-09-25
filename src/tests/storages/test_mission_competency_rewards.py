import pytest

from src.core.competencies.exceptions import CompetencyLevelIncreaseTooHighError
from src.storages.database_storage import DatabaseStorage
from src.tests.fixtures import FactoryFixture, StorageFixture


class TestMissionCompetencyRewards(FactoryFixture, StorageFixture):
    @pytest.fixture(autouse=True)
    async def setup(self, storage: DatabaseStorage) -> None:
        self.storage = storage
        branch = await self.storage_helper.insert_season(season=self.factory.season(name="TEST"))
        assert branch is not None
        mission = await self.storage_helper.insert_mission(
            mission=self.factory.mission(
                title="TEST",
                description="TEST",
                season_id=branch.id,
            )
        )
        assert mission is not None
        self.inserted_mission = mission.to_schema()

        competency = await self.storage_helper.insert_competency(
            competency=self.factory.competency(name="TEST_COMPETENCY", max_level=100)
        )
        assert competency is not None
        self.inserted_competency = competency

    async def test_add_competency_reward_to_mission(self) -> None:
        await self.storage.add_competency_reward_to_mission(
            mission_id=self.inserted_mission.id,
            competency_id=self.inserted_competency.id,
            level_increase=10,
        )

        mission_model = await self.storage_helper.get_mission_by_id_with_entities(
            mission_id=self.inserted_mission.id
        )
        assert mission_model is not None
        mission = mission_model.to_schema()

        assert mission is not None
        assert mission.title == "TEST"
        assert mission.description == "TEST"
        assert mission.reward_competencies is not None
        assert len(mission.reward_competencies) == 1
        assert mission.reward_competencies[0].competency.id == self.inserted_competency.id

    async def test_remove_competency_reward_from_mission(self) -> None:
        await self.storage.add_competency_reward_to_mission(
            mission_id=self.inserted_mission.id,
            competency_id=self.inserted_competency.id,
            level_increase=10,
        )

        await self.storage.remove_competency_reward_from_mission(
            mission_id=self.inserted_mission.id,
            competency_id=self.inserted_competency.id,
        )

        mission_model = await self.storage_helper.get_mission_by_id_with_entities(
            mission_id=self.inserted_mission.id
        )
        assert mission_model is not None
        mission = mission_model.to_schema()
        assert mission is not None
        assert mission.reward_competencies is not None
        assert len(mission.reward_competencies) == 0

    async def test_add_multiple_competency_rewards_to_mission(self) -> None:
        competency_2 = await self.storage_helper.insert_competency(
            competency=self.factory.competency(name="TEST_COMPETENCY_2", max_level=50)
        )
        assert competency_2 is not None

        await self.storage.add_competency_reward_to_mission(
            mission_id=self.inserted_mission.id,
            competency_id=self.inserted_competency.id,
            level_increase=10,
        )

        await self.storage.add_competency_reward_to_mission(
            mission_id=self.inserted_mission.id,
            competency_id=competency_2.id,
            level_increase=5,
        )

        mission_model = await self.storage_helper.get_mission_by_id_with_entities(
            mission_id=self.inserted_mission.id
        )
        assert mission_model is not None
        mission = mission_model.to_schema()
        assert mission is not None
        assert mission.reward_competencies is not None
        assert len(mission.reward_competencies) == 2

        assert mission.reward_competencies[0].competency.id == self.inserted_competency.id
        assert mission.reward_competencies[0].level_increase == 10
        assert mission.reward_competencies[1].competency.id == competency_2.id
        assert mission.reward_competencies[1].level_increase == 5

    async def test_competency_reward_level_increase_validation(self) -> None:
        with pytest.raises(CompetencyLevelIncreaseTooHighError):
            await self.storage.add_competency_reward_to_mission(
                mission_id=self.inserted_mission.id,
                competency_id=self.inserted_competency.id,
                level_increase=0,
            )

        with pytest.raises(CompetencyLevelIncreaseTooHighError):
            await self.storage.add_competency_reward_to_mission(
                mission_id=self.inserted_mission.id,
                competency_id=self.inserted_competency.id,
                level_increase=101,
            )

        await self.storage.add_competency_reward_to_mission(
            mission_id=self.inserted_mission.id,
            competency_id=self.inserted_competency.id,
            level_increase=50,
        )

        mission_model = await self.storage_helper.get_mission_by_id_with_entities(
            mission_id=self.inserted_mission.id
        )
        assert mission_model is not None
        mission = mission_model.to_schema()
        assert mission is not None
        assert mission.reward_competencies is not None
        assert len(mission.reward_competencies) == 1
        assert mission.reward_competencies[0].level_increase == 50
