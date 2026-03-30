from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


# ── Existing tests ────────────────────────────────────────────────────────────

def test_mark_complete_changes_status():
    task = Task(title="Morning walk", duration_minutes=30, priority="high")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task(title="Feeding", duration_minutes=10, priority="high"))
    assert len(pet.tasks) == 1


# ── Sorting ───────────────────────────────────────────────────────────────────

def test_sort_by_time_returns_chronological_order():
    owner = Owner(name="Jordan", available_minutes=120)
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Evening walk", duration_minutes=30, priority="low",  time_of_day="17:00"))
    pet.add_task(Task(title="Medication",   duration_minutes=5,  priority="high", time_of_day="08:00"))
    pet.add_task(Task(title="Morning walk", duration_minutes=30, priority="high", time_of_day="07:00"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner=owner)
    sorted_tasks = scheduler.sort_by_time(owner.get_all_tasks())
    times = [task.time_of_day for task, _ in sorted_tasks]

    assert times == ["07:00", "08:00", "17:00"]


def test_sort_by_time_places_untimed_tasks_last():
    owner = Owner(name="Jordan", available_minutes=60)
    pet = Pet(name="Luna", species="cat")
    pet.add_task(Task(title="Playtime", duration_minutes=20, priority="low", time_of_day=""))
    pet.add_task(Task(title="Feeding",  duration_minutes=10, priority="high", time_of_day="07:30"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner=owner)
    sorted_tasks = scheduler.sort_by_time(owner.get_all_tasks())
    titles = [task.title for task, _ in sorted_tasks]

    assert titles[-1] == "Playtime"


# ── Recurrence ────────────────────────────────────────────────────────────────

def test_daily_task_creates_next_occurrence_on_completion():
    pet = Pet(name="Mochi", species="dog")
    task = Task(title="Feeding", duration_minutes=10, priority="high", frequency="daily")
    pet.add_task(task)

    next_task = pet.complete_task(task)

    assert next_task is not None
    assert next_task.title == "Feeding"
    assert next_task.due_date == date.today() + timedelta(days=1)
    assert next_task.completed is False


def test_weekly_task_creates_next_occurrence_seven_days_out():
    pet = Pet(name="Mochi", species="dog")
    task = Task(title="Bath time", duration_minutes=20, priority="medium", frequency="weekly")
    pet.add_task(task)

    next_task = pet.complete_task(task)

    assert next_task is not None
    assert next_task.due_date == date.today() + timedelta(weeks=1)


def test_as_needed_task_does_not_recur():
    pet = Pet(name="Luna", species="cat")
    task = Task(title="Vet visit", duration_minutes=60, priority="high", frequency="as-needed")
    pet.add_task(task)

    next_task = pet.complete_task(task)

    assert next_task is None


# ── Conflict detection ────────────────────────────────────────────────────────

def test_detect_conflicts_flags_duplicate_times():
    owner = Owner(name="Jordan", available_minutes=120)
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Morning walk", duration_minutes=30, priority="high",   time_of_day="08:00"))
    pet.add_task(Task(title="Medication",   duration_minutes=5,  priority="high",   time_of_day="08:00"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner=owner)
    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "08:00" in warnings[0]


def test_detect_conflicts_returns_empty_when_no_conflicts():
    owner = Owner(name="Jordan", available_minutes=120)
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Morning walk", duration_minutes=30, priority="high", time_of_day="07:00"))
    pet.add_task(Task(title="Medication",   duration_minutes=5,  priority="high", time_of_day="08:00"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner=owner)
    warnings = scheduler.detect_conflicts()

    assert warnings == []


# ── Edge cases ────────────────────────────────────────────────────────────────

def test_generate_plan_with_no_pets_returns_empty():
    owner = Owner(name="Jordan", available_minutes=60)
    scheduler = Scheduler(owner=owner)
    assert scheduler.generate_plan() == []


def test_generate_plan_skips_task_exceeding_available_time():
    owner = Owner(name="Jordan", available_minutes=10)
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Long walk", duration_minutes=60, priority="high"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner=owner)
    plan = scheduler.generate_plan()

    assert len(plan) == 1
    assert "skipped" in plan[0].explanation
