import streamlit as st
import time
from datetime import datetime, time as datetime_time

# --- PAGE CONFIG ---
st.set_page_config(page_title="Smart Priority To-Do List", page_icon="⚡", layout="wide")

# --- INITIALIZE MEMORY LAYER WITH SAFETY FORMAT CHECK ---
if "todo_list" not in st.session_state:
    st.session_state.todo_list = []
else:
    # Safety Check: If an old task format exists without a deadline, flush the list to prevent KeyErrors
    for task in st.session_state.todo_list:
        if "deadline" not in task:
            st.session_state.todo_list = []
            break

st.title("⚡ Smart Task Engine with Deadlines")
st.write("A bug-free, priority-sorted predictive tracking matrix built in Python.")
st.markdown("---")

# --- SIDEBAR PRODUCTION METRICS ---
with st.sidebar:
    st.header("📊 Progress Analytics")
    total_tasks = len(st.session_state.todo_list)
    completed_tasks = sum(1 for t in st.session_state.todo_list if t["done"])
    pending_tasks = total_tasks - completed_tasks
    
    st.metric(label="Total Tasks", value=total_tasks)
    col_metrics1, col_metrics2 = st.columns(2)
    col_metrics1.metric(label="Pending", value=pending_tasks)
    col_metrics2.metric(label="Done", value=completed_tasks)
    
    st.markdown("**Workload Cleared**")
    if total_tasks > 0:
        ratio = completed_tasks / total_tasks
        st.progress(ratio)
        st.caption(f"{int(ratio * 100)}% of tasks archived.")
    else:
        st.progress(0.0)
        st.caption("No operational metrics tracked yet.")

# --- MAIN RESPONSIVE GRID LAYOUT ---
col_input, col_display = st.columns([1.5, 2.5])

with col_input:
    st.subheader("📥 Add a New Task")
    with st.form(key="task_form", clear_on_submit=True):
        task_input = st.text_input("Task Intent:", placeholder="e.g., Finish math assignment...")
        priority_input = st.selectbox("Priority Level", ["🔴 High", "🟡 Medium", "🟢 Low"])
        time_limit = st.time_input("Target Deadline", datetime_time(23, 59))
        
        submit_button = st.form_submit_button(label="🚀 Add to Roadmap", use_container_width=True)

    if submit_button and task_input.strip() != "":
        unique_id = f"{task_input.strip()[:10]}_{time.time()}"
        target_datetime = datetime.combine(datetime.today().date(), time_limit)
        
        new_task = {
            "id": unique_id,
            "task": task_input.strip(),
            "priority": priority_input,
            "done": False,
            "deadline": target_datetime
        }
        st.session_state.todo_list.append(new_task)
        st.rerun()

with col_display:
    st.subheader("📋 Your Organized Roadmap")
    
    # --- SMART SORTING ENGINE ---
    priority_weights = {"🔴 High": 1, "🟡 Medium": 2, "🟢 Low": 3}
    st.session_state.todo_list.sort(key=lambda x: (x["done"], priority_weights.get(x["priority"], 4)))
    
    current_now = datetime.now()
    
    if not st.session_state.todo_list:
        st.info("Your pipeline is currently clear.")
    else:
        for task in list(st.session_state.todo_list):
            col_check, col_text, col_del = st.columns([0.5, 4, 0.5])
            
            # Safe checking fallback dictionary lookup method (.get()) to prevent runtime KeyErrors
            task_deadline = task.get("deadline", current_now)
            is_overdue = current_now > task_deadline and not task.get("done", False)
            formatted_time = task_deadline.strftime("%I:%M %p")
            
            if is_overdue:
                st.toast(f"🚨 Milestone passed: '{task['task']}' is overdue!", icon="⚠️")
            
            # 1. State Mutation Logic
            with col_check:
                is_checked = st.checkbox("", value=task["done"], key=f"chk_{task['id']}")
                if is_checked != task["done"]:
                    task["done"] = is_checked
                    st.rerun()
            
            # 2. Text Representation Layer
            with col_text:
                if task["done"]:
                    st.markdown(f"~~{task['priority']} {task['task']}~~ :green[*(Archived)*]")
                elif is_overdue:
                    st.markdown(f"**{task['priority']} {task['task']}** :red[[🚨 OVERDUE - past {formatted_time}]]")
                else:
                    st.markdown(f"**{task['priority']}** {task['task']} *(Due by {formatted_time})*")
            
            # 3. Targeted Deletion Engine
            with col_del:
                if st.button("🗑️", key=f"del_{task['id']}"):
                    st.session_state.todo_list.remove(task)
                    st.rerun()
                    
        st.markdown("---")
        
        # --- GLOBAL CLEANUP CONTROLS ---
        col_clear_done, col_clear_all = st.columns(2)
        with col_clear_done:
            if st.button("🧹 Clear All Completed Tasks", use_container_width=True):
                st.session_state.todo_list = [t for t in st.session_state.todo_list if not t["done"]]
                st.rerun()
        with col_clear_all:
            if st.button("🚨 Clear Entire List", use_container_width=True):
                st.session_state.todo_list = []
                st.rerun()