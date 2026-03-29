from dataclasses import dataclass


@dataclass
class Owner:
    name: str
    available_minutes: int


@dataclass
class Pet:
    name: str
    species: str


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", or "high"

    def priority_value(self) -> int:
        pass


@dataclass
class ScheduledTask:
    task: Task
    explanation: str

    def format_summary(self) -> str:
        pass


class Scheduler:
    def __init__(self, tasks: list[Task], owner: Owner):
        self.tasks = tasks
        self.owner = owner

    def generate_plan(self) -> list[ScheduledTask]:
        pass
