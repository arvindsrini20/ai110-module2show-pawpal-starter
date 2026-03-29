from dataclasses import dataclass, field


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str          # "low", "medium", or "high"
    frequency: str = "daily"   # "daily", "weekly", "as-needed"
    completed: bool = False

    def priority_value(self) -> int:
        """Return a numeric priority (1=low, 2=medium, 3=high) for sorting."""
        return {"low": 1, "medium": 2, "high": 3}.get(self.priority.lower(), 0)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_pending_tasks(self) -> list[Task]:
        """Return only tasks that have not been completed."""
        return [t for t in self.tasks if not t.completed]


@dataclass
class Owner:
    name: str
    available_minutes: int
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[tuple[Task, Pet]]:
        """Return all pending tasks across all pets, paired with their pet."""
        result = []
        for pet in self.pets:
            for task in pet.get_pending_tasks():
                result.append((task, pet))
        return result


@dataclass
class ScheduledTask:
    task: Task
    pet: Pet
    explanation: str

    def format_summary(self) -> str:
        """Return a human-readable summary of this scheduled task."""
        return (
            f"[{self.pet.name}] {self.task.title} "
            f"({self.task.duration_minutes} min, {self.task.priority} priority) — "
            f"{self.explanation}"
        )


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def generate_plan(self) -> list[ScheduledTask]:
        """Build a prioritized daily plan that fits within the owner's available time."""
        all_tasks = self.owner.get_all_tasks()
        sorted_tasks = sorted(all_tasks, key=lambda pair: pair[0].priority_value(), reverse=True)

        plan = []
        time_remaining = self.owner.available_minutes

        for task, pet in sorted_tasks:
            if task.duration_minutes <= time_remaining:
                explanation = (
                    f"included because priority is '{task.priority}' and "
                    f"{task.duration_minutes} min fits within remaining time "
                    f"({time_remaining} min left)"
                )
                plan.append(ScheduledTask(task, pet, explanation))
                time_remaining -= task.duration_minutes
            else:
                explanation = (
                    f"skipped — {task.duration_minutes} min needed but only "
                    f"{time_remaining} min remaining"
                )
                plan.append(ScheduledTask(task, pet, explanation))

        return plan
