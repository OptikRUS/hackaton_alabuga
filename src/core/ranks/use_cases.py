from dataclasses import dataclass

from src.core.ranks.exceptions import (
    RankNameAlreadyExistError,
    RankNotFoundError,
)
from src.core.ranks.schemas import Rank, Ranks
from src.core.storages import RankStorage
from src.core.use_case import UseCase


@dataclass
class CreateRankUseCase(UseCase):
    storage: RankStorage

    async def execute(self, rank: Rank) -> Rank:
        try:
            await self.storage.get_rank_by_name(name=rank.name)
            raise RankNameAlreadyExistError
        except RankNotFoundError:
            await self.storage.insert_rank(rank=rank)
            return await self.storage.get_rank_by_name(name=rank.name)


@dataclass
class GetRanksUseCase(UseCase):
    storage: RankStorage

    async def execute(self) -> Ranks:
        return await self.storage.list_ranks()


@dataclass
class GetRankDetailUseCase(UseCase):
    storage: RankStorage

    async def execute(self, rank_id: int) -> Rank:
        return await self.storage.get_rank_by_id(rank_id=rank_id)


@dataclass
class UpdateRankUseCase(UseCase):
    storage: RankStorage

    async def execute(self, rank: Rank) -> Rank:
        try:
            existing = await self.storage.get_rank_by_name(name=rank.name)
            if existing.id != rank.id:
                raise RankNameAlreadyExistError
        except RankNotFoundError:
            pass
        await self.storage.update_rank(rank=rank)
        return await self.storage.get_rank_by_id(rank_id=rank.id)


@dataclass
class DeleteRankUseCase(UseCase):
    storage: RankStorage

    async def execute(self, rank_id: int) -> None:
        await self.storage.delete_rank(rank_id=rank_id)



