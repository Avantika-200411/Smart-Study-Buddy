
import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date

HISTORY_FILE = "study_history.json"


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return {}

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}


def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)

def record_completed_session(username, subject, task, minutes):
    history = load_history()

    sessions = history.get(username, [])
    sessions.append({
        "subject": subject or "General",
        "task": task or "Focus Session",
        "minutes": int(minutes),
        "date": date.today().isoformat(),
        "recorded_at": datetime.now().isoformat(timespec="seconds")
    })

    history[username] = sessions
    save_history(history)


def study_history():
    st.subheader("📚 Study Session History")

    username = st.session_state.get("username", "")
    if not username:
        st.warning("Please log in to view your study history.")
        return

    history = load_history()
    sessions = history.get(username, [])

    st.write("Record completed study sessions and track your focus time.")

    with st.form("record_study_session"):
        subject = st.text_input("Subject", placeholder="e.g. Python")
        task = st.text_input("Task studied", placeholder="e.g. Recursion")
        minutes = st.number_input(
            "Focus time (minutes)",
            min_value=1,
            max_value=600,
            value=25
        )
        session_date = st.date_input("Study date", value=date.today())

        submitted = st.form_submit_button("Save Study Session")

    if submitted:
        if not subject.strip() or not task.strip():
            st.warning("Please enter both subject and task.")
        else:
            new_session = {
                "subject": subject.strip(),
                "task": task.strip(),
                "minutes": int(minutes),
                "date": session_date.isoformat(),
                "recorded_at": datetime.now().isoformat(timespec="seconds")
            }

            sessions.append(new_session)
            history[username] = sessions
            save_history(history)

            st.success("Study session saved!")
            st.rerun()

    st.divider()
    st.markdown("### 📊 Your Study Summary")

    if not sessions:
        st.info("No sessions recorded yet. Save your first study session above.")
        return

    df = pd.DataFrame(sessions)
    df["minutes"] = pd.to_numeric(df["minutes"], errors="coerce").fillna(0)

    total_minutes = int(df["minutes"].sum())
    today_sessions = df[df["date"] == date.today().isoformat()]
    today_minutes = int(today_sessions["minutes"].sum())

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sessions", len(df))
    col2.metric("Total Focus Time", f"{total_minutes} min")
    col3.metric("Today's Focus", f"{today_minutes} min")

    st.markdown("### 📅 Session Records")
    st.dataframe(
        df[["date", "subject", "task", "minutes"]],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### 📈 Focus Time by Subject")
    subject_summary = (
        df.groupby("subject", as_index=False)["minutes"]
        .sum()
        .sort_values("minutes", ascending=False)
    )
    st.bar_chart(subject_summary.set_index("subject"))

    csv_data = df[["date", "subject", "task", "minutes"]].to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        "⬇️ Download Session History",
        data=csv_data,
        file_name="study_session_history.csv",
        mime="text/csv"
    )

    st.caption(
        "Sessions are recorded when you save them here. "
        "This version does not automatically import completed Pomodoro sessions."
    )
