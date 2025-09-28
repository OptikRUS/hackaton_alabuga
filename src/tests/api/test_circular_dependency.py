import pytest
from httpx import codes

from src.core.mission_chains.exceptions import CircularDependencyError
from src.core.mission_chains.use_cases import AddMissionDependencyUseCase, AddMissionToChainUseCase
from src.tests.fixtures import APIFixture, ContainerFixture, FactoryFixture


class TestCircularDependencyAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.add_mission_dependency_use_case = await self.container.override_use_case(
            AddMissionDependencyUseCase
        )
        self.add_mission_to_chain_use_case = await self.container.override_use_case(
            AddMissionToChainUseCase
        )

    def test_add_mission_dependency_api_self_dependency_returns_400(self) -> None:
        """Тест API: попытка добавить зависимость миссии от самой себя должна возвращать 400"""
        # Arrange
        mission_chain = self.factory.mission_chain()
        mission = self.factory.mission()

        # Настраиваем мок для успешного добавления миссии в цепочку
        self.add_mission_to_chain_use_case.execute.return_value = mission_chain

        # Настраиваем мок для выброса исключения циклической зависимости
        self.add_mission_dependency_use_case.execute.side_effect = CircularDependencyError

        # Act
        response = self.hr_api.add_mission_dependency(
            chain_id=mission_chain.id,
            mission_id=mission.id,
            prerequisite_mission_id=mission.id,
        )

        # Assert
        assert response.status_code == codes.BAD_REQUEST
        assert "Circular dependency detected" in response.json()["detail"]

    def test_add_mission_dependency_api_circular_dependency_returns_400(self) -> None:
        """Тест API: попытка создать циклическую зависимость должна возвращать 400"""
        # Arrange
        mission_chain = self.factory.mission_chain()
        mission1 = self.factory.mission()
        mission2 = self.factory.mission()

        # Настраиваем мок для успешного добавления миссий в цепочку
        self.add_mission_to_chain_use_case.execute.return_value = mission_chain

        # Настраиваем мок для успешного добавления первой зависимости
        self.add_mission_dependency_use_case.execute.return_value = mission_chain

        # Добавляем миссии в цепочку
        self.hr_api.add_mission_to_chain(chain_id=mission_chain.id, mission_id=mission1.id)
        self.hr_api.add_mission_to_chain(chain_id=mission_chain.id, mission_id=mission2.id)

        # Добавляем первую зависимость: mission1 зависит от mission2
        self.hr_api.add_mission_dependency(
            chain_id=mission_chain.id,
            mission_id=mission1.id,
            prerequisite_mission_id=mission2.id,
        )

        # Настраиваем мок для выброса исключения циклической зависимости при второй попытке
        self.add_mission_dependency_use_case.execute.side_effect = CircularDependencyError

        # Act
        # Попытка добавить обратную зависимость: mission2 зависит от mission1
        response = self.hr_api.add_mission_dependency(
            chain_id=mission_chain.id,
            mission_id=mission2.id,
            prerequisite_mission_id=mission1.id,
        )

        # Assert
        assert response.status_code == codes.BAD_REQUEST
        assert "Circular dependency detected" in response.json()["detail"]

    def test_add_mission_dependency_api_valid_dependency_returns_200(self) -> None:
        """Тест API: добавление валидной зависимости должно возвращать 200"""
        # Arrange
        mission_chain = self.factory.mission_chain()
        mission1 = self.factory.mission()
        mission2 = self.factory.mission()

        # Настраиваем мок для успешного добавления миссий в цепочку
        self.add_mission_to_chain_use_case.execute.return_value = mission_chain

        # Настраиваем мок для успешного добавления зависимости
        mission_chain_with_dependency = self.factory.mission_chain(
            dependencies=[
                self.factory.mission_dependency(
                    mission_id=mission2.id, prerequisite_mission_id=mission1.id
                )
            ]
        )
        self.add_mission_dependency_use_case.execute.return_value = mission_chain_with_dependency

        # Добавляем миссии в цепочку
        self.hr_api.add_mission_to_chain(chain_id=mission_chain.id, mission_id=mission1.id)
        self.hr_api.add_mission_to_chain(chain_id=mission_chain.id, mission_id=mission2.id)

        # Act
        response = self.hr_api.add_mission_dependency(
            chain_id=mission_chain.id,
            mission_id=mission2.id,
            prerequisite_mission_id=mission1.id,
        )

        # Assert
        assert response.status_code == codes.OK
        data = response.json()
        assert len(data["dependencies"]) == 1
        assert data["dependencies"][0]["missionId"] == mission2.id
        assert data["dependencies"][0]["prerequisiteMissionId"] == mission1.id
