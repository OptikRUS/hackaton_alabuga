import pytest
from httpx import codes

from src.core.exceptions import PermissionDeniedError
from src.core.tasks.exceptions import TaskNameAlreadyExistError, TaskNotFoundError
from src.core.users.exceptions import UserNotFoundError
from src.core.tasks.use_cases import (
    CreateMissionTaskUseCase,
    DeleteMissionTaskUseCase,
    GetMissionTaskDetailUseCase,
    GetMissionTasksUseCase,
    TaskApproveUseCase,
    UpdateMissionTaskUseCase,
)
from src.tests.fixtures import APIFixture, ContainerFixture, FactoryFixture


class TestCreateTaskAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(CreateMissionTaskUseCase)

    def test_not_auth(self) -> None:
        response = self.api.create_task(title="TEST", description="TEST")

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.create_task(title="TEST", description="TEST")

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_create_task(self) -> None:
        self.use_case.execute.return_value = self.factory.mission_task(
            task_id=100,
            title="TEST",
            description="TEST",
        )

        response = self.hr_api.create_task(title="TEST", description="TEST")

        assert response.status_code == codes.CREATED
        assert response.json() == {"id": 100, "title": "TEST", "description": "TEST"}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            task=self.factory.mission_task(
                task_id=0,
                title="TEST",
                description="TEST",
            )
        )

    def test_create_task_already_exists(self) -> None:
        self.use_case.execute.side_effect = TaskNameAlreadyExistError

        response = self.hr_api.create_task(title="TEST", description="TEST")

        assert response.status_code == codes.CONFLICT
        assert response.json() == {"detail": TaskNameAlreadyExistError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            task=self.factory.mission_task(
                task_id=0,
                title="TEST",
                description="TEST",
            )
        )


class TestGetTasksAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetMissionTasksUseCase)

    def test_not_auth(self) -> None:
        response = self.api.get_tasks()

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_get_tasks(self) -> None:
        self.use_case.execute.return_value = self.factory.mission_tasks(
            values=[
                self.factory.mission_task(
                    task_id=1,
                    title="TASK_1",
                    description="Description 1",
                ),
                self.factory.mission_task(
                    task_id=2,
                    title="TASK_2",
                    description="Description 2",
                ),
            ]
        )

        response = self.hr_api.get_tasks()

        assert response.status_code == codes.OK
        assert response.json() == {
            "values": [
                {"id": 1, "title": "TASK_1", "description": "Description 1"},
                {"id": 2, "title": "TASK_2", "description": "Description 2"},
            ]
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with()

    def test_get_tasks_empty(self) -> None:
        self.use_case.execute.return_value = self.factory.mission_tasks(values=[])

        response = self.candidate_api.get_tasks()

        assert response.status_code == codes.OK
        assert response.json() == {"values": []}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with()


class TestGetTaskDetailAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(GetMissionTaskDetailUseCase)

    def test_not_auth(self) -> None:
        response = self.api.get_task(task_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_get_task(self) -> None:
        self.use_case.execute.return_value = self.factory.mission_task(
            task_id=1,
            title="TEST_TASK",
            description="Test task description",
        )

        response = self.hr_api.get_task(task_id=1)

        assert response.status_code == codes.OK
        assert response.json() == {
            "id": 1,
            "title": "TEST_TASK",
            "description": "Test task description",
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(task_id=1)

    def test_get_task_not_found(self) -> None:
        self.use_case.execute.side_effect = TaskNotFoundError

        response = self.candidate_api.get_task(task_id=999)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": TaskNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(task_id=999)


class TestUpdateTaskAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(UpdateMissionTaskUseCase)

    def test_not_auth(self) -> None:
        response = self.api.update_task(task_id=1, title="TEST", description="TEST")

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.update_task(task_id=1, title="TEST", description="TEST")

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_update_task(self) -> None:
        self.use_case.execute.return_value = self.factory.mission_task(
            task_id=1,
            title="TEST",
            description="TEST",
        )

        response = self.hr_api.update_task(task_id=1, title="TEST", description="TEST")

        assert response.status_code == codes.OK
        assert response.json() == {
            "id": 1,
            "title": "TEST",
            "description": "TEST",
        }
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            task=self.factory.mission_task(task_id=1, title="TEST", description="TEST")
        )

    def test_update_task_already_exists(self) -> None:
        self.use_case.execute.side_effect = TaskNameAlreadyExistError

        response = self.hr_api.update_task(task_id=1, title="TEST", description="TEST")

        assert response.status_code == codes.CONFLICT
        assert response.json() == {"detail": TaskNameAlreadyExistError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            task=self.factory.mission_task(
                task_id=1,
                title="TEST",
                description="TEST",
            )
        )

    def test_update_task_not_found(self) -> None:
        self.use_case.execute.side_effect = TaskNotFoundError

        response = self.hr_api.update_task(task_id=999, title="TEST", description="TEST")

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": TaskNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            task=self.factory.mission_task(
                task_id=999,
                title="TEST",
                description="TEST",
            )
        )


class TestDeleteTaskAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(DeleteMissionTaskUseCase)

    def test_not_auth(self) -> None:
        response = self.api.delete_task(task_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.delete_task(task_id=1)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_delete_task(self) -> None:
        self.use_case.execute.return_value = None

        response = self.hr_api.delete_task(task_id=1)

        assert response.status_code == codes.NO_CONTENT
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(task_id=1)

    def test_delete_task_not_found(self) -> None:
        self.use_case.execute.side_effect = TaskNotFoundError

        response = self.hr_api.delete_task(task_id=999)

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": TaskNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(task_id=999)


class TestApproveTaskAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(TaskApproveUseCase)

    def test_not_auth(self) -> None:
        response = self.api.approve_task(task_id=1, user_login="test_user")

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.approve_task(task_id=1, user_login="test_user")

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_approve_task(self) -> None:
        self.use_case.execute.return_value = None

        response = self.hr_api.approve_task(task_id=1, user_login="test_user")

        assert response.status_code == codes.NO_CONTENT
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            params=self.factory.task_approve_params(task_id=1, user_login="test_user")
        )

    def test_approve_task_not_found(self) -> None:
        self.use_case.execute.side_effect = TaskNotFoundError

        response = self.hr_api.approve_task(task_id=999, user_login="test_user")

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": TaskNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            params=self.factory.task_approve_params(task_id=999, user_login="test_user")
        )

    def test_approve_task_user_not_found(self) -> None:
        self.use_case.execute.side_effect = UserNotFoundError

        response = self.hr_api.approve_task(task_id=1, user_login="nonexistent_user")

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": UserNotFoundError.detail}
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(
            params=self.factory.task_approve_params(task_id=1, user_login="nonexistent_user")
        )
