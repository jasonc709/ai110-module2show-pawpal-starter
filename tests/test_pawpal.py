"""Simple tests for the PawPal+ core classes."""

from datetime import date, time, timedelta

from pawpal_system import Owner, Pet, Task, Scheduler, Frequency


def test_mark_complete_changes_status():
    """mark_complete() should switch a task's completed status to True."""
    task = Task("Morning walk", time(8, 0), 30, Frequency.DAILY, "high")

    assert task.completed is False  # starts incomplete
    task.mark_complete()
    assert task.completed is True   # now marked done


def test_add_task_increases_pet_task_count():
    """Adding a task to a Pet should increase that pet's task count by one."""
    pet = Pet("Mochi", "cat", 3)

    assert len(pet.get_tasks()) == 0  # no tasks yet
    pet.add_task(Task("Feed breakfast", time(7, 30), 10, Frequency.DAILY, "high"))
    assert len(pet.get_tasks()) == 1  # one task after adding


def test_completing_daily_task_creates_next_occurrence():
    """Completing a DAILY task should add a new task due one day later."""
    owner = Owner("Jordan")
    pet = Pet("Mochi", "cat", 3)
    owner.add_pet(pet)
    task = Task(
        "Feed breakfast", time(7, 30), 10, Frequency.DAILY, "high",
        pet_name="Mochi", due_date=date(2026, 6, 27),
    )
    pet.add_task(task)
    scheduler = Scheduler(owner)

    next_task = scheduler.mark_task_complete(task)

    assert task.completed is True                       # original is done
    assert len(pet.get_tasks()) == 2                    # next occurrence added
    assert next_task.due_date == date(2026, 6, 28)      # one day later
    assert next_task.completed is False                 # the new one is fresh


def test_weekly_task_recurs_seven_days_later():
    """Completing a WEEKLY task should add a new task due seven days later."""
    owner = Owner("Jordan")
    pet = Pet("Rex", "dog", 5)
    owner.add_pet(pet)
    task = Task(
        "Bath", time(9, 0), 30, Frequency.WEEKLY, "medium",
        pet_name="Rex", due_date=date(2026, 6, 27),
    )
    pet.add_task(task)
    scheduler = Scheduler(owner)

    next_task = scheduler.mark_task_complete(task)

    assert next_task.due_date == date(2026, 6, 27) + timedelta(days=7)


def test_once_task_does_not_recur():
    """Completing a ONCE task should NOT create a new task."""
    owner = Owner("Jordan")
    pet = Pet("Mochi", "cat", 3)
    owner.add_pet(pet)
    task = Task("Vet visit", time(15, 0), 60, Frequency.ONCE, "high", pet_name="Mochi")
    pet.add_task(task)
    scheduler = Scheduler(owner)

    next_task = scheduler.mark_task_complete(task)

    assert task.completed is True            # still marked complete
    assert next_task is None                 # but nothing new returned
    assert len(pet.get_tasks()) == 1         # no extra task added


def test_sort_by_time_returns_chronological_order():
    """sort_by_time() should return tasks in time order even when added out of order."""
    owner = Owner("Jordan")
    pet = Pet("Mochi", "cat", 3)
    owner.add_pet(pet)

    # Added OUT OF ORDER on purpose: 12:00, then 7:30, then 9:15.
    pet.add_task(Task("Lunch", time(12, 0), 10, Frequency.DAILY, "medium", pet_name="Mochi"))
    pet.add_task(Task("Breakfast", time(7, 30), 10, Frequency.DAILY, "high", pet_name="Mochi"))
    pet.add_task(Task("Walk", time(9, 15), 20, Frequency.DAILY, "low", pet_name="Mochi"))
    scheduler = Scheduler(owner)

    ordered_times = [task.scheduled_time for task in scheduler.sort_by_time()]

    assert ordered_times == [time(7, 30), time(9, 15), time(12, 0)]  # chronological


def test_detect_conflicts_flags_same_time():
    """Two tasks at the same time (across pets) should produce at least one warning."""
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "cat", 3)
    rex = Pet("Rex", "dog", 5)
    owner.add_pet(mochi)
    owner.add_pet(rex)

    # Both scheduled at 08:00 -> a conflict.
    mochi.add_task(Task("Playtime", time(8, 0), 15, Frequency.DAILY, "low", pet_name="Mochi"))
    rex.add_task(Task("Morning walk", time(8, 0), 30, Frequency.DAILY, "high", pet_name="Rex"))
    scheduler = Scheduler(owner)

    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) >= 1  # at least one warning returned


def test_generate_schedule_respects_available_time():
    """Tasks beyond the available time are skipped, lower priority first."""
    owner = Owner("Jordan", available_hours=0.5)  # 0.5 h = 30 minutes
    pet = Pet("Mochi", "cat", 3)
    owner.add_pet(pet)

    # 20 (high) + 20 (low) = 40 min, which is more than the 30 available.
    pet.add_task(Task("Walk", time(8, 0), 20, Frequency.DAILY, "high", pet_name="Mochi"))
    pet.add_task(Task("Play", time(9, 0), 20, Frequency.DAILY, "low", pet_name="Mochi"))
    scheduler = Scheduler(owner)

    scheduled, skipped = scheduler.generate_schedule()

    scheduled_names = [t.description for t in scheduled]
    skipped_names = [t.description for t in skipped]

    assert "Walk" in scheduled_names                          # high priority fits
    assert "Play" in skipped_names                            # low priority doesn't
    assert sum(t.duration_minutes for t in scheduled) <= 30   # stays within budget
