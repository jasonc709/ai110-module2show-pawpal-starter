import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler, Frequency

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Streamlit re-runs this whole script on every interaction. st.session_state
# persists data across those reruns, so the Owner isn't recreated (and emptied)
# each time the page reruns.
if "owner" not in st.session_state:
    st.session_state["owner"] = Owner("Jordan")

owner = st.session_state["owner"]

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Add a Pet")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
age = st.number_input("Age", min_value=0, max_value=50, value=3)

if st.button("Add pet"):
    # Build a real Pet object and store it through the Owner.
    new_pet = Pet(pet_name, species, int(age))
    owner.add_pet(new_pet)
    st.success(f"Added {new_pet.name} the {new_pet.species}!")

# Show the owner's current pets.
if owner.pets:
    st.write("Current pets:")
    st.table(
        [{"name": p.name, "species": p.species, "age": p.age} for p in owner.pets]
    )
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Schedule a Task")

if not owner.pets:
    st.info("Add a pet first, then you can schedule tasks for it.")
else:
    # Choose which pet the task is for (selectbox returns the pet's position).
    pet_index = st.selectbox(
        "For which pet?",
        range(len(owner.pets)),
        format_func=lambda i: f"{owner.pets[i].name} ({owner.pets[i].species})",
    )

    task_title = st.text_input("Task title", value="Morning walk")
    col1, col2 = st.columns(2)
    with col1:
        task_time = st.time_input("Time")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col2:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        frequency = st.selectbox("Frequency", list(Frequency), format_func=lambda f: f.value)

    if st.button("Add task"):
        # Find the selected pet, build a real Task, and add it to that pet.
        selected_pet = owner.pets[pet_index]
        new_task = Task(
            task_title,
            task_time,
            int(duration),
            frequency,
            priority,
            pet_name=selected_pet.name,
        )
        selected_pet.add_task(new_task)
        st.success(f"Added '{new_task.description}' for {selected_pet.name}!")

st.divider()

st.subheader("Today's Schedule")
st.caption("Gathers every pet's tasks through the Scheduler and sorts them by time.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    schedule = scheduler.get_today_schedule()
    if schedule:
        st.table(
            [
                {
                    "time": t.scheduled_time.strftime("%H:%M"),
                    "pet": t.pet_name,
                    "task": t.description,
                    "duration (min)": t.duration_minutes,
                    "priority": t.priority,
                }
                for t in schedule
            ]
        )
    else:
        st.info("No tasks scheduled yet. Add some tasks above.")
