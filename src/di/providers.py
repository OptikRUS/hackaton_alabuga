from collections.abc import AsyncIterator

from aiobotocore.client import AioBaseClient
from dishka import Provider, Scope, provide
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth.schemas import JwtCandidateUser, JwtHRUser, JwtUser
from src.clients.minio import get_minio_client
from src.core.artifacts.use_cases import (
    AddArtifactToMissionUseCase,
    AddArtifactToUserUseCase,
    CreateArtifactUseCase,
    DeleteArtifactUseCase,
    GetArtifactDetailUseCase,
    GetArtifactsUseCase,
    RemoveArtifactFromMissionUseCase,
    RemoveArtifactFromUserUseCase,
    UpdateArtifactUseCase,
)
from src.core.competencies.use_cases import (
    AddSkillToCompetencyUseCase,
    CreateCompetencyUseCase,
    DeleteCompetencyUseCase,
    GetCompetenciesUseCase,
    GetCompetencyDetailUseCase,
    RemoveSkillFromCompetencyUseCase,
    UpdateCompetencyUseCase,
)
from src.core.exceptions import InvalidJWTTokenError, PermissionDeniedError
from src.core.mission_chains.use_cases import (
    AddMissionDependencyUseCase,
    AddMissionToChainUseCase,
    CreateMissionChainUseCase,
    DeleteMissionChainUseCase,
    GetMissionChainDetailUseCase,
    GetMissionChainsUseCase,
    RemoveMissionDependencyUseCase,
    RemoveMissionFromChainUseCase,
    UpdateMissionChainUseCase,
    UpdateMissionOrderInChainUseCase,
)
from src.core.missions.use_cases import (
    AddCompetencyRewardToMissionUseCase,
    AddSkillRewardToMissionUseCase,
    AddTaskToMissionUseCase,
    CreateMissionUseCase,
    DeleteMissionUseCase,
    GetMissionDetailUseCase,
    GetMissionsUseCase,
    GetMissionWithUserTasksUseCase,
    RemoveCompetencyRewardFromMissionUseCase,
    RemoveSkillRewardFromMissionUseCase,
    RemoveTaskFromMissionUseCase,
    UpdateMissionUseCase,
)
from src.core.password import PasswordService
from src.core.ranks.use_cases import (
    AddRequiredCompetencyToRankUseCase,
    AddRequiredMissionToRankUseCase,
    CreateRankUseCase,
    DeleteRankUseCase,
    GetRankDetailUseCase,
    GetRanksUseCase,
    RemoveRequiredCompetencyFromRankUseCase,
    RemoveRequiredMissionFromRankUseCase,
    UpdateRankUseCase,
)
from src.core.seasons.use_cases import (
    CreateSeasonUseCase,
    DeleteSeasonUseCase,
    GetSeasonDetailUseCase,
    GetSeasonsUseCase,
    UpdateSeasonUseCase,
)
from src.core.skills.use_cases import (
    CreateSkillUseCase,
    DeleteSkillUseCase,
    GetSkillDetailUseCase,
    GetSkillsUseCase,
    UpdateSkillUseCase,
)
from src.core.storages import (
    ArtifactStorage,
    CompetencyStorage,
    MissionStorage,
    RankStorage,
    SkillStorage,
    UserStorage,
)
from src.core.tasks.use_cases import (
    CreateMissionTaskUseCase,
    DeleteMissionTaskUseCase,
    GetMissionTaskDetailUseCase,
    GetMissionTasksUseCase,
    UpdateMissionTaskUseCase,
)
from src.core.users.enums import UserRoleEnum
from src.core.users.use_cases import CreateUserUseCase, GetUserUseCase, LoginUserUseCase
from src.services.minio import MinioService
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
    def build_create_season_use_case(self, storage: MissionStorage) -> CreateSeasonUseCase:
        return CreateSeasonUseCase(storage=storage)

    @provide
    def build_get_seasons_use_case(self, storage: MissionStorage) -> GetSeasonsUseCase:
        return GetSeasonsUseCase(storage=storage)

    @provide
    def build_get_season_detail_use_case(self, storage: MissionStorage) -> GetSeasonDetailUseCase:
        return GetSeasonDetailUseCase(storage=storage)

    @provide
    def build_create_mission_use_case(self, storage: MissionStorage) -> CreateMissionUseCase:
        return CreateMissionUseCase(storage=storage)

    @provide
    def build_get_missions_use_case(self, storage: MissionStorage) -> GetMissionsUseCase:
        return GetMissionsUseCase(storage=storage)

    @provide
    def build_get_mission_detail_use_case(self, storage: MissionStorage) -> GetMissionDetailUseCase:
        return GetMissionDetailUseCase(storage=storage)

    @provide
    def build_update_mission_use_case(self, storage: MissionStorage) -> UpdateMissionUseCase:
        return UpdateMissionUseCase(storage=storage)

    @provide
    def build_delete_mission_use_case(self, storage: MissionStorage) -> DeleteMissionUseCase:
        return DeleteMissionUseCase(storage=storage)

    @provide
    def build_update_season_use_case(self, storage: MissionStorage) -> UpdateSeasonUseCase:
        return UpdateSeasonUseCase(storage=storage)

    @provide
    def build_delete_season_use_case(self, storage: MissionStorage) -> DeleteSeasonUseCase:
        return DeleteSeasonUseCase(storage=storage)

    @provide
    def build_create_mission_task_use_case(
        self,
        storage: MissionStorage,
    ) -> CreateMissionTaskUseCase:
        return CreateMissionTaskUseCase(storage=storage)

    @provide
    def build_get_mission_tasks_use_case(self, storage: MissionStorage) -> GetMissionTasksUseCase:
        return GetMissionTasksUseCase(storage=storage)

    @provide
    def build_get_mission_task_detail_use_case(
        self, storage: MissionStorage
    ) -> GetMissionTaskDetailUseCase:
        return GetMissionTaskDetailUseCase(storage=storage)

    @provide
    def build_update_mission_task_use_case(
        self, storage: MissionStorage
    ) -> UpdateMissionTaskUseCase:
        return UpdateMissionTaskUseCase(storage=storage)

    @provide
    def build_delete_mission_task_use_case(
        self, storage: MissionStorage
    ) -> DeleteMissionTaskUseCase:
        return DeleteMissionTaskUseCase(storage=storage)

    @provide
    def build_add_task_to_mission_use_case(
        self, storage: MissionStorage
    ) -> AddTaskToMissionUseCase:
        return AddTaskToMissionUseCase(storage=storage)

    @provide
    def build_remove_task_from_mission_use_case(
        self, storage: MissionStorage
    ) -> RemoveTaskFromMissionUseCase:
        return RemoveTaskFromMissionUseCase(storage=storage)

    @provide
    def build_add_competency_reward_to_mission_use_case(
        self, storage: MissionStorage
    ) -> AddCompetencyRewardToMissionUseCase:
        return AddCompetencyRewardToMissionUseCase(storage=storage)

    @provide
    def build_remove_competency_reward_from_mission_use_case(
        self, storage: MissionStorage
    ) -> RemoveCompetencyRewardFromMissionUseCase:
        return RemoveCompetencyRewardFromMissionUseCase(storage=storage)

    @provide
    def build_add_skill_reward_to_mission_use_case(
        self, storage: MissionStorage
    ) -> AddSkillRewardToMissionUseCase:
        return AddSkillRewardToMissionUseCase(storage=storage)

    @provide
    def build_remove_skill_reward_from_mission_use_case(
        self, storage: MissionStorage
    ) -> RemoveSkillRewardFromMissionUseCase:
        return RemoveSkillRewardFromMissionUseCase(storage=storage)

    @provide
    def build_get_mission_with_user_tasks_use_case(
        self, storage: MissionStorage
    ) -> GetMissionWithUserTasksUseCase:
        return GetMissionWithUserTasksUseCase(storage=storage)


