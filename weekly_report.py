
import streamlit as st
import pandas as pd
import json
import os
from datetime import date, timedelta


def weekly_report():
    st.subheader("📊 Weekly Study Report")

    username = st.session_state.get("username", "")
    if not username:
        st.warning("Please log in first.")
        return

    history_file = "study_history.json"

    if not os.path.exists(history_file):
        st.info("No study history found. Complete a focus session first.")
        return

    try:
        with open(history_file, "r", encoding="utf-8") as file:
            history = json.load(file)
    except (json.JSONDecodeError, OSError):
        st.error("Could not read study history.")
        return

    sessions = history.get(username, [])

    if not sessions:
        st.info("No sessions recorded yet.")
        return

    df = pd.DataFrame(sessions)

    required_columns = {"date", "subject", "task", "minutes"}
    if not required_columns.issubset(df.columns):
        st.error("Study history is missing required fields.")
        return

    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    df["minutes"] = pd.to_numeric(df["minutes"], errors="coerce").fillna(0)

    today = date.today()
    week_start = today - timedelta(days=6)

    weekly_df = df[
        (df["date"] >= week_start) &
        (df["date"] <= today)
    ].copy()

    st.caption(
        f"Report period: {week_start.strftime('%d %b %Y')} – "
        f"{today.strftime('%d %b %Y')}"
    )

    total_minutes = int(weekly_df["minutes"].sum())
    total_sessions = len(weekly_df)
    study_days = weekly_df["date"].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("Focus Time", f"{total_minutes} min")
    col2.metric("Completed Sessions", total_sessions)
    col3.metric("Study Days", int(study_days))

    if weekly_df.empty:
        st.info("No study sessions were recorded in the last 7 days.")
        return

    st.divider()
    st.markdown("### 📅 Daily Focus Time")

    days = [week_start + timedelta(days=i) for i in range(7)]
    daily_totals = (
        weekly_df.groupby("date")["minutes"]
        .sum()
        .to_dict()
    )

    daily_df = pd.DataFrame({
        "Date": [day.strftime("%a, %d %b") for day in days],
        "Focus Minutes": [int(daily_totals.get(day, 0)) for day in days]
    })

    st.bar_chart(daily_df.set_index("Date"))

    st.markdown("### 📚 Focus Time by Subject")

    subject_df = (
        weekly_df.groupby("subject", as_index=False)["minutes"]
        .sum()
        .sort_values("minutes", ascending=False)
        .rename(columns={"minutes": "Focus Minutes"})
    )

    st.bar_chart(subject_df.set_index("subject"))

    st.markdown("### 📝 Sessions This Week")

    display_df = weekly_df[
        ["date", "subject", "task", "minutes"]
    ].sort_values("date", ascending=False)

    display_df["date"] = display_df["date"].astype(str)

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    csv_data = display_df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        "⬇️ Download Weekly Report",
        data=csv_data,
        file_name=f"weekly_study_report_{today.isoformat()}.csv",
        mime="text/csv"
    )
