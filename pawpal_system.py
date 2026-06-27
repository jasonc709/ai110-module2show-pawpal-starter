"""PawPal+ system classes — core implementation based on diagrams/uml.mmd."""

from dataclasses import dataclass, field
from datetime import date, time, timedelta
from enum import Enum
from itertools import count

# Auto-incrementing id generators so tasks/pets can be told apart even when
# their other fields are identical.
_task_ids = count(1)
_pet_ids = count(1)


class Frequency(Enum):
    """Fixed set of allowed recurrence values for a task (avoids parsing free text)."""

    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"


@dataclass
class Task:
    """A single pet care activity (feeding, walk, medication, appointment)."""

    description: str
    scheduled_time: time
    duration_minutes: int
    frequency: Frequency
    priority: str
    pet_name: str = ""
    due_date: date = field(default_factory=date.today)
    completed: bool = False
    id: int = field(default_factory=lambda: next(_task_ids))

    def mark_complete(self) -> None:
        """Set this task's completed status to True."""
        self.completed = True

    def reset(self) -> None:
        """Set this task's completed status back to False."""
        self.completed = False

    def is_high_priority(self) -> bool:
        """Return True if this task's priority is 'high'."""
        return self.priority == "high"


@dataclass
class Pet:
    """A pet with basic info and its own list of care tasks."""

    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)
    id: int = field(default_factory=lambda: next(_pet_ids))

    def add_task(self, task: Task) -> None:
        """Add a care task for this pet."""
        self.tasks.append(task)

    def remove_task(self, task_id: int) -> None:
        """Remove this pet's task matching the given id."""
        self.tasks = [task for task in self.tasks if task.id != task_id]

    def get_tasks(self) -> list[Task]:
        """Return this pet's care tasks."""
        return self.tasks


@dataclass
class Owner:
    """The person using the app, owning one or more pets."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet_id: int) -> None:
        """Remove the pet matching the given id."""
        self.pets = [pet for pet in self.pets if pet.id != pet_id]

    def get_all_tasks(self) -> list[Task]:
        """Return every task gathered from all of this owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """Organizes tasks across all of an owner's pets into a sorted schedule."""

    def __init__(self, owner: Owner) -> None:
        """Initialize the scheduler for an owner (the single source of task data)."""
        self.owner = owner

    def collect_tasks(self) -> list[Task]:
        """Gather every task across the owner's pets into one list."""
        return self.owner.get_all_tasks()

    def sort_by_time(self) -> list[Task]:
        """Return all tasks sorted by their scheduled time."""
        return sorted(self.collect_tasks(), key=lambda task: task.scheduled_time)

    def get_today_schedule(self) -> list[Task]:
        """Return today's tasks in time order."""
        return self.sort_by_time()

    def filter_by_pet(self, pet_name: str) -> list[Task]:
        """Return only tasks belonging to the pet with the given name."""
        return [task for task in self.collect_tasks() if task.pet_name == pet_name]

    def filter_by_status(self, completed: bool) -> list[Task]:
        """Return only tasks matching the given completion status."""
        return [task for task in self.collect_tasks() if task.completed == completed]

    def mark_task_complete(self, task: Task) -> Task | None:
        """Mark a task complete; if it recurs, add the next occurrence to its pet."""
        task.mark_complete()
        if task.frequency == Frequency.ONCE:
            return None  # one-time tasks never recur
        for pet in self.owner.pets:  # find the pet that owns this task
            if task in pet.get_tasks():
                if task.frequency == Frequency.DAILY:
                    next_date = task.due_date + timedelta(days=1)
                else:  # WEEKLY
                    next_date = task.due_date + timedelta(days=7)
                next_task = Task(
                    task.description,
                    task.scheduled_time,
                    task.duration_minutes,
                    task.frequency,
                    task.priority,
                    pet_name=task.pet_name,
                    due_date=next_date,
                )
                pet.add_task(next_task)
                return next_task
        return None

    def build_schedule(self, day: date) -> list[Task]:
        """Build the ordered schedule of tasks for a given day (not implemented yet)."""
        pass

    def detect_conflicts(self) -> list[str]:
        """Return warning strings for tasks (across all pets) that share the same time."""
        warnings = []
        by_time = {}  # group tasks by their scheduled time
        for task in self.collect_tasks():
            by_time.setdefault(task.scheduled_time, []).append(task)
        for scheduled_time, group in by_time.items():
            if len(group) > 1:  # two or more tasks at the same time = conflict
                clock = scheduled_time.strftime("%H:%M")
                labels = ", ".join(f"{t.description} ({t.pet_name})" for t in group)
                warnings.append(f"Conflict at {clock}: {labels}")
        return warnings

    def explain_plan(self) -> str:
        """Return a human-readable explanation of the plan (not implemented yet)."""
        pass
