
import streamlit as st
import json
import os
from datetime import date, timedelta

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


def study_achievements():
    st.subheader("🏆 Study Achievements")
    st.write("Build consistency and unlock achievements through your study activity.")

    username = st.session_state.get("username", "")
    if not username:
        st.warning("Please log in first.")
        return

    history = load_json(HISTORY_FILE)
    goals_data = load_json(GOALS_FILE)
    sessions = history.get(username, [])

    valid_sessions = []

    for session in sessions:
        try:
            session_date = date.fromisoformat(session.get("date", ""))
            minutes = max(0, int(session.get("minutes", 0)))
            valid_sessions.append({
                "date": session_date,
                "minutes": minutes
            })
        except (ValueError, TypeError):
            continue

    study_dates = {session["date"] for session in valid_sessions}
    total_sessions = len(valid_sessions)
    total_minutes = sum(session["minutes"] for session in valid_sessions)
    today = date.today()

    streak = 0
    check_date = today if today in study_dates else today - timedelta(days=1)

    while check_date in study_dates:
        streak += 1
        check_date -= timedelta(days=1)

    today_minutes = sum(
        session["minutes"]
        for session in valid_sessions
        if session["date"] == today
    )

    daily_target = int(goals_data.get(username, 60))
    daily_goal_reached = today_minutes >= daily_target

    achievements = [
        {
            "name": "First Focus",
            "description": "Record your first study session.",
            "icon": "🌱",
            "unlocked": total_sessions >= 1
        },
        {
            "name": "Study Starter",
            "description": "Record 5 study sessions.",
            "icon": "📚",
            "unlocked": total_sessions >= 5
        },
        {
            "name": "Focus Champion",
            "description": "Accumulate 5 hours of focus time.",
            "icon": "🎯",
            "unlocked": total_minutes >= 300
        },
        {
            "name": "Consistent Learner",
            "description": "Study on 3 consecutive days.",
            "icon": "🔥",
            "unlocked": streak >= 3
        },
        {
            "name": "Weekly Warrior",
            "description": "Study on 7 consecutive days.",
            "icon": "🏅",
            "unlocked": streak >= 7
        },
        {
            "name": "Daily Goal Achiever",
            "description": "Reach your daily focus-time target today.",
            "icon": "⭐",
            "unlocked": daily_goal_reached
        }
    ]

    unlocked_count = sum(item["unlocked"] for item in achievements)

    col1, col2, col3 = st.columns(3)
    col1.metric("Badges Unlocked", f"{unlocked_count}/{len(achievements)}")
    col2.metric("Recorded Sessions", total_sessions)
    col3.metric("Total Focus Time", f"{total_minutes // 60} hr {total_minutes % 60} min")

    st.progress(unlocked_count / len(achievements))

    st.markdown("### 🎖️ Your Badges")

    for achievement in achievements:
        with st.container(border=True):
            col1, col2 = st.columns([1, 5])

            with col1:
                st.markdown(f"# {achievement['icon']}")

            with col2:
                st.markdown(f"**{achievement['name']}**")

                if achievement["unlocked"]:
                    st.success("Unlocked")
                else:
                    st.caption("🔒 " + achievement["description"])

    st.caption(
        "Achievements are calculated from your saved study history. "
        "The streak badges use your current streak, so a broken streak "
        "will no longer qualify until you build it again."
    )
