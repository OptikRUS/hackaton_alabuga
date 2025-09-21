from dataclasses import dataclass

from src.core.competitions.exceptions import (
    CompetitionNameAlreadyExistError,
    CompetitionNotFoundError,
)
from src.core.competitions.schemas import Competition, Competitions
from src.core.storages import CompetitionStorage
from src.core.use_case import UseCase


@dataclass
class CreateCompetitionUseCase(UseCase):
    storage: CompetitionStorage

    async def execute(self, competition: Competition) -> Competition:
        try:
            await self.storage.get_competition_by_name(name=competition.name)
            raise CompetitionNameAlreadyExistError
        except CompetitionNotFoundError:
            await self.storage.insert_competition(competition=competition)
            return await self.storage.get_competition_by_name(name=competition.name)


@dataclass
class GetCompetitionsUseCase(UseCase):
    storage: CompetitionStorage

    async def execute(self) -> Competitions:
        return await self.storage.list_competitions()


@dataclass
class GetCompetitionDetailUseCase(UseCase):
    storage: CompetitionStorage

    async def execute(self, competition_id: int) -> Competition:
        return await self.storage.get_competition_by_id(competition_id=competition_id)


@dataclass
class UpdateCompetitionUseCase(UseCase):
    storage: CompetitionStorage

    async def execute(self, competition: Competition) -> Competition:
        try:
            existing = await self.storage.get_competition_by_name(name=competition.name)
            if existing.id != competition.id:
                raise CompetitionNameAlreadyExistError
        except CompetitionNotFoundError:
            pass
        await self.storage.update_competition(competition=competition)
        return await self.storage.get_competition_by_id(competition_id=competition.id)


@dataclass
class DeleteCompetitionUseCase(UseCase):
    storage: CompetitionStorage

    async def execute(self, competition_id: int) -> None:
        await self.storage.delete_competition(competition_id=competition_id)


