# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## ✨ Features

PawPal+ lets one owner manage several pets and their care tasks, then builds a daily plan that respects the owner's available time and each task's priority.

**Managing pets and tasks**

- Add one or more pets (name, species, age) under a single owner.
- Add care tasks to a pet with a description, time, duration (minutes), priority (low/medium/high), and frequency (once/daily/weekly).
- Mark tasks complete (and reset them back to incomplete).

**Scheduling algorithms** (all in the `Scheduler` class)

- **Sort tasks by time** — `sort_by_time()` returns the tasks in chronological order, so the schedule reads top-to-bottom by start time.
- **Filter tasks** — `filter_by_pet(name)` returns only one pet's tasks, and `filter_by_status(completed)` returns only completed or only incomplete tasks.
- **Recurring daily/weekly tasks** — completing a task with `mark_task_complete()` automatically creates the next occurrence on the same pet: one day later for daily tasks, seven days later for weekly. One-time (`once`) tasks do not recur.
- **Conflict warnings** — `detect_conflicts()` returns readable warning messages when two or more tasks (across any pets) are scheduled at the exact same start time. It warns instead of crashing. (This is a lightweight check: it compares start times only, not overlapping durations.)
- **Available-hours scheduling** — the owner sets how many hours they have today, and `generate_schedule()` fits tasks into that time, choosing higher-priority tasks first (ties broken by earlier start time). It is a simple greedy approach, not a guaranteed-optimal packing.
- **Skipped tasks** — any tasks that do not fit in the available time are returned in a separate "skipped" list instead of the schedule, and `explain_plan()` summarizes which tasks were included or skipped and why.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:
Today's Schedule for Jordan
========================================
07:30  |  Mochi   |  Feed breakfast (10 min, high priority)
08:00  |  Rex     |  Morning walk (30 min, high priority)
12:00  |  Mochi   |  Give medication (5 min, medium priority)
========================================
3 task(s) planned.

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

The Scheduler class gathers tasks live from the owner's pets (single source of truth) and adds the logic below.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | Scheduler.sort_by_time() | Returns a new list sorted chronologically by each task's scheduled_time, using Python's sorted() with a lambda key. |
| Filtering | Scheduler.filter_by_pet(pet_name), Scheduler.filter_by_status(completed) | Filter tasks across all pets by pet name or by completion status (True/False). Each returns a new list. |
| Conflict handling | Scheduler.detect_conflicts() | Groups tasks by start time and returns readable warning strings (not exceptions) when 2 or more tasks share the same time. Lightweight: exact start-time match only, not duration overlap. |
| Recurring tasks | Scheduler.mark_task_complete(task) | Marks a task done and auto-creates the next occurrence on the same pet — due_date + 1 day (daily) or + 7 days (weekly) via timedelta. ONCE tasks do not recur. |
| Available-hours scheduling | Scheduler.generate_schedule() | Converts the owner's available_hours to minutes, picks higher-priority tasks first (ties broken by earlier time), includes the tasks that fit, and returns (scheduled, skipped). Greedy, not guaranteed-optimal. |
| Skipped tasks + explanation | Scheduler.explain_plan(scheduled, skipped) | Lists which tasks were included or skipped and why. In the UI, skipped tasks appear in a separate warning-colored section. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Add a pet (name, species, age) in the "Add a Pet" section — a success message confirms it and it appears in the pet table.
2. Schedule a task for that pet (title, time, duration, priority, frequency) in the "Schedule a Task" section.
3. Set "Hours available today," then click "Generate schedule" to see today's plan in sorted time order.
4. If two tasks share the same time, a conflict warning appears near the schedule.
5. If tasks don't fit your available hours, lower-priority ones are skipped into a separate warning section.

**Sample CLI output** (`python main.py`):

```text
Today's Schedule (sorted by time)
========================================
07:30  |  Mochi   |  Feed breakfast (10 min, high priority) [done]
08:00  |  Mochi   |  Playtime (15 min, low priority) [todo]
08:00  |  Rex     |  Morning walk (30 min, high priority) [todo]
12:00  |  Mochi   |  Give medication (5 min, medium priority) [todo]
========================================

Conflict check
========================================
WARNING: Conflict at 08:00: Playtime (Mochi), Morning walk (Rex)
========================================

Limited availability demo (Sam has 0.75 h = 45 min today)
Scheduled (fits the available time)
  07:00  Long walk (high, 30 min)
  09:00  Vet meds (high, 10 min)
  18:00  Brush coat (medium, 5 min)
Skipped (not enough time)
  17:00  Fetch game (low, 20 min)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->


 "Testing PawPal+"
 python -m pytest
 The test suite covers the four scheduler algorithms, chronological sorting, daily and weekly recurrence, same-time conflict detection, and core task and pet behaviors like marking complete and adding tasks.
 ======================================================================= test session starts ========================================================================
platform darwin -- Python 3.13.13, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/jasonchen/Documents/PawPalProject/ai110-module2show-pawpal-starter
plugins: anyio-4.14.1
collected 7 items                                                                                                                                                  

tests/test_pawpal.py .......                                                                                                                                 [100%]

======================================================================== 7 passed in 0.02s =========================================================================
Confidence level 5


