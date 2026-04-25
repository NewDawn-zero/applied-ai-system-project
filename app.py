from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler
from rag_engine import ask_rag, confidence_score
from agent import run_agent

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

if "owner" not in st.session_state:
    st.session_state.owner = None

st.subheader("Owner & Pet Setup")
owner_name = st.text_input("Owner name")
pet_name = st.text_input("Pet name")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Create Owner & Pet"):
    owner = Owner(name=owner_name)
    pet = Pet(name=pet_name, species=species)
    owner.add_pet(pet)
    st.session_state.owner = owner
    st.success(f"Created {owner_name} with pet {pet_name}!")

if st.session_state.owner:
    st.divider()
    st.subheader("Add a Task")
    pet_options = [p.name for p in st.session_state.owner.pets]
    selected_pet = st.selectbox("Pet", pet_options)
    task_title = st.text_input("Task title")
    task_time = st.text_input("Time (HH:MM)", value="08:00")
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    priority = st.selectbox("Priority", ["low", "medium", "high"])
    frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    if st.button("Add Task"):
        for pet in st.session_state.owner.pets:
            if pet.name == selected_pet:
                pet.add_task(Task(title=task_title, time=task_time, duration=duration, priority=priority, frequency=frequency))
        st.success(f"Added '{task_title}' to {selected_pet}!")

    st.divider()
    st.subheader("Today's Schedule")
    scheduler = Scheduler(st.session_state.owner)
    schedule = scheduler.sort_by_time()

    if schedule:
        for pet, task in schedule:
            status = "✅" if task.completed else "⬜"
            st.write(f"{status} [{task.time}] {task.title} ({pet}) - {task.duration}min | {task.priority}")
        conflicts = scheduler.detect_conflicts()
        if conflicts:
            for c in conflicts:
                st.warning(c)
    else:
        st.info("No tasks yet.")

    st.divider()
    st.subheader("Ask PawPal+ (AI Assistant)")
    user_question = st.text_input("Ask a pet care question...")
    if st.button("Ask"):
        if user_question:
            with st.spinner("Thinking..."):
                schedule_text = scheduler.daily_schedule()
                answer, retrieved = ask_rag(user_question, schedule_text)
                score = confidence_score(answer, [retrieved])
            st.success(answer)
            st.caption(f"Confidence Score: {score}")
            with st.expander("View retrieved knowledge"):
                st.text(retrieved)

    st.divider()
    st.subheader("AI Schedule Agent")
    if st.button("Run Agent Analysis"):
        with st.spinner("Agent is analyzing your schedule..."):
            result = run_agent(st.session_state.owner)
        st.text(result)