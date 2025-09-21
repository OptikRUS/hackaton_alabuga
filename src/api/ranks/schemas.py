from pydantic import Field

from src.api.boundary import BoundaryModel
from src.core.ranks.schemas import Rank, Ranks


class RankCreateRequest(BoundaryModel):
    name: str = Field(default=..., description="Название ранга")
    required_xp: int = Field(default=..., ge=0, description="Необходимый опыт")

    def to_schema(self) -> Rank:
        return Rank(id=0, name=self.name, required_xp=self.required_xp)


class RankUpdateRequest(BoundaryModel):
    name: str = Field(default=..., description="Название ранга")
    required_xp: int = Field(default=..., ge=0, description="Необходимый опыт")

    def to_schema(self, rank_id: int) -> Rank:
        return Rank(id=rank_id, name=self.name, required_xp=self.required_xp)


class RankResponse(BoundaryModel):
    id: int = Field(default=..., description="Идентификатор ранга")
    name: str = Field(default=..., description="Название ранга")
    required_xp: int = Field(default=..., description="Необходимый опыт")

    @classmethod
    def from_schema(cls, rank: Rank) -> "RankResponse":
        return cls(id=rank.id, name=rank.name, required_xp=rank.required_xp)


class RanksResponse(BoundaryModel):
    values: list[RankResponse]

    @classmethod
    def from_schema(cls, ranks: Ranks) -> "RanksResponse":
        return cls(values=[RankResponse.from_schema(rank=r) for r in ranks.values])



