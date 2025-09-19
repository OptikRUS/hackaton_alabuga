from unittest.mock import AsyncMock

from dishka import Provider, Scope, provide
from fastapi import Request
from fastapi.security import HTTPBearer

from src.api.auth.schemas import JwtUser
from src.core.exceptions import InvalidJWTTokenError
from src.core.missions.use_cases import CreateMissionBranchUseCase, GetMissionBranchesUseCase
from src.core.password import PasswordService
from src.core.users.use_cases import CreateUserUseCase, GetUserUseCase, LoginUserUseCase
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
    def override_create_mission_branch_use_cas(self) -> CreateMissionBranchUseCase:
        return AsyncMock(spec=CreateMissionBranchUseCase)

    @provide
    def override_get_mission_branches_use_case(self) -> GetMissionBranchesUseCase:
        return AsyncMock(spec=GetMissionBranchesUseCase)


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
