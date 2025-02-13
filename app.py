import streamlit as st
import json
import os

# File where tasks are stored
TASKS_FILE = "tasks.json"

def load_tasks():
    """Load tasks from the JSON file."""
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_tasks(tasks):
    """Save tasks to the JSON file."""
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

# Initialize session state
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

st.title("To‑Do List Manager")
st.markdown("A simple app to add, complete, and delete your tasks. Your tasks are saved locally in a JSON file.")

# --- Add New Task ---
with st.form(key="add_task_form", clear_on_submit=True):
    new_task = st.text_input("Enter a new task:")
    submit_task = st.form_submit_button("Add Task")
    if submit_task and new_task:
        st.session_state.tasks.append({"task": new_task, "completed": False})
        save_tasks(st.session_state.tasks)
        st.experimental_rerun()  # refresh the app

# --- Display Tasks ---
st.subheader("Your Tasks")
if not st.session_state.tasks:
    st.info("No tasks yet. Add a task above!")
else:
    for index, task in enumerate(st.session_state.tasks):
        cols = st.columns([0.1, 0.6, 0.15, 0.15])
        # Display task number
        cols[0].write(f"{index+1}.")
        
        # Display task text with strikethrough if completed
        task_text = f"<s>{task['task']}</s>" if task["completed"] else task["task"]
        cols[1].markdown(task_text, unsafe_allow_html=True)
        
        # Button to mark as complete (if not already)
        if not task["completed"]:
            if cols[2].button("Complete", key=f"complete_{index}"):
                st.session_state.tasks[index]["completed"] = True
                save_tasks(st.session_state.tasks)
                st.experimental_rerun()
        else:
            cols[2].write("")  # spacer
        
        # Button to delete task
        if cols[3].button("Delete", key=f"delete_{index}"):
            st.session_state.tasks.pop(index)
            save_tasks(st.session_state.tasks)
            st.experimental_rerun()

# --- Optionally, a Refresh Button ---
if st.button("Refresh Tasks"):
    st.session_state.tasks = load_tasks()
    st.experimental_rerun()
