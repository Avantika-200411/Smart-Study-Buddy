
import streamlit as st
import datetime


def study_reminders():
    st.subheader("🔔 Study Reminders")

    profile = st.session_state.get("user_profile", {})
    tasks = profile.get("tasks", [])
    goals = profile.get("goals", [])

    now = datetime.datetime.now()
    today = now.date()
    current_time = now.strftime("%H:%M")

    due_today = []
    overdue = []
    reminders_due = []

    for task in tasks:
        if task.get("done", task.get("Completed", False)):
            continue

        name = task.get("task", task.get("Task", "Untitled task"))
        deadline = task.get("deadline", task.get("Deadline", ""))
        reminder = task.get("reminder_time", task.get("Reminder", ""))

        try:
            deadline_date = datetime.date.fromisoformat(str(deadline))
        except (ValueError, TypeError):
            deadline_date = None

        if deadline_date and deadline_date < today:
            overdue.append(name)
        elif deadline_date == today:
            due_today.append(name)

        # In-app reminder for the current minute
        if reminder == current_time:
            reminders_due.append(name)

    col1, col2, col3 = st.columns(3)
    col1.metric("⚠️ Overdue", len(overdue))
    col2.metric("📅 Due Today", len(due_today))
    col3.metric("🔔 Reminders Now", len(reminders_due))

    if overdue:
        st.error("Overdue tasks")
        for name in overdue:
            st.write(f"- {name}")

    if due_today:
        st.warning("Tasks due today")
        for name in due_today:
            st.write(f"- {name}")

    if reminders_due:
        st.success("⏰ Your scheduled reminder time has arrived!")
        for name in reminders_due:
            st.write(f"📚 Time to work on: **{name}**")
    else:
        st.info(
            "No task reminder is due at this minute. "
            "Your saved reminder times are checked when this page runs."
        )

    st.caption(
        "Reminder times use your computer's local time. "
        "This page provides in-app alerts, not background or push notifications."
    )
