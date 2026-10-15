
import streamlit as st
import pandas as pd
import datetime

def study_export():
    st.subheader("📥 Export Study Plan")
    st.write("Download your study tasks and deadlines as a CSV file.")

    profile = st.session_state.get("user_profile", {})
    tasks = profile.get("tasks", [])
    goals = profile.get("goals", [])

    export_data = []

    for task in tasks:
        export_data.append({
            "Task": task.get("task", task.get("Task", "Untitled")),
            "Subject": task.get("subject", "General"),
            "Deadline": task.get("deadline", task.get("Deadline", "")),
            "Difficulty": task.get("difficulty", "Medium"),
            "Completed": task.get("done", task.get("Completed", False)),
            "Required Sessions": task.get(
                "pomodoro_sessions",
                task.get("PomodoroSessionsRequired", 1)
            ),
            "Source": "Daily Planner"
        })

    for goal in goals:
        export_data.append({
            "Task": goal.get("Task", "Untitled"),
            "Subject": "General",
            "Deadline": goal.get("Deadline", ""),
            "Difficulty": "Medium",
            "Completed": goal.get("Completed", False),
            "Required Sessions": goal.get("PomodoroSessions", 1),
            "Source": "To-Do List"
        })

    if not export_data:
        st.info("No tasks found. Add tasks before exporting your study plan.")
        return

    df = pd.DataFrame(export_data)

    st.markdown("### 👀 Preview")
    st.dataframe(df, use_container_width=True, hide_index=True)

    csv_data = df.to_csv(index=False).encode("utf-8-sig")
    filename = f"study_plan_{datetime.date.today().isoformat()}.csv"

    st.download_button(
        label="⬇️ Download Study Plan (CSV)",
        data=csv_data,
        file_name=filename,
        mime="text/csv",
        use_container_width=True
    )

    st.success("Your study plan is ready to download.")
