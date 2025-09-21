import pytest

from src.core.competencies.exceptions import CompetencyNotFoundError
from src.core.competencies.use_cases import DeleteCompetencyUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestDeleteCompetencyUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = DeleteCompetencyUseCase(storage=self.storage)

    async def test_delete_competency(self) -> None:
        await self.storage.insert_competency(
            competency=self.factory.competency(competency_id=1, name="ML", max_level=100)
        )

        await self.use_case.execute(competency_id=1)

        with pytest.raises(CompetencyNotFoundError):
            await self.storage.get_competency_by_id(competency_id=1)

    async def test_delete_competency_not_found(self) -> None:
        with pytest.raises(CompetencyNotFoundError):
            await self.use_case.execute(competency_id=999)
