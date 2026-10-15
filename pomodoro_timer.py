
import time
import json
import os
import datetime
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from user_profile import save_users

HISTORY_FILE = "study_history.json"


def record_completed_session(username, subject, task, minutes):
    history = {}

    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as file:
                history = json.load(file)
        except (json.JSONDecodeError, OSError):
            history = {}

    user_sessions = history.get(username, [])
    user_sessions.append({
        "subject": subject or "General",
        "task": task or "Focus Session",
        "minutes": int(minutes),
        "date": datetime.date.today().isoformat(),
        "recorded_at": datetime.datetime.now().isoformat(
            timespec="seconds"
        )
    })

    history[username] = user_sessions

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)


def pomodoro_timer():
    st.subheader("⏱️ Focus Room")
    st.write("Choose a task from your Daily Planner or To-Do List.")

    profile = st.session_state.get("user_profile", {})
    tasks = profile.setdefault("tasks", [])
    goals = profile.setdefault("goals", [])

    if not st.session_state.get("username"):
        st.warning("Please log in first.")
        return

    available_tasks = []

    for i, task in enumerate(tasks):
        if not task.get("done", task.get("Completed", False)):
            available_tasks.append(("planner", i, task))

    for i, task in enumerate(goals):
        if not task.get("Completed", False):
            available_tasks.append(("todo", i, task))

    defaults = {
        "focus_running": False,
        "focus_end": None,
        "focus_remaining": 0,
        "focus_task_source": None,
        "focus_task_index": None,
        "focus_duration": 1500,
        "focus_task_name": "",
        "focus_subject": "General",
        "focus_session_saved": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    def get_task_name(task, source):
        if source == "planner":
            return task.get("task", task.get("Task", "Untitled task"))
        return task.get("Task", "Untitled task")

    active = (
        st.session_state.focus_running
        or st.session_state.focus_remaining > 0
    )

    if not active:
        if not available_tasks:
            st.success("🎉 No pending tasks! Add a task to start focusing.")
            return

        options = [
            f"{'Daily Planner' if source == 'planner' else 'To-Do List'}: "
            f"{get_task_name(task, source)}"
            for source, _, task in available_tasks
        ]

        selected = st.selectbox("Choose your task", options)
        selected_index = options.index(selected)
        source, task_index, selected_task = available_tasks[selected_index]

        default_minutes = st.select_slider(
            "Focus duration (minutes)",
            options=[5, 10, 15, 20, 25, 30, 45, 60],
            value=25
        )

        if st.button("▶ Start Focus Session"):
            st.session_state.focus_task_source = source
            st.session_state.focus_task_index = task_index
            st.session_state.focus_task_name = get_task_name(
                selected_task, source
            )
            st.session_state.focus_subject = selected_task.get(
                "subject", "General"
            )
            st.session_state.focus_duration = default_minutes * 60
            st.session_state.focus_remaining = default_minutes * 60
            st.session_state.focus_end = time.time() + default_minutes * 60
            st.session_state.focus_running = True
            st.session_state.focus_session_saved = False
            st.rerun()

        return

    if st.session_state.focus_running:
        remaining = max(
            0,
            int(st.session_state.focus_end - time.time())
        )

        if remaining <= 0:
            if not st.session_state.focus_session_saved:
                username = st.session_state.username
                task_name = st.session_state.focus_task_name
                subject = st.session_state.focus_subject
                minutes = st.session_state.focus_duration // 60
                source = st.session_state.focus_task_source
                task_index = st.session_state.focus_task_index

                record_completed_session(
                    username, subject, task_name, minutes
                )

                if source == "planner" and task_index is not None:
                    if task_index < len(tasks):
                        tasks[task_index]["completed_sessions"] = (
                            tasks[task_index].get("completed_sessions", 0) + 1
                        )
                elif source == "todo" and task_index is not None:
                    if task_index < len(goals):
                        goals[task_index]["CompletedSessions"] = (
                            goals[task_index].get("CompletedSessions", 0) + 1
                        )

                users = st.session_state.get("user_db", {})
                if username in users:
                    users[username]["tasks"] = tasks
                    users[username]["goals"] = goals
                    save_users(users)
                    st.session_state.user_db = users

                st.session_state.focus_session_saved = True

            st.session_state.focus_running = False
            st.session_state.focus_end = None
            st.session_state.focus_remaining = 0
            st.success("🎉 Focus session completed and saved to Study History!")
            st.rerun()

        st.session_state.focus_remaining = remaining
        minutes, seconds = divmod(remaining, 60)
        st.markdown(f"# {minutes:02d}:{seconds:02d}")
        st.caption(f"Studying: {st.session_state.focus_task_name}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("⏸ Pause"):
                st.session_state.focus_remaining = remaining
                st.session_state.focus_running = False
                st.session_state.focus_end = None
                st.rerun()

        with col2:
            if st.button("⏹ Stop Session"):
                st.session_state.focus_running = False
                st.session_state.focus_end = None
                st.session_state.focus_remaining = 0
                st.session_state.focus_task_source = None
                st.session_state.focus_task_index = None
                st.rerun()

        st_autorefresh(interval=1000, key="focus_countdown_refresh")

    elif st.session_state.focus_remaining > 0:
        remaining = st.session_state.focus_remaining
        minutes, seconds = divmod(remaining, 60)
        st.markdown(f"# {minutes:02d}:{seconds:02d}")
        st.caption("Timer paused. Resume when you're ready.")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("▶ Resume"):
                st.session_state.focus_end = time.time() + remaining
                st.session_state.focus_running = True
                st.rerun()

        with col2:
            if st.button("⏹ Stop Session"):
                st.session_state.focus_running = False
                st.session_state.focus_end = None
                st.session_state.focus_remaining = 0
                st.session_state.focus_task_source = None
                st.session_state.focus_task_index = None
                st.rerun()

    st.caption(
        "Only fully completed focus sessions are recorded. "
        "Stopping early does not add a history entry."
    )
