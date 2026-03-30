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

## Smarter Scheduling

The scheduler goes beyond a simple task list with four intelligent features:

- **Sorting by time** — tasks can be assigned an optional `time_of_day` (HH:MM) and sorted chronologically using a lambda key, so the plan reflects the actual flow of a pet owner's day.
- **Filtering** — tasks can be filtered by pet name or completion status, making it easy to view only what's relevant (e.g., "show me only Mochi's pending tasks").
- **Recurring tasks** — daily and weekly tasks auto-schedule their next occurrence when marked complete, using Python's `timedelta` to calculate the next due date. One-off (`as-needed`) tasks do not recur.
- **Conflict detection** — the scheduler warns when two tasks share the same `time_of_day` slot, returning human-readable messages instead of crashing.

## Testing PawPal+

Run the full test suite with:

```bash
python -m pytest
```

The suite contains 11 automated tests covering:

- **Task completion** — `mark_complete()` correctly flips the completed flag
- **Task addition** — `add_task()` grows the pet's task list
- **Sorting** — tasks are returned in chronological HH:MM order; untimed tasks fall last
- **Recurrence** — daily tasks create a next occurrence due tomorrow; weekly tasks due in 7 days; `as-needed` tasks do not recur
- **Conflict detection** — duplicate `time_of_day` slots produce a warning; distinct times produce none
- **Edge cases** — an owner with no pets returns an empty plan; a task exceeding the time budget is marked skipped

**Confidence level: ★★★★☆ (4/5)**
The core scheduling behaviors are well covered. The main gap is duration-overlap conflict detection (two tasks whose time windows overlap but don't share an exact start time), which is noted as a known tradeoff in the design.

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
