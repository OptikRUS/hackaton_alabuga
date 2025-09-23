import pytest

from src.core.ranks.exceptions import RankCompetencyMinLevelTooHighError
from src.storages.database_storage import DatabaseStorage
from src.tests.fixtures import FactoryFixture, StorageFixture


class TestRankCompetencyRelations(FactoryFixture, StorageFixture):
    @pytest.fixture(autouse=True)
    async def setup(self, storage: DatabaseStorage) -> None:
        self.storage = storage
        rank = await self.storage_helper.insert_rank(
            rank=self.factory.rank(name="TEST_RANK", required_xp=1000)
        )
        assert rank is not None
        self.inserted_rank = rank

    async def test_add_required_competency_to_rank(self) -> None:
        competency = await self.storage_helper.insert_competency(
            competency=self.factory.competency(name="TEST_COMPETENCY", max_level=100)
        )
        assert competency is not None

        await self.storage.add_required_competency_to_rank(
            rank_id=self.inserted_rank.id,
            competency_id=competency.id,
            min_level=50,
        )

        rank_model = await self.storage_helper.get_rank_by_id_with_entities(
            rank_id=self.inserted_rank.id
        )
        rank_schema = rank_model.to_schema() if rank_model else None
        assert rank_schema is not None
        assert rank_schema.name == "TEST_RANK"
        assert rank_schema.required_xp == 1000
        assert rank_schema.required_competencies is not None
        assert len(rank_schema.required_competencies) == 1
        assert rank_schema.required_competencies[0].competency.id == competency.id

    async def test_remove_required_competency_from_rank(self) -> None:
        competency = await self.storage_helper.insert_competency(
            competency=self.factory.competency(name="TEST_COMPETENCY", max_level=100)
        )
        assert competency is not None

        await self.storage.add_required_competency_to_rank(
            rank_id=self.inserted_rank.id,
            competency_id=competency.id,
            min_level=50,
        )

        await self.storage.remove_required_competency_from_rank(
            rank_id=self.inserted_rank.id,
            competency_id=competency.id,
        )

        rank_model = await self.storage_helper.get_rank_by_id_with_entities(
            rank_id=self.inserted_rank.id
        )
        rank_schema = rank_model.to_schema() if rank_model else None
        assert rank_schema is not None
        assert rank_schema.required_competencies is not None
        assert len(rank_schema.required_competencies) == 0

    async def test_add_multiple_required_competencies_to_rank(self) -> None:
        competency_1 = await self.storage_helper.insert_competency(
            competency=self.factory.competency(name="TEST_COMPETENCY_1", max_level=100)
        )
        competency_2 = await self.storage_helper.insert_competency(
            competency=self.factory.competency(name="TEST_COMPETENCY_2", max_level=50)
        )
        assert competency_1 is not None
        assert competency_2 is not None

        await self.storage.add_required_competency_to_rank(
            rank_id=self.inserted_rank.id,
            competency_id=competency_1.id,
            min_level=50,
        )
        await self.storage.add_required_competency_to_rank(
            rank_id=self.inserted_rank.id,
            competency_id=competency_2.id,
            min_level=25,
        )

        rank_model = await self.storage_helper.get_rank_by_id_with_entities(
            rank_id=self.inserted_rank.id
        )
        assert rank_model is not None
        rank_schema = rank_model.to_schema()
        assert rank_schema is not None
        assert rank_schema.required_competencies is not None
        assert len(rank_schema.required_competencies) == 2
        assert rank_schema.required_competencies[0].competency.id == competency_1.id
        assert rank_schema.required_competencies[0].min_level == 50
        assert rank_schema.required_competencies[1].competency.id == competency_2.id
        assert rank_schema.required_competencies[1].min_level == 25

    async def test_competency_min_level_validation(self) -> None:
        competency = await self.storage_helper.insert_competency(
            competency=self.factory.competency(name="TEST_COMPETENCY", max_level=100)
        )
        assert competency is not None

        with pytest.raises(RankCompetencyMinLevelTooHighError):
            await self.storage.add_required_competency_to_rank(
                rank_id=self.inserted_rank.id,
                competency_id=competency.id,
                min_level=0,
            )

        with pytest.raises(RankCompetencyMinLevelTooHighError):
            await self.storage.add_required_competency_to_rank(
                rank_id=self.inserted_rank.id,
                competency_id=competency.id,
                min_level=101,
            )

        await self.storage.add_required_competency_to_rank(
            rank_id=self.inserted_rank.id,
            competency_id=competency.id,
            min_level=50,
        )

        rank_model = await self.storage_helper.get_rank_by_id_with_entities(
            rank_id=self.inserted_rank.id
        )
        assert rank_model is not None
        rank_schema = rank_model.to_schema()
        assert rank_schema is not None
        assert rank_schema.required_competencies is not None
        assert len(rank_schema.required_competencies) == 1
        assert rank_schema.required_competencies[0].min_level == 50
