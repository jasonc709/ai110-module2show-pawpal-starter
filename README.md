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

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

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


