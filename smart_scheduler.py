
import streamlit as st
import datetime


def smart_scheduler():
    st.subheader("🗓️ Smart Study Scheduler")
    st.write("Get a suggested order for your pending study tasks.")

    profile = st.session_state.get("user_profile", {})
    tasks = profile.get("tasks", [])
    goals = profile.get("goals", [])
    today = datetime.date.today()

    schedule_tasks = []

    for task in tasks:
        if task.get("done", task.get("Completed", False)):
            continue

        schedule_tasks.append({
            "name": task.get("task", task.get("Task", "Untitled task")),
            "subject": task.get("subject", "General"),
            "deadline": task.get("deadline", task.get("Deadline", "")),
            "sessions": task.get(
                "pomodoro_sessions",
                task.get("PomodoroSessionsRequired", 1)
            ),
            "difficulty": task.get("difficulty", "Medium"),
            "source": "Daily Planner"
        })

    for goal in goals:
        if goal.get("Completed", False):
            continue

        schedule_tasks.append({
            "name": goal.get("Task", "Untitled task"),
            "subject": "General",
            "deadline": goal.get("Deadline", ""),
            "sessions": goal.get("PomodoroSessionsRequired", 1),
            "difficulty": "Medium",
            "source": "To-Do List"
        })

    if not schedule_tasks:
        st.success("🎉 No pending tasks! Add tasks to create a study plan.")
        return

    def parse_deadline(value):
        try:
            return datetime.date.fromisoformat(str(value))
        except (ValueError, TypeError):
            return None

    def priority_key(task):
        deadline = parse_deadline(task["deadline"])

        # Earlier deadlines first; tasks without a valid deadline go last.
        deadline_key = deadline or datetime.date.max

        difficulty_order = {
            "Hard": 0,
            "Medium": 1,
            "Easy": 2
        }

        return (
            deadline_key,
            difficulty_order.get(task["difficulty"], 1)
        )

    schedule_tasks.sort(key=priority_key)

    st.markdown("### 📌 Your Suggested Study Order")

    total_sessions = 0

    for number, task in enumerate(schedule_tasks, start=1):
        deadline = parse_deadline(task["deadline"])

        try:
            sessions = max(1, int(task["sessions"]))
        except (ValueError, TypeError):
            sessions = 1

        total_sessions += sessions

        if deadline and deadline < today:
            status = "⚠️ Overdue"
        elif deadline == today:
            status = "📅 Due today"
        elif deadline:
            status = f"Deadline: {deadline.isoformat()}"
        else:
            status = "No deadline set"

        with st.container(border=True):
            st.markdown(f"**{number}. {task['name']}**")
            st.caption(
                f"{task['source']} · {task['subject']} · "
                f"Difficulty: {task['difficulty']}"
            )
            st.write(status)
            st.write(f"Estimated focus sessions: {sessions}")
            st.write(f"Approximate focus time: {sessions * 25} minutes")

    st.divider()
    st.markdown("### ⏱️ Estimated Study Time")
    st.metric("Total focus time", f"{total_sessions * 25} minutes")
    st.caption(
        "Estimate assumes 25 minutes per focus session. "
        "Breaks are not included. This is a suggested order, not a fixed timetable."
    )
