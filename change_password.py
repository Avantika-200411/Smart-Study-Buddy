
import streamlit as st
import hashlib
import json
import os
import hmac

USER_FILE = "users.json"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def change_password():
    st.subheader("🔐 Change Password")

    username = st.session_state.get("username", "")

    if not username:
        st.warning("Please log in first.")
        return

    with st.form("change_password_form"):
        current_password = st.text_input(
            "Current Password",
            type="password"
        )

        new_password = st.text_input(
            "New Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm New Password",
            type="password"
        )

        submitted = st.form_submit_button(
            "Update Password",
            use_container_width=True
        )

    if not submitted:
        return

    if not current_password or not new_password or not confirm_password:
        st.warning("Please fill in all fields.")
        return

    if len(new_password) < 8:
        st.warning("New password must contain at least 8 characters.")
        return

    if new_password != confirm_password:
        st.error("New passwords do not match.")
        return

    if not os.path.exists(USER_FILE):
        st.error("User database was not found.")
        return

    try:
        with open(USER_FILE, "r", encoding="utf-8") as file:
            users = json.load(file)
    except (json.JSONDecodeError, OSError):
        st.error("Could not read the user database.")
        return

    user_data = users.get(username)

    if not user_data:
        st.error("User account was not found.")
        return

    stored_hash = user_data.get("password", "")
    entered_hash = hash_password(current_password)

    if not hmac.compare_digest(entered_hash, stored_hash):
        st.error("Current password is incorrect.")
        return

    user_data["password"] = hash_password(new_password)

    try:
        with open(USER_FILE, "w", encoding="utf-8") as file:
            json.dump(users, file, indent=4)
    except OSError:
        st.error("Unable to save the new password.")
        return

    st.session_state.user_db = users

    st.success("Password updated successfully!")
    st.info("Your existing login session remains active.")
