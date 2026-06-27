"""PawPal+ system classes — core implementation based on diagrams/uml.mmd."""

from dataclasses import dataclass, field
from datetime import date, time
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

    def build_schedule(self, day: date) -> list[Task]:
        """Build the ordered schedule of tasks for a given day (not implemented yet)."""
        pass

    def detect_conflicts(self) -> list[tuple[Task, Task]]:
        """Return pairs of tasks that overlap in time (not implemented yet)."""
        pass

    def explain_plan(self) -> str:
        """Return a human-readable explanation of the plan (not implemented yet)."""
        pass
