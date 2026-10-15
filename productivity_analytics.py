
import streamlit as st
import datetime


def productivity_analytics():
    st.subheader("📊 Productivity Analytics")
    st.write("Track your study progress and task completion.")

    profile = st.session_state.user_profile
    tasks = profile.get("tasks", [])
    goals = profile.get("goals", [])
    today = datetime.date.today()

    def is_completed(item):
        return bool(item.get("done", item.get("Completed", False)))

    def get_name(item):
        return item.get("task", item.get("Task", "Untitled task"))

    def get_deadline(item):
        value = item.get("deadline", item.get("Deadline", ""))
        try:
            return datetime.date.fromisoformat(str(value))
        except (ValueError, TypeError):
            return None

    all_items = [
        {"item": task, "source": "Daily Planner"}
        for task in tasks
    ] + [
        {"item": goal, "source": "To-Do List"}
        for goal in goals
    ]

    if not all_items:
        st.info("No study tasks found. Add tasks in Daily Planner or To-Do List to see your analytics.")
        return

    total = len(all_items)
    completed = sum(is_completed(entry["item"]) for entry in all_items)
    pending = total - completed

    overdue = sum(
        not is_completed(entry["item"])
        and get_deadline(entry["item"]) is not None
        and get_deadline(entry["item"]) < today
        for entry in all_items
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Tasks", total)
    c2.metric("Completed", completed)
    c3.metric("Pending", pending)
    c4.metric("Overdue", overdue)

    completion_rate = completed / total
    st.markdown("### 🎯 Overall Completion")
    st.progress(completion_rate)
    st.caption(f"{completion_rate:.0%} of your tasks are completed.")

    st.divider()
    st.markdown("### 📚 Subject-wise Progress")

    subjects = {}

    for task in tasks:
        subject = task.get("subject", "General") or "General"
        if subject not in subjects:
            subjects[subject] = {"total": 0, "completed": 0}

        subjects[subject]["total"] += 1
        subjects[subject]["completed"] += int(is_completed(task))

    if subjects:
        for subject, stats in subjects.items():
            rate = stats["completed"] / stats["total"]
            st.write(f"**{subject}** — {stats['completed']}/{stats['total']} completed")
            st.progress(rate)
    else:
        st.caption("Add subject details in Daily Planner to see subject-wise progress.")

    st.divider()
    st.markdown("### ⏱️ Focus Session Progress")

    total_sessions = 0
    completed_sessions = 0

    for entry in all_items:
        item = entry["item"]

        required = item.get(
            "pomodoro_sessions",
            item.get("PomodoroSessionsRequired", 0)
        )
        finished = item.get(
            "completed_sessions",
            item.get("CompletedSessions", item.get("PomodoroSessions", 0))
        )

        try:
            total_sessions += max(0, int(required))
            completed_sessions += max(0, int(finished))
        except (ValueError, TypeError):
            continue

    st.metric("Completed Focus Sessions", completed_sessions)
    st.metric("Estimated Focus Sessions", total_sessions)

    if total_sessions:
        session_rate = min(1.0, completed_sessions / total_sessions)
        st.progress(session_rate)
        st.caption(f"{session_rate:.0%} of estimated focus sessions completed.")

    st.divider()
    st.markdown("### 📋 Task Overview")

    filter_choice = st.selectbox(
        "Filter by status",
        ["All", "Completed", "Pending", "Overdue"]
    )

    for entry in all_items:
        item = entry["item"]
        done = is_completed(item)
        deadline = get_deadline(item)

        if done:
            status = "Completed"
        elif deadline and deadline < today:
            status = "Overdue"
        else:
            status = "Pending"

        if filter_choice != "All" and status != filter_choice:
            continue

        with st.container(border=True):
            st.write(f"**{get_name(item)}**")
            st.caption(f"Source: {entry['source']} | Status: {status}")
            if deadline:
                st.caption(f"Deadline: {deadline.isoformat()}")
