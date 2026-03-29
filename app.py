import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# ── Session state initialization ──────────────────────────────────────────────
if "owner" not in st.session_state:
    st.session_state.owner = None

# ── Section 1: Owner setup ────────────────────────────────────────────────────
st.subheader("Owner Info")

col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Your name", value="Jordan")
with col2:
    available_minutes = st.number_input("Time available today (minutes)", min_value=10, max_value=480, value=90)

if st.button("Set owner"):
    st.session_state.owner = Owner(name=owner_name, available_minutes=available_minutes)
    st.success(f"Owner set: {owner_name} ({available_minutes} min available)")

if st.session_state.owner is None:
    st.info("Set your owner info above to get started.")
    st.stop()

owner: Owner = st.session_state.owner

st.divider()

# ── Section 2: Add a pet ──────────────────────────────────────────────────────
st.subheader("Add a Pet")

col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    new_pet = Pet(name=pet_name, species=species)
    owner.add_pet(new_pet)
    st.success(f"Added {pet_name} the {species}!")

if owner.pets:
    st.write("**Current pets:**", ", ".join(f"{p.name} ({p.species})" for p in owner.pets))

st.divider()

# ── Section 3: Add a task ─────────────────────────────────────────────────────
st.subheader("Add a Task")

if not owner.pets:
    st.info("Add a pet first before adding tasks.")
else:
    pet_names = [p.name for p in owner.pets]
    selected_pet_name = st.selectbox("Assign to pet", pet_names)
    selected_pet = next(p for p in owner.pets if p.name == selected_pet_name)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add task"):
        new_task = Task(title=task_title, duration_minutes=int(duration), priority=priority)
        selected_pet.add_task(new_task)
        st.success(f"Added '{task_title}' to {selected_pet_name}!")

    all_tasks = owner.get_all_tasks()
    if all_tasks:
        st.write("**Pending tasks:**")
        st.table([
            {"Pet": pet.name, "Task": task.title, "Duration (min)": task.duration_minutes, "Priority": task.priority}
            for task, pet in all_tasks
        ])

st.divider()

# ── Section 4: Generate schedule ─────────────────────────────────────────────
st.subheader("Generate Today's Schedule")

if st.button("Generate schedule"):
    if not owner.pets or not owner.get_all_tasks():
        st.warning("Add at least one pet and one task first.")
    else:
        scheduler = Scheduler(owner=owner)
        plan = scheduler.generate_plan()

        included = [s for s in plan if "included" in s.explanation]
        skipped = [s for s in plan if "skipped" in s.explanation]

        st.markdown("### Today's Plan")
        for i, scheduled in enumerate(included, 1):
            st.markdown(f"**{i}. {scheduled.task.title}** — [{scheduled.pet.name}] · {scheduled.task.duration_minutes} min · `{scheduled.task.priority}` priority")
            st.caption(scheduled.explanation)

        if skipped:
            st.markdown("### Skipped")
            for scheduled in skipped:
                st.markdown(f"- ~~{scheduled.task.title}~~ [{scheduled.pet.name}]")
                st.caption(scheduled.explanation)

        total = sum(s.task.duration_minutes for s in included)
        st.info(f"Total scheduled: {total} min / {owner.available_minutes} min available")
