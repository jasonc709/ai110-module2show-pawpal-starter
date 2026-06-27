"""PawPal+ CLI demo — builds a small owner/pet/task setup and shows scheduling."""

from datetime import time

from pawpal_system import Owner, Pet, Task, Scheduler, Frequency


def print_tasks(title, tasks):
    """Print a titled, readable list of tasks (one per line)."""
    print(title)
    print("=" * 40)
    if not tasks:
        print("(none)")
    for task in tasks:
        clock = task.scheduled_time.strftime("%H:%M")
        status = "done" if task.completed else "todo"
        print(
            f"{clock}  |  {task.pet_name:<6}  |  {task.description} "
            f"({task.duration_minutes} min, {task.priority} priority) [{status}]"
        )
    print("=" * 40)
    print()


def main():
    """Set up sample data and demonstrate sorting and filtering."""

    # 1. Create one owner.
    owner = Owner("Jordan")

    # 2. Create two pets and add them to the owner.
    mochi = Pet("Mochi", "cat", 3)
    rex = Pet("Rex", "dog", 5)
    owner.add_pet(mochi)
    owner.add_pet(rex)

    # 3. Add tasks OUT OF ORDER (8:00 added before 7:30) to show sorting works.
    rex.add_task(
        Task("Morning walk", time(8, 0), 30, Frequency.DAILY, "high", pet_name="Rex")
    )
    mochi.add_task(
        Task("Feed breakfast", time(7, 30), 10, Frequency.DAILY, "high", pet_name="Mochi")
    )
    mochi.add_task(
        Task("Give medication", time(12, 0), 5, Frequency.DAILY, "medium", pet_name="Mochi")
    )
    # Intentionally clashes with Rex's 08:00 walk to show conflict detection.
    mochi.add_task(
        Task("Playtime", time(8, 0), 15, Frequency.DAILY, "low", pet_name="Mochi")
    )

    # 4. Mark one task complete so the status filter has something to show.
    mochi.get_tasks()[0].mark_complete()  # Feed breakfast -> done

    scheduler = Scheduler(owner)

    # Sorted schedule (tasks come back in time order despite being added out of order).
    print_tasks("Today's Schedule (sorted by time)", scheduler.sort_by_time())

    # Filter by pet name.
    print_tasks("Filtered by pet: Mochi", scheduler.filter_by_pet("Mochi"))

    # Filter by completion status.
    print_tasks("Filtered by status: completed", scheduler.filter_by_status(True))
    print_tasks("Filtered by status: incomplete", scheduler.filter_by_status(False))

    # Conflict detection: warn (don't crash) when tasks share the same time.
    print("Conflict check")
    print("=" * 40)
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print(f"WARNING: {warning}")
    else:
        print("No conflicts found.")
    print("=" * 40)
    print()

    # Recurring tasks: completing a daily task auto-creates the next occurrence.
    medication = mochi.get_tasks()[1]  # "Give medication", a DAILY task
    print(f"Mochi has {len(mochi.get_tasks())} tasks before completing medication.")
    next_task = scheduler.mark_task_complete(medication)
    print(f"Mochi has {len(mochi.get_tasks())} tasks after completing it.")
    if next_task:
        print(
            f"Next occurrence created: '{next_task.description}' "
            f"due {next_task.due_date} (was due {medication.due_date})."
        )
    print()


if __name__ == "__main__":
    main()