class MissionChainProvider(Provider):
    scope: Scope = Scope.REQUEST

    @provide
    def build_create_mission_chain_use_case(
        self, storage: MissionStorage
    ) -> CreateMissionChainUseCase:
        return CreateMissionChainUseCase(storage=storage)

    @provide
    def build_get_mission_chains_use_case(self, storage: MissionStorage) -> GetMissionChainsUseCase:
        return GetMissionChainsUseCase(storage=storage)

    @provide
    def build_get_mission_chain_detail_use_case(
        self, storage: MissionStorage
    ) -> GetMissionChainDetailUseCase:
        return GetMissionChainDetailUseCase(storage=storage)

    @provide
    def build_update_mission_chain_use_case(
        self, storage: MissionStorage
    ) -> UpdateMissionChainUseCase:
        return UpdateMissionChainUseCase(storage=storage)

    @provide
    def build_delete_mission_chain_use_case(
        self, storage: MissionStorage
    ) -> DeleteMissionChainUseCase:
        return DeleteMissionChainUseCase(storage=storage)

    @provide
    def build_add_mission_to_chain_use_case(
        self, storage: MissionStorage
    ) -> AddMissionToChainUseCase:
        return AddMissionToChainUseCase(storage=storage)

    @provide
    def build_remove_mission_from_chain_use_case(
        self, storage: MissionStorage
    ) -> RemoveMissionFromChainUseCase:
        return RemoveMissionFromChainUseCase(storage=storage)

    @provide
    def build_add_mission_dependency_use_case(
        self, storage: MissionStorage
    ) -> AddMissionDependencyUseCase:
        return AddMissionDependencyUseCase(storage=storage)

    @provide
    def build_remove_mission_dependency_use_case(
        self, storage: MissionStorage
    ) -> RemoveMissionDependencyUseCase:
        return RemoveMissionDependencyUseCase(storage=storage)

    @provide
    def build_update_mission_order_in_chain_use_case(
        self, storage: MissionStorage
    ) -> UpdateMissionOrderInChainUseCase:
        return UpdateMissionOrderInChainUseCase(storage=storage)


