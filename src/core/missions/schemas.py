from dataclasses import dataclass


@dataclass
class MissionBranch:
    id: int
    name: str


@dataclass
class MissionBranches:
    values: list[MissionBranch]
