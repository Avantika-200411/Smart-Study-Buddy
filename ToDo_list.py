
import streamlit as st
import datetime
from user_profile import save_users


def ToDo_list():
    st.subheader("📝 Your Study Task Manager")

    profile = st.session_state.user_profile
    user = st.session_state.username
    goals = profile.setdefault("goals", [])

    def save_data():
        st.session_state.user_db[user]["goals"] = goals
        save_users(st.session_state.user_db)

    # Add task
    with st.form("add_todo_form", clear_on_submit=True):
        task_name = st.text_input(
            "📚 Task name",
            placeholder="e.g. Revise DSA linked lists"
        )
        deadline = st.date_input(
            "📅 Deadline",
            value=datetime.date.today()
        )
        sessions = st.number_input(
            "Estimated focus sessions",
            min_value=1,
            max_value=20,
            value=2
        )

        add = st.form_submit_button("➕ Add Task")

        if add:
            if task_name.strip():
                goals.append({
                    "Task": task_name.strip(),
                    "Deadline": deadline.strftime("%Y-%m-%d"),
                    "Reminder": "09:00",
                    "Completed": False,
                    "Created": datetime.date.today().strftime("%Y-%m-%d"),
                    "PomodoroSessions": 0,
                    "CompletedSessions": 0,
                    "PomodoroSessionsRequired": int(sessions)
                })
                save_data()
                st.success("Task saved successfully!")
                st.rerun()
            else:
                st.warning("Please enter a task name.")

    st.divider()
    st.markdown("### 🎯 Your Tasks")

    if not goals:
        st.info("No tasks yet. Add your first task above!")
        return

    for i, task in enumerate(goals):
        # Support existing records
        task.setdefault("Completed", False)
        task.setdefault("PomodoroSessions", 0)
        task.setdefault("CompletedSessions", 0)
        task.setdefault("PomodoroSessionsRequired", 1)

        with st.container(border=True):
            st.markdown(f"**📌 {task.get('Task', 'Untitled task')}**")
            st.caption(f"Deadline: {task.get('Deadline', 'Not set')}")

            required = task["PomodoroSessionsRequired"]
            completed_sessions = task["CompletedSessions"]

            st.progress(
                min(1.0, completed_sessions / required)
            )
            st.caption(
                f"Focus sessions: {completed_sessions}/{required}"
            )

            checked = st.checkbox(
                "Mark task completed",
                value=task["Completed"],
                key=f"todo_done_{i}"
            )

            if checked != task["Completed"]:
                task["Completed"] = checked
                save_data()
                st.rerun()

            col1, col2 = st.columns(2)

            with col1:
                if st.button("✏️ Edit", key=f"todo_edit_{i}"):
                    st.session_state["edit_index"] = i
                    st.rerun()

            with col2:
                if st.button("🗑️ Delete", key=f"todo_delete_{i}"):
                    st.session_state["confirm_delete"] = i
                    st.rerun()

    # Edit task
    idx = st.session_state.get("edit_index")

    if idx is not None and 0 <= idx < len(goals):
        st.divider()
        st.markdown("### ✏️ Edit Task")

        current = goals[idx]

        with st.form("edit_todo_form"):
            new_name = st.text_input(
                "Task name",
                value=current.get("Task", "")
            )
            new_deadline = st.date_input(
                "Deadline",
                value=datetime.date.fromisoformat(
                    current.get(
                        "Deadline",
                        datetime.date.today().isoformat()
                    )
                )
            )
            new_required = st.number_input(
                "Required focus sessions",
                min_value=1,
                max_value=20,
                value=int(current.get("PomodoroSessionsRequired", 1))
            )

            update = st.form_submit_button("Save Changes")

            if update:
                if new_name.strip():
                    current["Task"] = new_name.strip()
                    current["Deadline"] = new_deadline.isoformat()
                    current["PomodoroSessionsRequired"] = int(new_required)
                    save_data()
                    del st.session_state["edit_index"]
                    st.success("Task updated!")
                    st.rerun()
                else:
                    st.warning("Task name cannot be empty.")

    # Confirm deletion
    delete_idx = st.session_state.get("confirm_delete")

    if delete_idx is not None and 0 <= delete_idx < len(goals):
        st.warning(
            f"Delete '{goals[delete_idx].get('Task', 'this task')}'?"
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Yes, delete", type="primary"):
                goals.pop(delete_idx)
                save_data()
                st.session_state.pop("confirm_delete", None)
                st.session_state.pop("edit_index", None)
                st.rerun()

        with col2:
            if st.button("Cancel"):
                st.session_state.pop("confirm_delete", None)
                st.rerun()

    # Weekly report
    today = datetime.date.today()
    start = today - datetime.timedelta(days=today.weekday())

    weekly = []
    for task in goals:
        try:
            created = datetime.date.fromisoformat(task.get("Created", ""))
            if start <= created <= today:
                weekly.append(task)
        except ValueError:
            continue

    completed = sum(task.get("Completed", False) for task in weekly)

    st.divider()
    st.markdown("### 📊 Weekly Progress")

    if weekly:
        rate = completed / len(weekly)
        st.progress(rate)
        st.write(
            f"{completed} of {len(weekly)} tasks completed "
            f"({int(rate * 100)}%)."
        )
    else:
        st.info("No tasks created this week.")
