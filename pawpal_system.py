"""PawPal+ system classes — skeletons based on diagrams/uml.mmd."""

from dataclasses import dataclass, field
from datetime import date, time


@dataclass
class Task:
    """A single pet care activity (feeding, walk, medication, appointment)."""

    description: str
    scheduled_time: time
    duration_minutes: int
    frequency: str
    priority: str
    completed: bool = False

    def mark_done(self) -> None:
        """Mark this task as completed."""
        pass

    def is_high_priority(self) -> bool:
        """Return True if this task is high priority."""
        pass


@dataclass
class Pet:
    """A pet with basic info and its own list of care tasks."""

    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task for this pet."""
        pass

    def remove_task(self, task: Task) -> None:
        """Remove a care task from this pet."""
        pass

    def list_tasks(self) -> list[Task]:
        """Return this pet's care tasks."""
        pass


@dataclass
class Owner:
    """The person using the app, owning one or more pets."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        pass

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner."""
        pass

    def list_pets(self) -> list[Pet]:
        """Return this owner's pets."""
        pass


class Scheduler:
    """Organizes tasks across all pets into a sorted, conflict-aware schedule."""

    def __init__(self) -> None:
        """Initialize the scheduler with an empty task list."""
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler."""
        pass

    def build_schedule(self, day: date) -> list[Task]:
        """Build the ordered schedule of tasks for a given day."""
        pass

    def sort_by_time(self) -> list[Task]:
        """Return tasks sorted by scheduled time."""
        pass

    def view_today(self) -> list[Task]:
        """Return today's tasks in time order."""
        pass

    def detect_conflicts(self) -> list[Task]:
        """Return tasks that overlap or conflict in time."""
        pass

    def explain_plan(self) -> str:
        """Return a human-readable explanation of why tasks were chosen and ordered."""
        pass