class CompetencyProvider(Provider):
    scope: Scope = Scope.REQUEST

    @provide
    def build_create_competency_use_case(
        self,
        storage: CompetencyStorage,
    ) -> CreateCompetencyUseCase:
        return CreateCompetencyUseCase(storage=storage)

    @provide
    def build_get_competencies_use_case(self, storage: CompetencyStorage) -> GetCompetenciesUseCase:
        return GetCompetenciesUseCase(storage=storage)

    @provide
    def build_get_competency_detail_use_case(
        self, storage: CompetencyStorage
    ) -> GetCompetencyDetailUseCase:
        return GetCompetencyDetailUseCase(storage=storage)

    @provide
    def build_update_competency_use_case(
        self, storage: CompetencyStorage
    ) -> UpdateCompetencyUseCase:
        return UpdateCompetencyUseCase(storage=storage)

    @provide
    def build_delete_competency_use_case(
        self, storage: CompetencyStorage
    ) -> DeleteCompetencyUseCase:
        return DeleteCompetencyUseCase(storage=storage)

    @provide
    def build_add_skill_to_competency_use_case(
        self, storage: CompetencyStorage
    ) -> AddSkillToCompetencyUseCase:
        return AddSkillToCompetencyUseCase(storage=storage)

    @provide
    def build_remove_skill_from_competency_use_case(
        self, storage: CompetencyStorage
    ) -> RemoveSkillFromCompetencyUseCase:
        return RemoveSkillFromCompetencyUseCase(storage=storage)


class RankProvider(Provider):
    scope: Scope = Scope.REQUEST

    @provide
    def build_create_rank_use_case(
        self,
        storage: RankStorage,
    ) -> CreateRankUseCase:
        return CreateRankUseCase(storage=storage)

    @provide
    def build_get_ranks_use_case(self, storage: RankStorage) -> GetRanksUseCase:
        return GetRanksUseCase(storage=storage)

    @provide
    def build_get_rank_detail_use_case(self, storage: RankStorage) -> GetRankDetailUseCase:
        return GetRankDetailUseCase(storage=storage)

    @provide
    def build_update_rank_use_case(self, storage: RankStorage) -> UpdateRankUseCase:
        return UpdateRankUseCase(storage=storage)

    @provide
    def build_delete_rank_use_case(self, storage: RankStorage) -> DeleteRankUseCase:
        return DeleteRankUseCase(storage=storage)

    @provide
    def build_add_required_mission_to_rank_use_case(
        self, storage: RankStorage
    ) -> AddRequiredMissionToRankUseCase:
        return AddRequiredMissionToRankUseCase(storage=storage)

    @provide
    def build_remove_required_mission_from_rank_use_case(
        self, storage: RankStorage
    ) -> RemoveRequiredMissionFromRankUseCase:
        return RemoveRequiredMissionFromRankUseCase(storage=storage)

    @provide
    def build_add_required_competency_to_rank_use_case(
        self, storage: RankStorage
    ) -> AddRequiredCompetencyToRankUseCase:
        return AddRequiredCompetencyToRankUseCase(storage=storage)

    @provide
    def build_remove_required_competency_from_rank_use_case(
        self, storage: RankStorage
    ) -> RemoveRequiredCompetencyFromRankUseCase:
        return RemoveRequiredCompetencyFromRankUseCase(storage=storage)


