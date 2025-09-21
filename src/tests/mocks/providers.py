from unittest.mock import AsyncMock

from dishka import Provider, Scope, provide
from fastapi import Request
from fastapi.security import HTTPBearer

from src.api.auth.schemas import JwtUser
from src.core.exceptions import InvalidJWTTokenError
from src.core.missions.use_cases import (
    AddTaskToMissionUseCase,
    CreateMissionBranchUseCase,
    CreateMissionUseCase,
    DeleteMissionBranchUseCase,
    DeleteMissionUseCase,
    GetMissionBranchesUseCase,
    GetMissionDetailUseCase,
    GetMissionsUseCase,
    RemoveTaskFromMissionUseCase,
    UpdateMissionBranchUseCase,
    UpdateMissionUseCase,
)
from src.core.password import PasswordService
from src.core.tasks.use_cases import (
    CreateMissionTaskUseCase,
    DeleteMissionTaskUseCase,
    GetMissionTaskDetailUseCase,
    GetMissionTasksUseCase,
    UpdateMissionTaskUseCase,
)
from src.core.users.use_cases import CreateUserUseCase, GetUserUseCase, LoginUserUseCase
from src.services.minio import MinioService
from src.tests.mocks.user_password import UserPasswordServiceMock


class UserProviderMock(Provider):
    scope: Scope = Scope.APP

    @provide
    def override_create_user_use_case(self) -> CreateUserUseCase:
        return AsyncMock(spec=CreateUserUseCase)

    @provide
    def override_get_user_use_case(self) -> GetUserUseCase:
        return AsyncMock(spec=GetUserUseCase)

    @provide
    def override_login_user_use_case(self) -> LoginUserUseCase:
        return AsyncMock(spec=LoginUserUseCase)


class MissionProviderMock(Provider):
    scope: Scope = Scope.APP

    @provide
    def override_create_mission_branch_use_case(self) -> CreateMissionBranchUseCase:
        return AsyncMock(spec=CreateMissionBranchUseCase)

    @provide
    def override_get_mission_branches_use_case(self) -> GetMissionBranchesUseCase:
        return AsyncMock(spec=GetMissionBranchesUseCase)

    @provide
    def override_update_mission_branch_use_case(self) -> UpdateMissionBranchUseCase:
        return AsyncMock(spec=CreateMissionBranchUseCase)

    @provide
    def override_delete_mission_branch_usecase(self) -> DeleteMissionBranchUseCase:
        return AsyncMock(spec=GetMissionBranchesUseCase)

    @provide
    def override_create_mission_use_case(self) -> CreateMissionUseCase:
        return AsyncMock(spec=CreateMissionUseCase)

    @provide
    def override_get_missions_use_case(self) -> GetMissionsUseCase:
        return AsyncMock(spec=GetMissionsUseCase)

    @provide
    def override_get_mission_detail_use_case(self) -> GetMissionDetailUseCase:
        return AsyncMock(spec=GetMissionDetailUseCase)

    @provide
    def override_update_mission_use_case(self) -> UpdateMissionUseCase:
        return AsyncMock(spec=UpdateMissionUseCase)

    @provide
    def override_delete_mission_use_case(self) -> DeleteMissionUseCase:
        return AsyncMock(spec=DeleteMissionUseCase)

    @provide
    def override_create_mission_task_use_case(self) -> CreateMissionTaskUseCase:
        return AsyncMock(storage=CreateMissionTaskUseCase)

    @provide
    def override_get_mission_tasks_use_case(self) -> GetMissionTasksUseCase:
        return AsyncMock(storage=GetMissionTasksUseCase)

    @provide
    def override_get_mission_task_detail_use_case(self) -> GetMissionTaskDetailUseCase:
        return AsyncMock(storage=GetMissionTaskDetailUseCase)

    @provide
    def override_update_mission_task_use_case(self) -> UpdateMissionTaskUseCase:
        return AsyncMock(storage=UpdateMissionTaskUseCase)

    @provide
    def override_delete_mission_task_use_case(self) -> DeleteMissionTaskUseCase:
        return AsyncMock(storage=DeleteMissionTaskUseCase)

    @provide
    def override_add_task_to_mission_use_case(self) -> AddTaskToMissionUseCase:
        return AsyncMock(spec=AddTaskToMissionUseCase)

    @provide
    def override_remove_task_from_mission_use_case(self) -> RemoveTaskFromMissionUseCase:
        return AsyncMock(spec=RemoveTaskFromMissionUseCase)


class FileStorageProviderMock(Provider):
    scope: Scope = Scope.APP

    @provide
    def get_minio_service(self) -> MinioService:
        return AsyncMock(spec=MinioService)


class AuthProviderMock(Provider):
    scope = Scope.APP

    @provide
    def get_password_service(self) -> PasswordService:
        return UserPasswordServiceMock()

    @provide(scope=Scope.REQUEST)
    async def get_jwt_user(self, request: Request) -> JwtUser:
        security = HTTPBearer()
        auth = await security(request=request)
        if not auth:
            raise InvalidJWTTokenError
        return JwtUser.decode(payload=auth.credentials)
