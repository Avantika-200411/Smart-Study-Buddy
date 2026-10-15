
import streamlit as st
import json
import os
from datetime import date, timedelta


def home_dashboard():
    username = st.session_state.get("username", "")
    profile = st.session_state.get("user_profile", {})

    if not username:
        st.warning("Please log in first.")
        return

    # ---------- WELCOME HEADER ----------
    st.markdown(
        """
        <div style="
            padding: 28px;
            border-radius: 18px;
            background: linear-gradient(120deg, #e8eaff, #f5f0ff);
            border: 1px solid #d9dcff;
            margin-bottom: 24px;
        ">
            <h1 style="color:#292d72; margin:0;">
                Welcome back 👋
            </h1>
            <p style="color:#4b5563; margin:10px 0 0 0;">
                Plan smarter. Focus better. Achieve more.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tasks = profile.get("tasks", [])
    pending_tasks = [
        task for task in tasks
        if not task.get("done", task.get("Completed", False))
    ]
    completed_tasks = [
        task for task in tasks
        if task.get("done", task.get("Completed", False))
    ]

    # ---------- STUDY HISTORY ----------
    history = {}
    if os.path.exists("study_history.json"):
        try:
            with open("study_history.json", "r", encoding="utf-8") as file:
                history = json.load(file)
        except (json.JSONDecodeError, OSError):
            history = {}

    sessions = history.get(username, [])
    today = date.today().isoformat()

    def session_minutes(session):
        try:
            return max(0, int(session.get("minutes", 0) or 0))
        except (ValueError, TypeError):
            return 0

    today_minutes = sum(
        session_minutes(session)
        for session in sessions
        if session.get("date") == today
    )

    study_dates = set()
    for session in sessions:
        try:
            study_dates.add(date.fromisoformat(session.get("date", "")))
        except (ValueError, TypeError):
            continue

    streak = 0
    check_day = (
        date.today()
        if date.today() in study_dates
        else date.today() - timedelta(days=1)
    )

    while check_day in study_dates:
        streak += 1
        check_day -= timedelta(days=1)

    # ---------- DAILY GOAL ----------
    daily_goals = {}
    if os.path.exists("study_goals.json"):
        try:
            with open("study_goals.json", "r", encoding="utf-8") as file:
                daily_goals = json.load(file)
        except (json.JSONDecodeError, OSError):
            daily_goals = {}

    try:
        daily_target = max(1, int(daily_goals.get(username, 60)))
    except (ValueError, TypeError):
        daily_target = 60

    progress = min(today_minutes / daily_target, 1.0)

    # ---------- QUICK ACTIONS ----------
    st.subheader("⚡ Quick Actions")

    action1, action2, action3 = st.columns(3)

    if action1.button("📝 Daily Planner", use_container_width=True):
        st.session_state["dashboard_action"] = "Daily Planner"

    if action2.button("⏱️ Focus Timer", use_container_width=True):
        st.session_state["dashboard_action"] = "Pomodoro Timer"

    if action3.button("📊 My Progress", use_container_width=True):
        st.session_state["dashboard_action"] = "Productivity Analytics"

    if st.session_state.get("dashboard_action"):
        st.info(
            "Use the corresponding page in the sidebar: "
            + st.session_state["dashboard_action"]
        )

    st.divider()

    # ---------- OVERVIEW ----------
    st.subheader("📊 Your Study Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📚 Pending Tasks", len(pending_tasks))
    col2.metric("✅ Completed Tasks", len(completed_tasks))
    col3.metric("⏱️ Today's Focus", f"{today_minutes} min")
    col4.metric("🔥 Study Streak", f"{streak} days")

    st.divider()

    # ---------- DAILY GOAL ----------
    st.subheader("🎯 Daily Focus Goal")

    st.progress(progress)

    goal_col1, goal_col2 = st.columns(2)
    goal_col1.write(f"**{today_minutes} / {daily_target} minutes**")
    goal_col2.write(
        f"**{int(progress * 100)}% complete**"
    )

    if today_minutes >= daily_target:
        st.success("🎉 Your daily focus goal is complete!")
    else:
        st.info(
            f"{daily_target - today_minutes} more minutes "
            "to reach today's goal."
        )

    st.divider()

    # ---------- PENDING TASKS ----------
    st.subheader("📝 Upcoming Study Tasks")

    if pending_tasks:
        for index, task in enumerate(pending_tasks[:5], start=1):
            name = task.get("task", task.get("Task", "Untitled task"))
            subject = task.get("subject", "General")

            with st.container(border=True):
                st.markdown(f"**{index}. {name}**")
                st.caption(f"📘 Subject: {subject}")

        if len(pending_tasks) > 5:
            st.caption(
                f"And {len(pending_tasks) - 5} more pending tasks."
            )
    else:
        st.success("All Daily Planner tasks are complete!")

    st.divider()

    # ---------- ACHIEVEMENTS ----------
    st.subheader("🏆 Study Achievements")

    total_sessions = len(sessions)
    total_minutes = sum(session_minutes(s) for s in sessions)

    achievements = [
        ("First Study Session", total_sessions >= 1),
        ("5 Study Sessions", total_sessions >= 5),
        ("5 Hours of Focus", total_minutes >= 300),
        ("3-Day Streak", streak >= 3),
        ("7-Day Streak", streak >= 7),
        ("Daily Goal Completed", today_minutes >= daily_target),
    ]

    unlocked = sum(1 for _, earned in achievements if earned)

    st.metric("Achievements Unlocked", f"{unlocked}/6")

    achievement_cols = st.columns(3)

    for index, (name, earned) in enumerate(achievements):
        with achievement_cols[index % 3]:
            with st.container(border=True):
                st.write("🏅" if earned else "🔒")
                st.write(name)
                st.caption("Unlocked" if earned else "Keep studying!")

    st.caption(
        "Your dashboard uses saved tasks, study history, "
        "and daily goal data."
    )
