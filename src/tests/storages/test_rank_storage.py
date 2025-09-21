import pytest

from src.core.missions.schemas import Mission
from src.core.ranks.exceptions import (
    RankCompetencyMinLevelTooHighError,
    RankNameAlreadyExistError,
    RankNotFoundError,
)
from src.storages.database_storage import DatabaseStorage
from src.tests.fixtures import FactoryFixture, StorageFixture


class TestRankStorage(FactoryFixture, StorageFixture):
    @pytest.fixture(autouse=True)
    async def setup(self, storage: DatabaseStorage) -> None:
        self.storage = storage
        # Create baseline data
        await self.storage.insert_rank(self.factory.rank(name="Bronze", required_xp=100))
        self.created = await self.storage.get_rank_by_name(name="Bronze")

    async def test_get_rank_by_id(self) -> None:
        rank = await self.storage.get_rank_by_id(rank_id=self.created.id)
        assert rank.name == "Bronze"
        assert rank.required_xp == 100
        assert rank.required_missions == []
        assert rank.required_competencies == []

    async def test_get_rank_by_name(self) -> None:
        rank = await self.storage.get_rank_by_name(name="Bronze")
        assert rank.id == self.created.id

    async def test_insert_rank_duplicate(self) -> None:
        with pytest.raises(RankNameAlreadyExistError):
            await self.storage.insert_rank(self.factory.rank(name="Bronze", required_xp=200))

    async def test_list_ranks(self) -> None:
        await self.storage.insert_rank(self.factory.rank(name="Silver", required_xp=200))
        ranks = await self.storage.list_ranks()
        assert len(ranks.values) >= 2

    async def test_update_rank(self) -> None:
        await self.storage.update_rank(
            self.factory.rank(rank_id=self.created.id, name="Bronze+", required_xp=150)
        )
        updated = await self.storage.get_rank_by_id(rank_id=self.created.id)
        assert updated.name == "Bronze+"
        assert updated.required_xp == 150

    async def test_update_rank_duplicate_name(self) -> None:
        await self.storage.insert_rank(self.factory.rank(name="Silver", required_xp=200))
        silver = await self.storage.get_rank_by_name(name="Silver")
        with pytest.raises(RankNameAlreadyExistError):
            await self.storage.update_rank(
                self.factory.rank(rank_id=silver.id, name="Bronze", required_xp=200)
            )

    async def test_delete_rank(self) -> None:
        await self.storage.delete_rank(rank_id=self.created.id)
        with pytest.raises(RankNotFoundError):
            await self.storage.get_rank_by_id(rank_id=self.created.id)

    async def test_get_rank_not_found_by_id(self) -> None:
        with pytest.raises(RankNotFoundError):
            await self.storage.get_rank_by_id(rank_id=999)

    async def test_get_rank_not_found_by_name(self) -> None:
        with pytest.raises(RankNotFoundError):
            await self.storage.get_rank_by_name(name="NONEXISTENT")

    async def test_update_rank_not_found(self) -> None:
        with pytest.raises(RankNotFoundError):
            await self.storage.update_rank(self.factory.rank(rank_id=999, name="X", required_xp=1))

    async def test_delete_rank_not_found(self) -> None:
        with pytest.raises(RankNotFoundError):
            await self.storage.delete_rank(rank_id=999)

    async def test_add_remove_required_mission(self) -> None:
        # Create a branch and a mission to require (FK requires existing branch)
        branch = await self.storage_helper.insert_branch(self.factory.mission_branch(name="BR1"))
        assert branch is not None
        mission_model = await self.storage_helper.insert_mission(
            mission=self.factory.mission(title="M1", branch_id=branch.id)
        )
        assert mission_model is not None
        mission = mission_model.to_schema()

        await self.storage.add_required_mission_to_rank(
            rank_id=self.created.id, mission_id=mission.id
        )
        got = await self.storage.get_rank_by_id(rank_id=self.created.id)
        assert isinstance(got.required_missions, list)
        assert any(
            isinstance(m, Mission) and m.id == mission.id for m in (got.required_missions or [])
        )

        await self.storage.remove_required_mission_from_rank(
            rank_id=self.created.id, mission_id=mission.id
        )
        got2 = await self.storage.get_rank_by_id(rank_id=self.created.id)
        assert all(m.id != mission.id for m in (got2.required_missions or []))

    async def test_add_remove_required_competency(self) -> None:
        # Create competency to require
        await self.storage.insert_competency(self.factory.competency(name="ML", max_level=5))
        comp = await self.storage.get_competency_by_name(name="ML")

        await self.storage.add_required_competency_to_rank(
            rank_id=self.created.id, competency_id=comp.id, min_level=3
        )
        got = await self.storage.get_rank_by_id(rank_id=self.created.id)
        assert any(
            req.competency.id == comp.id and req.min_level == 3
            for req in (got.required_competencies or [])
        )

        await self.storage.remove_required_competency_from_rank(
            rank_id=self.created.id, competency_id=comp.id
        )
        got2 = await self.storage.get_rank_by_id(rank_id=self.created.id)
        assert all(req.competency.id != comp.id for req in (got2.required_competencies or []))

    async def test_add_required_competency_level_too_high(self) -> None:
        await self.storage.insert_competency(self.factory.competency(name="Web", max_level=2))
        comp = await self.storage.get_competency_by_name(name="Web")
        with pytest.raises(RankCompetencyMinLevelTooHighError):
            await self.storage.add_required_competency_to_rank(
                rank_id=self.created.id, competency_id=comp.id, min_level=99
            )
