import pytest

from src.core.competencies.exceptions import CompetencyNameAlreadyExistError
from src.core.competencies.use_cases import CreateCompetencyUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestCreateCompetencyUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = CreateCompetencyUseCase(storage=self.storage)

    async def test_create_competency(self) -> None:
        competency = await self.use_case.execute(
            competency=self.factory.competency(competency_id=1, name="ML", max_level=100)
        )

        assert competency == self.factory.competency(competency_id=1, name="ML", max_level=100)

    async def test_create_competency_name_already_exist(self) -> None:
        await self.storage.insert_competency(
            competency=self.factory.competency(competency_id=0, name="ML", max_level=100)
        )

        with pytest.raises(CompetencyNameAlreadyExistError):
            await self.use_case.execute(
                competency=self.factory.competency(competency_id=0, name="ML", max_level=50)
            )
