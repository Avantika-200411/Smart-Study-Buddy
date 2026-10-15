
import streamlit as st
import datetime
from user_profile import save_users


def daily_planner():
    st.subheader("📅 Smart Daily Planner")

    profile = st.session_state.user_profile
    user = st.session_state.username

    if "tasks" not in profile:
        profile["tasks"] = []

    tasks = profile["tasks"]
    today = datetime.date.today()

    # Dashboard
    st.markdown("### 📊 Today's Focus Dashboard")

    def get_task_status(task):
        return bool(task.get("done", task.get("Completed", False)))

    def get_deadline(task):
        value = task.get("deadline", task.get("Deadline", ""))
        try:
            return datetime.date.fromisoformat(str(value))
        except (ValueError, TypeError):
            return None

    completed = sum(get_task_status(t) for t in tasks)
    pending = len(tasks) - completed
    overdue = sum(
        not get_task_status(t)
        and get_deadline(t) is not None
        and get_deadline(t) < today
        for t in tasks
    )
    due_today = sum(
        not get_task_status(t)
        and get_deadline(t) == today
        for t in tasks
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📚 Total Tasks", len(tasks))
    c2.metric("✅ Completed", completed)
    c3.metric("⏳ Pending", pending)
    c4.metric("⚠️ Overdue", overdue)

    if tasks:
        st.progress(completed / len(tasks))
        st.caption(f"Overall progress: {completed}/{len(tasks)} tasks completed")

    if due_today:
        st.warning(f"📅 You have {due_today} task(s) due today.")
    elif tasks and pending:
        st.info("Keep going! Focus on one task at a time.")

    st.divider()
    st.markdown("### 🎯 Plan Your Study Session")

    with st.form("add_task_form", clear_on_submit=True):
        subject = st.text_input("📚 Subject")
        topic = st.text_input("📝 Topic to study")
        task_desc = st.text_input("What do you need to complete?")

        col1, col2 = st.columns(2)

        with col1:
            deadline = st.date_input("📅 Deadline", value=today)
            difficulty = st.select_slider(
                "Difficulty",
                options=["Easy", "Medium", "Hard"],
                value="Medium"
            )

        with col2:
            pomodoro_sessions = st.slider(
                "Estimated focus sessions", 1, 10, 2
            )
            reminder_time = st.time_input(
                "⏰ Reminder time",
                value=datetime.time(9, 0)
            )

        submitted = st.form_submit_button(
            "➕ Add to My Study Plan",
            type="primary"
        )

        if submitted:
            if not task_desc.strip():
                st.warning("Please enter a task.")
            else:
                new_task = {
                    "task": task_desc.strip(),
                    "subject": subject.strip() or "General",
                    "topic": topic.strip() or task_desc.strip(),
                    "deadline": deadline.isoformat(),
                    "difficulty": difficulty,
                    "pomodoro_sessions": pomodoro_sessions,
                    "completed_sessions": 0,
                    "reminder_time": reminder_time.strftime("%H:%M"),
                    "done": False
                }

                tasks.append(new_task)
                st.session_state.user_db[user]["tasks"] = tasks
                save_users(st.session_state.user_db)
                st.success("Your study task has been saved!")
                st.rerun()

    st.divider()
    st.markdown("### 📋 Your Study Tasks")

    if not tasks:
        st.info("No tasks yet. Add your first study task above!")
        return

    # Filters
    filter_choice = st.radio(
        "Filter tasks",
        ["All Tasks", "Pending", "Completed", "Overdue", "Due Today"],
        horizontal=True,
        key="planner_filter"
    )

    visible_tasks = []

    for i, task in enumerate(tasks):
        is_done = get_task_status(task)
        due_date = get_deadline(task)

        if filter_choice == "Pending" and is_done:
            continue
        if filter_choice == "Completed" and not is_done:
            continue
        if filter_choice == "Overdue" and (
            is_done or due_date is None or due_date >= today
        ):
            continue
        if filter_choice == "Due Today" and (
            is_done or due_date != today
        ):
            continue

        visible_tasks.append((i, task))

    if not visible_tasks:
        st.info("No tasks found for this filter.")
        return

    for i, task in visible_tasks:
        task_name = task.get("task", task.get("Task", "Untitled task"))
        is_done = get_task_status(task)
        due_date = get_deadline(task)

        total = task.get(
            "pomodoro_sessions",
            task.get("PomodoroSessionsRequired", 1)
        )
        finished = task.get(
            "completed_sessions",
            task.get("CompletedSessions", task.get("PomodoroSessions", 0))
        )
        difficulty = task.get("difficulty", "Not set")
        subject_name = task.get("subject", "General")
        topic_name = task.get("topic", task_name)

        if is_done:
            status = "✅ Completed"
        elif due_date and due_date < today:
            status = "⚠️ Overdue"
        elif due_date == today:
            status = "📅 Due today"
        else:
            status = "⏳ Pending"

        with st.container(border=True):
            st.markdown(f"**📘 {task_name}**")
            st.caption(f"Subject: {subject_name} | Topic: {topic_name}")
            st.write(f"Status: {status}")
            st.write(
                f"Deadline: {due_date.isoformat() if due_date else 'Not set'}"
            )
            st.write(
                f"⏱️ Focus sessions: {finished}/{total} | "
                f"Difficulty: {difficulty}"
            )

            session_progress = min(1.0, max(0.0, finished / max(1, total)))
            st.progress(session_progress)

            new_done = st.checkbox(
                "Mark task as completed",
                value=is_done,
                key=f"planner_done_{i}"
            )

            if new_done != is_done:
                task["done"] = new_done

                if "Completed" in task:
                    task["Completed"] = new_done

                st.session_state.user_db[user]["tasks"] = tasks
                save_users(st.session_state.user_db)
                st.rerun()
