from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date

# Create owner
jordan = Owner(name="Jordan", available_minutes=90)

# Create pets
mochi = Pet(name="Mochi", species="dog")
luna = Pet(name="Luna", species="cat")

# Add tasks OUT OF ORDER (time_of_day intentionally scrambled)
mochi.add_task(Task(title="Evening walk",    duration_minutes=30, priority="high",   time_of_day="17:00"))
mochi.add_task(Task(title="Brush coat",      duration_minutes=15, priority="medium", time_of_day="09:30"))
mochi.add_task(Task(title="Morning walk",    duration_minutes=30, priority="high",   time_of_day="07:00"))

luna.add_task(Task(title="Playtime",         duration_minutes=20, priority="low",    time_of_day="15:00"))
luna.add_task(Task(title="Medication",       duration_minutes=5,  priority="high",   time_of_day="08:00"))
luna.add_task(Task(title="Feeding",          duration_minutes=10, priority="high",   time_of_day="07:30"))

# Mark one task complete to demo filter_by_status
luna.tasks[0].mark_complete()  # Playtime marked done

jordan.add_pet(mochi)
jordan.add_pet(luna)

scheduler = Scheduler(owner=jordan)
all_tasks = jordan.get_all_tasks()

# ── Demo 1: Sort by time_of_day ───────────────────────────────────────────────
print("=" * 50)
print("  Tasks sorted by time of day")
print("=" * 50)
sorted_tasks = scheduler.sort_by_time(all_tasks)
for task, pet in sorted_tasks:
    time_label = task.time_of_day if task.time_of_day else "anytime"
    print(f"  {time_label}  {task.title} [{pet.name}] ({task.priority})")

# ── Demo 2: Filter by pet ─────────────────────────────────────────────────────
print("\n" + "=" * 50)
print("  Mochi's tasks only")
print("=" * 50)
mochi_tasks = scheduler.filter_by_pet(all_tasks, "Mochi")
for task, pet in mochi_tasks:
    print(f"  - {task.title} ({task.duration_minutes} min, {task.priority})")

# ── Demo 3: Filter by status ──────────────────────────────────────────────────
print("\n" + "=" * 50)
print("  Pending tasks (not completed)")
print("=" * 50)
pending = scheduler.filter_by_status(jordan.get_all_tasks(), completed=False)
for task, pet in pending:
    print(f"  - {task.title} [{pet.name}]")

# ── Demo 4: Generate schedule (priority + duration tiebreaker) ────────────────
print("\n" + "=" * 50)
print(f"  Today's Schedule for {jordan.name}'s pets")
print("=" * 50)
plan = scheduler.generate_plan()
included = [s for s in plan if "included" in s.explanation]
skipped  = [s for s in plan if "skipped"  in s.explanation]

print("\nPlanned tasks:")
for i, s in enumerate(included, 1):
    print(f"  {i}. {s.task.title} [{s.pet.name}] — {s.task.duration_minutes} min ({s.task.priority})")

if skipped:
    print("\nSkipped:")
    for s in skipped:
        print(f"  - {s.task.title} [{s.pet.name}] — {s.task.duration_minutes} min needed")

total = sum(s.task.duration_minutes for s in included)
print(f"\nTotal: {total} min / {jordan.available_minutes} min available")
print("=" * 50)

# ── Demo 5: Conflict detection ───────────────────────────────────────────────
print("\n" + "=" * 50)
print("  Conflict Detection Demo")
print("=" * 50)
# Add two tasks at the same time_of_day
mochi.add_task(Task(title="Vet checkup", duration_minutes=60, priority="high", time_of_day="07:00"))
luna.add_task(Task(title="Nail trim",    duration_minutes=10, priority="medium", time_of_day="09:30"))

conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  ⚠  {warning}")
else:
    print("  No conflicts detected.")

# ── Demo 7: Recurring task auto-scheduling ────────────────────────────────────
print("\n" + "=" * 50)
print("  Recurring Task Demo")
print("=" * 50)
feeding = luna.tasks[2]  # Feeding — frequency="daily"
print(f"Completing '{feeding.title}' (frequency: {feeding.frequency}, due: {date.today()})")
next_task = luna.complete_task(feeding)
if next_task:
    print(f"  → Next occurrence auto-created: '{next_task.title}' due {next_task.due_date}")
else:
    print("  → No recurrence (as-needed task)")
