from pawpal_system import Owner, Pet, Task, Scheduler

# Create owner
jordan = Owner(name="Jordan", available_minutes=90)

# Create pets
mochi = Pet(name="Mochi", species="dog")
luna = Pet(name="Luna", species="cat")

# Add tasks to Mochi
mochi.add_task(Task(title="Morning walk", duration_minutes=30, priority="high"))
mochi.add_task(Task(title="Brush coat", duration_minutes=15, priority="medium"))

# Add tasks to Luna
luna.add_task(Task(title="Feeding", duration_minutes=10, priority="high"))
luna.add_task(Task(title="Playtime", duration_minutes=20, priority="low"))
luna.add_task(Task(title="Medication", duration_minutes=5, priority="high"))

# Register pets with owner
jordan.add_pet(mochi)
jordan.add_pet(luna)

# Generate plan
scheduler = Scheduler(owner=jordan)
plan = scheduler.generate_plan()

# Print schedule
print("=" * 50)
print(f"  Today's Schedule for {jordan.name}'s pets")
print("=" * 50)

included = [s for s in plan if s.task.duration_minutes <= jordan.available_minutes and "included" in s.explanation]
skipped = [s for s in plan if "skipped" in s.explanation]

print("\nPlanned tasks:")
for i, scheduled in enumerate(included, 1):
    print(f"  {i}. {scheduled.task.title} [{scheduled.pet.name}] — {scheduled.task.duration_minutes} min ({scheduled.task.priority} priority)")

if skipped:
    print("\nSkipped tasks (not enough time):")
    for scheduled in skipped:
        print(f"  - {scheduled.task.title} [{scheduled.pet.name}] — {scheduled.task.duration_minutes} min needed")

total = sum(s.task.duration_minutes for s in included)
print(f"\nTotal time: {total} min / {jordan.available_minutes} min available")
print("=" * 50)