class SkillProvider(Provider):
    scope: Scope = Scope.REQUEST

    @provide
    def build_create_skill_use_case(
        self,
        storage: SkillStorage,
    ) -> CreateSkillUseCase:
        return CreateSkillUseCase(storage=storage)

    @provide
    def build_get_skills_use_case(self, storage: SkillStorage) -> GetSkillsUseCase:
        return GetSkillsUseCase(storage=storage)

    @provide
    def build_get_skill_detail_use_case(self, storage: SkillStorage) -> GetSkillDetailUseCase:
        return GetSkillDetailUseCase(storage=storage)

    @provide
    def build_update_skill_use_case(self, storage: SkillStorage) -> UpdateSkillUseCase:
        return UpdateSkillUseCase(storage=storage)

    @provide
    def build_delete_skill_use_case(self, storage: SkillStorage) -> DeleteSkillUseCase:
        return DeleteSkillUseCase(storage=storage)


class ArtifactProvider(Provider):
    scope: Scope = Scope.REQUEST

    @provide
    def build_create_artifact_use_case(
        self,
        storage: ArtifactStorage,
    ) -> CreateArtifactUseCase:
        return CreateArtifactUseCase(storage=storage)

    @provide
    def build_get_artifacts_use_case(self, storage: ArtifactStorage) -> GetArtifactsUseCase:
        return GetArtifactsUseCase(storage=storage)

    @provide
    def build_get_artifact_detail_use_case(
        self, storage: ArtifactStorage
    ) -> GetArtifactDetailUseCase:
        return GetArtifactDetailUseCase(storage=storage)

    @provide
    def build_update_artifact_use_case(self, storage: ArtifactStorage) -> UpdateArtifactUseCase:
        return UpdateArtifactUseCase(storage=storage)

    @provide
    def build_delete_artifact_use_case(self, storage: ArtifactStorage) -> DeleteArtifactUseCase:
        return DeleteArtifactUseCase(storage=storage)

    @provide
    def build_add_artifact_to_mission_use_case(
        self, storage: ArtifactStorage, mission_storage: MissionStorage
    ) -> AddArtifactToMissionUseCase:
        return AddArtifactToMissionUseCase(storage=storage, mission_storage=mission_storage)

    @provide
    def build_remove_artifact_from_mission_use_case(
        self, storage: ArtifactStorage, mission_storage: MissionStorage
    ) -> RemoveArtifactFromMissionUseCase:
        return RemoveArtifactFromMissionUseCase(storage=storage, mission_storage=mission_storage)

    @provide
    def build_add_artifact_to_user_use_case(
        self, storage: ArtifactStorage, user_storage: UserStorage
    ) -> AddArtifactToUserUseCase:
        return AddArtifactToUserUseCase(storage=storage, user_storage=user_storage)

    @provide
    def build_remove_artifact_from_user_use_case(
        self, storage: ArtifactStorage, user_storage: UserStorage
    ) -> RemoveArtifactFromUserUseCase:
        return RemoveArtifactFromUserUseCase(storage=storage, user_storage=user_storage)


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
    def get_mission_storage(self, session: AsyncSession) -> MissionStorage:
        return DatabaseStorage(session=session)

    @provide
    def get_competency_storage(self, session: AsyncSession) -> CompetencyStorage:
        return DatabaseStorage(session=session)

    @provide
    def get_rank_storage(self, session: AsyncSession) -> RankStorage:
        return DatabaseStorage(session=session)

    @provide
    def get_skill_storage(self, session: AsyncSession) -> SkillStorage:
        return DatabaseStorage(session=session)

    @provide
    def get_artifact_storage(self, session: AsyncSession) -> ArtifactStorage:
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

    @provide(scope=Scope.REQUEST)
    async def hr_auth(self, jwt_user: JwtUser) -> JwtHRUser:
        if jwt_user.role == UserRoleEnum.HR:
            return JwtHRUser(login=jwt_user.login, role=jwt_user.role)
        raise PermissionDeniedError

    @provide(scope=Scope.REQUEST)
    async def candidate_auth(self, jwt_user: JwtUser) -> JwtCandidateUser:
        if jwt_user.role == UserRoleEnum.CANDIDATE:
            return JwtCandidateUser(login=jwt_user.login, role=jwt_user.role)
        raise PermissionDeniedError


class FileStorageProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.REQUEST)
    async def get_minio_connection(self) -> AsyncIterator[AioBaseClient]:
        async with get_minio_client() as minio_connection:
            yield minio_connection

    @provide
    async def get_minio_service(self, minio_connection: AioBaseClient) -> MinioService:
        return MinioService(minio_connection=minio_connection)
