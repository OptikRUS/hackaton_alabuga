import pytest

from src.core.skills.exceptions import SkillLevelIncreaseTooHighError
from src.storages.database_storage import DatabaseStorage
from src.tests.fixtures import FactoryFixture, StorageFixture


class TestMissionSkillRewards(FactoryFixture, StorageFixture):
    @pytest.fixture(autouse=True)
    async def setup(self, storage: DatabaseStorage) -> None:
        self.storage = storage
        branch = await self.storage_helper.insert_branch(
            branch=self.factory.mission_branch(name="TEST")
        )
        assert branch is not None
        mission = await self.storage_helper.insert_mission(
            mission=self.factory.mission(
                title="TEST",
                description="TEST",
                branch_id=branch.id,
            )
        )
        assert mission is not None
        self.inserted_mission = mission.to_schema()

        skill = await self.storage_helper.insert_skill(
            skill=self.factory.skill(name="TEST_SKILL", max_level=100)
        )
        assert skill is not None
        self.inserted_skill = skill

    async def test_add_skill_reward_to_mission(self) -> None:
        await self.storage.add_skill_reward_to_mission(
            mission_id=self.inserted_mission.id,
            skill_id=self.inserted_skill.id,
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
        assert mission.reward_skills is not None
        assert len(mission.reward_skills) == 1
        assert mission.reward_skills[0].skill.id == self.inserted_skill.id

    async def test_remove_skill_reward_from_mission(self) -> None:
        await self.storage.add_skill_reward_to_mission(
            mission_id=self.inserted_mission.id,
            skill_id=self.inserted_skill.id,
            level_increase=10,
        )

        await self.storage.remove_skill_reward_from_mission(
            mission_id=self.inserted_mission.id,
            skill_id=self.inserted_skill.id,
        )

        mission_model = await self.storage_helper.get_mission_by_id_with_entities(
            mission_id=self.inserted_mission.id
        )
        assert mission_model is not None
        mission = mission_model.to_schema()
        assert mission is not None
        assert mission.reward_skills is not None
        assert len(mission.reward_skills) == 0

    async def test_add_multiple_skill_rewards_to_mission(self) -> None:
        skill = await self.storage_helper.insert_skill(
            skill=self.factory.skill(name="TEST_SKILL_2", max_level=50)
        )
        assert skill is not None

        await self.storage.add_skill_reward_to_mission(
            mission_id=self.inserted_mission.id,
            skill_id=self.inserted_skill.id,
            level_increase=10,
        )
        await self.storage.add_skill_reward_to_mission(
            mission_id=self.inserted_mission.id,
            skill_id=skill.id,
            level_increase=5,
        )

        mission_model = await self.storage_helper.get_mission_by_id_with_entities(
            mission_id=self.inserted_mission.id
        )
        assert mission_model is not None
        mission = mission_model.to_schema()
        assert mission is not None
        assert mission.reward_skills is not None
        assert len(mission.reward_skills) == 2

        assert mission.reward_skills[0].skill.id == self.inserted_skill.id
        assert mission.reward_skills[0].level_increase == 10

        assert mission.reward_skills[1].skill.id == skill.id
        assert mission.reward_skills[1].level_increase == 5

    async def test_skill_reward_level_increase_validation(self) -> None:
        with pytest.raises(SkillLevelIncreaseTooHighError):
            await self.storage.add_skill_reward_to_mission(
                mission_id=self.inserted_mission.id,
                skill_id=self.inserted_skill.id,
                level_increase=0,
            )

        with pytest.raises(SkillLevelIncreaseTooHighError):
            await self.storage.add_skill_reward_to_mission(
                mission_id=self.inserted_mission.id,
                skill_id=self.inserted_skill.id,
                level_increase=101,
            )

        await self.storage.add_skill_reward_to_mission(
            mission_id=self.inserted_mission.id,
            skill_id=self.inserted_skill.id,
            level_increase=50,
        )

        mission_model = await self.storage_helper.get_mission_by_id_with_entities(
            mission_id=self.inserted_mission.id
        )
        assert mission_model is not None
        mission = mission_model.to_schema()
        assert mission is not None
        assert mission.reward_skills is not None
        assert len(mission.reward_skills) == 1
        assert mission.reward_skills[0].level_increase == 50
