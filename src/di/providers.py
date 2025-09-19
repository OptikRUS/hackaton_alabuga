from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth.schemas import JwtUser
from src.core.exceptions import InvalidJWTTokenError
from src.core.missions.use_cases import (
    CreateMissionBranchUseCase,
    CreateMissionUseCase,
    DeleteMissionUseCase,
    GetMissionBranchesUseCase,
    GetMissionsUseCase,
    GetMissionUseCase,
    UpdateMissionUseCase,
)
from src.core.password import PasswordService
from src.core.storages import MissionBranchStorage, MissionStorage, UserStorage
from src.core.users.use_cases import CreateUserUseCase, GetUserUseCase, LoginUserUseCase
from src.services.user_password_service import UserPasswordService
from src.storages.database import async_session
from src.storages.database_storage import DatabaseStorage


class UserProvider(Provider):
    scope: Scope = Scope.REQUEST

    @provide
    def build_create_user_use_case(
        self,
        storage: UserStorage,
        password_service: PasswordService,
    ) -> CreateUserUseCase:
        return CreateUserUseCase(storage=storage, password_service=password_service)

    @provide
    def build_get_user_use_case(self, storage: UserStorage) -> GetUserUseCase:
        return GetUserUseCase(storage=storage)

    @provide
    def build_login_user_use_case(
        self,
        storage: UserStorage,
        password_service: PasswordService,
    ) -> LoginUserUseCase:
        return LoginUserUseCase(storage=storage, password_service=password_service)


class MissionProvider(Provider):
    scope: Scope = Scope.REQUEST

    @provide
    def build_create_mission_branch_use_case(
        self,
        storage: MissionBranchStorage,
    ) -> CreateMissionBranchUseCase:
        return CreateMissionBranchUseCase(storage=storage)

    @provide
    def build_get_mission_branches_use_case(
        self, storage: MissionBranchStorage
    ) -> GetMissionBranchesUseCase:
        return GetMissionBranchesUseCase(storage=storage)

    @provide
    def build_create_mission_use_case(
        self,
        storage: MissionStorage,
    ) -> CreateMissionUseCase:
        return CreateMissionUseCase(storage=storage)

    @provide
    def build_get_missions_use_case(self, storage: MissionStorage) -> GetMissionsUseCase:
        return GetMissionsUseCase(storage=storage)

    @provide
    def build_get_mission_use_case(self, storage: MissionStorage) -> GetMissionUseCase:
        return GetMissionUseCase(storage=storage)

    @provide
    def build_update_mission_use_case(self, storage: MissionStorage) -> UpdateMissionUseCase:
        return UpdateMissionUseCase(storage=storage)

    @provide
    def build_delete_mission_use_case(self, storage: MissionStorage) -> DeleteMissionUseCase:
        return DeleteMissionUseCase(storage=storage)


class DatabaseProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_db_session(self) -> AsyncIterator[AsyncSession]:
        async with async_session() as session:
            yield session
            await session.commit()

    @provide
    def get_user_storage(self, session: AsyncSession) -> UserStorage:
        return DatabaseStorage(session=session)

    @provide
    def get_mission_branch_storage(self, session: AsyncSession) -> MissionBranchStorage:
        return DatabaseStorage(session=session)

    @provide
    def get_mission_storage(self, session: AsyncSession) -> MissionStorage:
        return DatabaseStorage(session=session)


class AuthProvider(Provider):
    scope = Scope.APP

    @provide
    def get_password_service(self) -> PasswordService:
        return UserPasswordService()

    @provide
    async def get_security(self) -> HTTPBearer:
        return HTTPBearer()

    @provide(scope=Scope.REQUEST)
    async def get_auth(
        self,
        request: Request,
        security: HTTPBearer,
    ) -> HTTPAuthorizationCredentials:
        auth = await security(request=request)
        if not auth:
            raise InvalidJWTTokenError
        return auth

    @provide(scope=Scope.REQUEST)
    async def get_jwt_user(self, auth: HTTPAuthorizationCredentials) -> JwtUser:
        return JwtUser.decode(payload=auth.credentials)
