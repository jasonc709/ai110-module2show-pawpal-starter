"""PawPal+ CLI demo — builds a small owner/pet/task setup and prints today's schedule."""

from datetime import time

from pawpal_system import Owner, Pet, Task, Scheduler, Frequency


def main():
    """Set up sample data and print today's schedule to the terminal."""

    # 1. Create one owner.
    owner = Owner("Jordan")

    # 2. Create two pets.
    mochi = Pet("Mochi", "cat", 3)
    rex = Pet("Rex", "dog", 5)

    # 3. Add the pets to the owner.
    owner.add_pet(mochi)
    owner.add_pet(rex)

    # 4. Add a few tasks (with different times) to the pets.
    rex.add_task(
        Task("Morning walk", time(8, 0), 30, Frequency.DAILY, "high", pet_name="Rex")
    )
    mochi.add_task(
        Task("Feed breakfast", time(7, 30), 10, Frequency.DAILY, "high", pet_name="Mochi")
    )
    mochi.add_task(
        Task("Give medication", time(12, 0), 5, Frequency.DAILY, "medium", pet_name="Mochi")
    )

    # 5. Use the scheduler to gather and order today's tasks.
    scheduler = Scheduler(owner)
    schedule = scheduler.get_today_schedule()

    # 6. Print a clean, readable schedule.
    print(f"Today's Schedule for {owner.name}")
    print("=" * 40)
    for task in schedule:
        clock = task.scheduled_time.strftime("%H:%M")
        print(
            f"{clock}  |  {task.pet_name:<6}  |  {task.description} "
            f"({task.duration_minutes} min, {task.priority} priority)"
        )
    print("=" * 40)
    print(f"{len(schedule)} task(s) planned.")


if __name__ == "__main__":
    main()
