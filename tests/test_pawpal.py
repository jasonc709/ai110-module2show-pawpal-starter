"""Simple tests for the PawPal+ core classes."""

from datetime import time

from pawpal_system import Pet, Task, Frequency


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
