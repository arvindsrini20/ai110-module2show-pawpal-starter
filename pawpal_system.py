from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str          # "low", "medium", or "high"
    frequency: str = "daily"   # "daily", "weekly", "as-needed"
    completed: bool = False
    time_of_day: str = ""        # optional preferred start time in "HH:MM" format
    due_date: date | None = None  # date this task is next due

    def priority_value(self) -> int:
        """Return a numeric priority (1=low, 2=medium, 3=high) for sorting."""
        return {"low": 1, "medium": 2, "high": 3}.get(self.priority.lower(), 0)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def next_occurrence(self) -> "Task | None":
        """Return a new Task for the next occurrence based on frequency, or None if non-recurring."""
        today = date.today()
        if self.frequency == "daily":
            next_due = today + timedelta(days=1)
        elif self.frequency == "weekly":
            next_due = today + timedelta(weeks=1)
        else:
            return None  # "as-needed" tasks don't recur automatically
        return Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            frequency=self.frequency,
            time_of_day=self.time_of_day,
            due_date=next_due,
        )


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

    def complete_task(self, task: Task) -> Task | None:
        """Mark a task complete and auto-schedule the next occurrence if recurring."""
        task.mark_complete()
        next_task = task.next_occurrence()
        if next_task:
            self.add_task(next_task)
        return next_task


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

    def sort_by_time(self, tasks: list[tuple["Task", "Pet"]]) -> list[tuple["Task", "Pet"]]:
        """Sort tasks by preferred time_of_day (HH:MM), with unscheduled tasks last."""
        return sorted(tasks, key=lambda pair: pair[0].time_of_day if pair[0].time_of_day else "99:99")

    def filter_by_pet(self, tasks: list[tuple["Task", "Pet"]], pet_name: str) -> list[tuple["Task", "Pet"]]:
        """Return only tasks belonging to the named pet."""
        return [pair for pair in tasks if pair[1].name.lower() == pet_name.lower()]

    def filter_by_status(self, tasks: list[tuple["Task", "Pet"]], completed: bool) -> list[tuple["Task", "Pet"]]:
        """Return only tasks matching the given completion status."""
        return [pair for pair in tasks if pair[0].completed == completed]

    def detect_conflicts(self) -> list[str]:
        """Return warning messages for tasks scheduled at the same time_of_day."""
        warnings = []
        seen: dict[str, tuple[str, str]] = {}  # time_of_day -> (task title, pet name)
        for task, pet in self.owner.get_all_tasks():
            if not task.time_of_day:
                continue
            if task.time_of_day in seen:
                prev_title, prev_pet = seen[task.time_of_day]
                warnings.append(
                    f"Conflict at {task.time_of_day}: '{prev_title}' [{prev_pet}] "
                    f"and '{task.title}' [{pet.name}] overlap."
                )
            else:
                seen[task.time_of_day] = (task.title, pet.name)
        return warnings

    def generate_plan(self) -> list[ScheduledTask]:
        """Build a prioritized daily plan that fits within the owner's available time."""
        all_tasks = self.owner.get_all_tasks()
        sorted_tasks = sorted(all_tasks, key=lambda pair: (pair[0].priority_value(), -pair[0].duration_minutes), reverse=True)

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
