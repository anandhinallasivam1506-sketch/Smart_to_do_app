import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Smart To-Do Manager", page_icon="📝", layout="centered")

# --- INITIALIZE SESSION STATE ---
if "todo_list" not in st.session_state:
    st.session_state.todo_list = [
        {"task": "Finish Python project assignment", "priority": "🔴 High", "done": False},
        {"task": "Buy notebooks for next semester", "priority": "🟢 Low", "done": False},
        {"task": "Prepare for quiz tomorrow", "priority": "🟡 Medium", "done": False}
    ]

# --- APP INTERFACE ---
st.title("📝 Smart To-Do List Manager")
st.write("Add your tasks, set their priority, and let the app automatically bubble important tasks to the top!")
st.markdown("---")

# --- FRONTEND INPUT FORM ---
st.subheader("➕ Add a New Task")
col1, col2 = st.columns([3, 1])

with col1:
    new_task = st.text_input("What needs to be done?", placeholder="e.g., Study for exams...", label_visibility="collapsed")
with col2:
    priority = st.selectbox("Priority", ["🔴 High", "🟡 Medium", "🟢 Low"], label_visibility="collapsed")

if st.button("Add Task to List", use_container_width=True):
    if new_task.strip() == "":
        st.warning("Task description cannot be empty!")
    else:
        st.session_state.todo_list.append({
            "task": new_task,
            "priority": priority,
            "done": False
        })
        st.success(f"Added: '{new_task}'")
        st.rerun()

