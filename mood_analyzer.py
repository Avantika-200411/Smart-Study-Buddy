
import streamlit as st
from textblob import TextBlob
import datetime


def mood_analyzer():
    st.subheader("😊 Smart Mood Analyzer")
    st.write(
        "Share how you feel, and get a study suggestion "
        "based on your text."
    )

    user_input = st.text_area(
        "How are you feeling today?",
        placeholder="Example: I feel tired, but I want to finish my Python assignment.",
        key="mood_text_input"
    )

    if st.button("🔍 Analyze Mood", type="primary"):
        if not user_input.strip():
            st.warning("Please enter some text to analyze.")
            return

        blob = TextBlob(user_input)
        polarity = blob.sentiment.polarity

        # Analyze sentiment and recommend a study approach
        if polarity > 0.15:
            mood = "Positive"
            st.success("😊 Your text sounds positive!")
            st.markdown("### 🎯 Your study recommendation")
            st.write(
                "Use your positive energy for a challenging topic "
                "or an important pending task."
            )
            suggested_duration = 25

        elif polarity < -0.15:
            mood = "Low or Negative"
            st.info(
                "💙 Your text sounds like you may be having a difficult day. "
                "Sentiment analysis can make mistakes, so choose what feels right for you."
            )
            st.markdown("### 🌿 Your study recommendation")
            st.write(
                "Consider a short break, some water, or a lighter revision task. "
                "If you feel ready, try a short 10-minute study session."
            )
            suggested_duration = 10

        else:
            mood = "Neutral"
            st.info("😌 Your text sounds relatively neutral.")
            st.markdown("### 📚 Your study recommendation")
            st.write(
                "Choose one manageable task, remove distractions, "
                "and work through it step by step."
            )
            suggested_duration = 20

        st.metric("Suggested focus duration", f"{suggested_duration} minutes")

        # Suggest an existing pending task, if available
        profile = st.session_state.get("user_profile", {})
        tasks = profile.get("tasks", [])
        goals = profile.get("goals", [])

        pending_tasks = []

        for task in tasks:
            if not task.get("done", task.get("Completed", False)):
                pending_tasks.append(
                    task.get("task", task.get("Task", "Untitled task"))
                )

        for goal in goals:
            if not goal.get("Completed", False):
                pending_tasks.append(
                    goal.get("Task", "Untitled task")
                )

        if pending_tasks:
            st.markdown("### ✅ One task you could work on")
            st.write(pending_tasks[0])
        else:
            st.caption(
                "No pending tasks found. Add a task in your Daily Planner "
                "or To-Do List to get a task suggestion."
            )

        st.caption(
            f"Sentiment score: {polarity:.2f} | "
            f"Detected category: {mood}"
        )

        st.caption(
            "This is a basic text sentiment estimate, not a clinical "
            "assessment of your mood or mental health."
        )
