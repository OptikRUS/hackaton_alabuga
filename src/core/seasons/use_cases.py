from dataclasses import dataclass

from src.core.seasons.exceptions import SeasonNameAlreadyExistError, SeasonNotFoundError
from src.core.seasons.schemas import Season, Seasons
from src.core.storages import MissionStorage
from src.core.use_case import UseCase


@dataclass
class CreateSeasonUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, branch: Season) -> Season:
        try:
            await self.storage.get_season_by_name(name=branch.name)
            raise SeasonNameAlreadyExistError
        except SeasonNotFoundError:
            await self.storage.insert_season(season=branch)
            return await self.storage.get_season_by_name(name=branch.name)


@dataclass
class GetSeasonsUseCase(UseCase):
    storage: MissionStorage

    async def execute(self) -> Seasons:
        return await self.storage.list_seasons()


@dataclass
class GetSeasonDetailUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, branch_id: int) -> Season:
        return await self.storage.get_season_by_id(season_id=branch_id)


@dataclass
class UpdateSeasonUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, branch: Season) -> Season:
        await self.storage.get_season_by_id(season_id=branch.id)
        try:
            existing_branch = await self.storage.get_season_by_name(name=branch.name)
            if existing_branch.id != branch.id:
                raise SeasonNameAlreadyExistError
        except SeasonNotFoundError:
            pass
        await self.storage.update_season(branch=branch)
        return await self.storage.get_season_by_id(season_id=branch.id)


@dataclass
class DeleteSeasonUseCase(UseCase):
    storage: MissionStorage

    async def execute(self, branch_id: int) -> None:
        await self.storage.delete_season(season_id=branch_id)
