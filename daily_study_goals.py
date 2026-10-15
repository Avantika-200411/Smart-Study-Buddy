
import streamlit as st
import json
import os
from datetime import date

HISTORY_FILE = "study_history.json"
GOALS_FILE = "study_goals.json"


def load_json(path):
    if not os.path.exists(path):
        return {}

    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def daily_study_goals():
    st.subheader("🎯 Daily Study Goals")

    username = st.session_state.get("username", "")
    if not username:
        st.warning("Please log in first.")
        return

    goals_data = load_json(GOALS_FILE)
    user_goal = goals_data.get(username, 60)

    st.markdown("### Set Your Daily Focus Target")

    with st.form("daily_goal_form"):
        target_minutes = st.number_input(
            "Daily focus target (minutes)",
            min_value=15,
            max_value=720,
            value=int(user_goal),
            step=15
        )
        submitted = st.form_submit_button("Save Daily Goal")

    if submitted:
        goals_data[username] = int(target_minutes)
        save_json(GOALS_FILE, goals_data)
        st.success("Daily goal saved!")
        st.rerun()

    history = load_json(HISTORY_FILE)
    sessions = history.get(username, [])
    today = date.today().isoformat()

    today_minutes = 0

    for session in sessions:
        if session.get("date") == today:
            try:
                today_minutes += max(0, int(session.get("minutes", 0)))
            except (ValueError, TypeError):
                continue

    target = int(goals_data.get(username, 60))
    progress = min(today_minutes / target, 1.0) if target > 0 else 0

    st.divider()
    st.markdown("### 📊 Today's Progress")

    col1, col2, col3 = st.columns(3)
    col1.metric("Today's Focus", f"{today_minutes} min")
    col2.metric("Daily Target", f"{target} min")
    col3.metric("Remaining", f"{max(0, target - today_minutes)} min")

    st.progress(progress)
    st.write(f"**{progress * 100:.0f}% completed**")

    if today_minutes >= target:
        st.success("🎉 Daily goal achieved! Great work.")
    else:
        st.info("Keep going! Complete another focus session to reach your goal.")

    st.caption(
        "Progress is calculated from sessions saved in study_history.json."
    )
