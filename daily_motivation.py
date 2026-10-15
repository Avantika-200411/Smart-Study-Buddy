import streamlit as st
import random

def daily_motivation():
    quotes = [
        "Believe in yourself and all that you are.",
        "Start where you are. Use what you have. Do what you can.",
        "Push yourself, because no one else is going to do it for you.",
        "Small steps every day lead to big results.",
        "You are capable of amazing things."
    ]
    st.markdown("🌟 **Daily Motivation:**")
    st.info(random.choice(quotes))
