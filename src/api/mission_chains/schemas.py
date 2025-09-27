from pydantic import Field

from src.api.boundary import BoundaryModel
from src.api.missions.schemas import MissionDependencyResponse, MissionResponse
from src.core.mission_chains.schemas import MissionChain, MissionChains


class MissionChainCreateRequest(BoundaryModel):
    name: str = Field(default=..., description="Название цепочки миссий")
    description: str = Field(default=..., description="Описание цепочки миссий")
    reward_xp: int = Field(default=..., ge=0, description="Награда в опыте за цепочку")
    reward_mana: int = Field(default=..., ge=0, description="Награда в мане за цепочку")

    def to_schema(self) -> MissionChain:
        return MissionChain(
            id=0,
            name=self.name,
            description=self.description,
            reward_xp=self.reward_xp,
            reward_mana=self.reward_mana,
        )


class MissionChainUpdateRequest(BoundaryModel):
    name: str = Field(default=..., description="Название цепочки миссий")
    description: str = Field(default=..., description="Описание цепочки миссий")
    reward_xp: int = Field(default=..., ge=0, description="Награда в опыте за цепочку")
    reward_mana: int = Field(default=..., ge=0, description="Награда в мане за цепочку")

    def to_schema(self, chain_id: int) -> MissionChain:
        return MissionChain(
            id=chain_id,
            name=self.name,
            description=self.description,
            reward_xp=self.reward_xp,
            reward_mana=self.reward_mana,
        )


class MissionChainResponse(BoundaryModel):
    id: int = Field(default=..., description="Идентификатор цепочки миссий")
    name: str = Field(default=..., description="Название цепочки миссий")
    description: str = Field(default=..., description="Описание цепочки миссий")
    reward_xp: int = Field(default=..., description="Награда в опыте за цепочку")
    reward_mana: int = Field(default=..., description="Награда в мане за цепочку")
    missions: list[MissionResponse] = Field(default_factory=list, description="Миссии в цепочке")
    dependencies: list[MissionDependencyResponse] = Field(
        default_factory=list, description="Зависимости между миссиями в цепочке"
    )

    @classmethod
    def from_schema(cls, mission_chain: MissionChain) -> "MissionChainResponse":
        return cls(
            id=mission_chain.id,
            name=mission_chain.name,
            description=mission_chain.description,
            reward_xp=mission_chain.reward_xp,
            reward_mana=mission_chain.reward_mana,
            missions=[
                MissionResponse.from_schema(mission=mission)
                for mission in (mission_chain.missions or [])
            ],
            dependencies=[
                MissionDependencyResponse.from_schema(dep)
                for dep in (mission_chain.dependencies or [])
            ],
        )


class MissionChainsResponse(BoundaryModel):
    values: list[MissionChainResponse]

    @classmethod
    def from_schema(cls, mission_chains: MissionChains) -> "MissionChainsResponse":
        return cls(
            values=[
                MissionChainResponse.from_schema(mission_chain=mission_chain)
                for mission_chain in mission_chains.values
            ]
        )
