import pytest

from src.core.competencies.exceptions import (
    CompetencyNameAlreadyExistError,
    CompetencyNotFoundError,
)
from src.storages.database_storage import DatabaseStorage
from src.tests.fixtures import FactoryFixture, StorageFixture


class TestCompetencyStorage(FactoryFixture, StorageFixture):
    @pytest.fixture(autouse=True)
    async def setup(self, storage: DatabaseStorage) -> None:
        self.storage = storage
        await self.storage.insert_competency(self.factory.competency(name="ML", max_level=100))
        self.created = await self.storage.get_competency_by_name(name="ML")

    async def test_get_competency_by_id(self) -> None:
        competency = await self.storage.get_competency_by_id(competency_id=self.created.id)
        assert competency == self.factory.competency(
            competency_id=self.created.id, name="ML", max_level=100, skills=[]
        )

    async def test_get_competency_by_name(self) -> None:
        competency = await self.storage.get_competency_by_name(name="ML")
        assert competency == self.factory.competency(
            competency_id=self.created.id, name="ML", max_level=100, skills=[]
        )

    async def test_insert_competency(self) -> None:
        await self.storage.insert_competency(self.factory.competency(name="Web", max_level=50))
        competency = await self.storage.get_competency_by_name(name="Web")
        assert competency.name == "Web"
        assert competency.max_level == 50

    async def test_insert_competency_with_duplicate_name(self) -> None:
        with pytest.raises(CompetencyNameAlreadyExistError):
            await self.storage.insert_competency(self.factory.competency(name="ML", max_level=110))

    async def test_list_competencies(self) -> None:
        await self.storage.insert_competency(self.factory.competency(name="Web", max_level=50))
        competencies = await self.storage.list_competencies()
        assert len(competencies.values) >= 2

    async def test_update_competency(self) -> None:
        await self.storage.update_competency(
            self.factory.competency(
                competency_id=self.created.id, name="ML Advanced", max_level=150
            )
        )
        updated = await self.storage.get_competency_by_id(competency_id=self.created.id)
        assert updated.name == "ML Advanced"
        assert updated.max_level == 150

    async def test_update_competency_with_duplicate_name(self) -> None:
        await self.storage.insert_competency(self.factory.competency(name="Web", max_level=50))
        web = await self.storage.get_competency_by_name(name="Web")
        with pytest.raises(CompetencyNameAlreadyExistError):
            await self.storage.update_competency(
                self.factory.competency(competency_id=web.id, name="ML", max_level=60)
            )

    async def test_delete_competency(self) -> None:
        await self.storage.delete_competency(competency_id=self.created.id)
        with pytest.raises(CompetencyNotFoundError):
            await self.storage.get_competency_by_id(competency_id=self.created.id)

    async def test_get_competency_not_found_by_id(self) -> None:
        with pytest.raises(CompetencyNotFoundError):
            await self.storage.get_competency_by_id(competency_id=999)

    async def test_get_competency_not_found_by_name(self) -> None:
        with pytest.raises(CompetencyNotFoundError):
            await self.storage.get_competency_by_name(name="NONEXISTENT")

    async def test_update_competency_not_found(self) -> None:
        with pytest.raises(CompetencyNotFoundError):
            await self.storage.update_competency(
                self.factory.competency(competency_id=999, name="Unknown", max_level=10)
            )

    async def test_delete_competency_not_found(self) -> None:
        with pytest.raises(CompetencyNotFoundError):
            await self.storage.delete_competency(competency_id=999)
