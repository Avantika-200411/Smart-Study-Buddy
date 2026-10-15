
import streamlit as st
import json
import os
from datetime import date, timedelta

HISTORY_FILE = "study_history.json"


def study_streak():
    st.subheader("🔥 Daily Study Streak")

    username = st.session_state.get("username", "")
    if not username:
        st.warning("Please log in first.")
        return

    history = {}

    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as file:
                history = json.load(file)
        except (json.JSONDecodeError, OSError):
            st.error("Could not read study history.")
            return

    sessions = history.get(username, [])

    # Count only dates with recorded study sessions.
    study_dates = set()

    for session in sessions:
        try:
            session_date = date.fromisoformat(session["date"])
            study_dates.add(session_date)
        except (ValueError, KeyError, TypeError):
            continue

    today = date.today()
    total_study_days = len(study_dates)

    # A streak is active if the user studied today or yesterday.
    streak = 0
    check_date = today if today in study_dates else today - timedelta(days=1)

    while check_date in study_dates:
        streak += 1
        check_date -= timedelta(days=1)

    today_sessions = [
        session for session in sessions
        if session.get("date") == today.isoformat()
    ]

    today_minutes = sum(
        int(session.get("minutes", 0) or 0)
        for session in today_sessions
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("🔥 Current Streak", f"{streak} days")
    col2.metric("📅 Total Study Days", total_study_days)
    col3.metric("⏱️ Today's Focus", f"{today_minutes} min")

    st.divider()

    if today in study_dates:
        st.success("🎉 You've studied today. Keep your streak going!")
    else:
        st.info("📚 Complete a focus session today to start or continue your streak.")

    st.markdown("### 📆 Last 7 Days")

    for offset in range(6, -1, -1):
        day = today - timedelta(days=offset)
        studied = day in study_dates
        label = day.strftime("%A, %d %b")
        status = "✅ Studied" if studied else "⬜ No session recorded"
        st.write(f"**{label}:** {status}")

    st.caption(
        "Streaks use dates recorded in study_history.json. "
        "Manually added history entries also count as study days."
    )
