import pytest

from src.core.competencies.exceptions import (
    CompetencyNameAlreadyExistError,
    CompetencyNotFoundError,
)
from src.core.competencies.use_cases import UpdateCompetencyUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestUpdateCompetencyUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = UpdateCompetencyUseCase(storage=self.storage)

    async def test_update_competency(self) -> None:
        await self.storage.insert_competency(
            self.factory.competency(competency_id=1, name="ML", max_level=100)
        )

        updated = await self.use_case.execute(
            competency=self.factory.competency(competency_id=1, name="ML Advanced", max_level=150)
        )

        assert updated == self.factory.competency(
            competency_id=1, name="ML Advanced", max_level=150
        )

    async def test_update_competency_name_already_exist(self) -> None:
        await self.storage.insert_competency(
            self.factory.competency(competency_id=1, name="ML", max_level=100)
        )
        await self.storage.insert_competency(
            self.factory.competency(competency_id=2, name="Web", max_level=50)
        )

        with pytest.raises(CompetencyNameAlreadyExistError):
            await self.use_case.execute(
                competency=self.factory.competency(competency_id=2, name="ML", max_level=60)
            )

    async def test_update_competency_not_found(self) -> None:
        with pytest.raises(CompetencyNotFoundError):
            await self.use_case.execute(
                competency=self.factory.competency(competency_id=999, name="Unknown", max_level=10)
            )
