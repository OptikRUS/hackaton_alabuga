from dataclasses import dataclass


@dataclass
class MissionTask:
    id: int
    title: str
    description: str


@dataclass
class MissionTasks:
    values: list[MissionTask]


@dataclass
class UserTask(MissionTask):
    is_completed: bool = False
