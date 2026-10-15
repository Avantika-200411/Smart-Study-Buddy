import streamlit as st
from PIL import Image
import os
import json

USER_FILE = "users.json"

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)


PROFILE_PIC_DIR = "profile_pics"

def profile():
    st.write("### \U0001F464 Your Profile")
    user = st.session_state.username
    profile_data = st.session_state.user_profile

    # Create folder if not exists
    if not os.path.exists(PROFILE_PIC_DIR):
        os.makedirs(PROFILE_PIC_DIR)

    profile_pic_path = os.path.join(PROFILE_PIC_DIR, f"{user}.png")
    pic_exists = os.path.exists(profile_pic_path)

    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = False  # Default no edit mode

    # Display profile pic next to name in header
    col1, col2 = st.columns([1, 4])
    with col1:
        if pic_exists:
            img = Image.open(profile_pic_path)
            st.image(img, width=80)
        else:
            st.write("⚠️ Profile picture not found.")
    with col2:
        st.markdown(f"## {profile_data.get('name', '')}")

    # Show age
    st.markdown(f"**Age:** {profile_data.get('age', '')}")

    # Show goals in nice style, with big font and maybe some color
    goals = profile_data.get("goals", [])
    if goals:
        st.markdown("### 🎯 Your Life Goals")
        for g in goals:
            goal_text = g.get("Goal", "")
            # Beautiful styling for motivation
            st.markdown(f"<p style='font-size:22px; color:#4B0082; font-weight:bold; font-family: Arial, sans-serif;'>{goal_text}</p>", unsafe_allow_html=True)
    else:
        st.write("No goals set yet.")

    # Edit mode toggle button
    if st.session_state.edit_mode:
        with st.form("profile_form"):
            name = st.text_input("Name", value=profile_data.get("name", ""))
            age = st.number_input("Age", min_value=10, max_value=100, value=profile_data.get("age", 18))

            # Upload photo only in edit mode, and show uploader only if no pic yet or user wants to change
            uploaded_file = None
            if not pic_exists:
                uploaded_file = st.file_uploader("Upload Profile Picture (PNG/JPG)", type=["png", "jpg", "jpeg"])
            else:
                change_pic = st.checkbox("Change Profile Picture?")
                if change_pic:
                    uploaded_file = st.file_uploader("Upload New Profile Picture (PNG/JPG)", type=["png", "jpg", "jpeg"])

            # Add goal editing textarea here
            goals_text = "\n".join([g.get("Goal", "") for g in goals])
            edited_goals = st.text_area("Edit Your Life Goals (one per line):", value=goals_text, height=150)

            submitted = st.form_submit_button("Save Profile")

            if submitted:
                # Save profile data
                st.session_state.user_profile["name"] = name
                st.session_state.user_profile["age"] = age

                # Save profile pic if uploaded
                if uploaded_file is not None:
                    img = Image.open(uploaded_file)
                    img.save(profile_pic_path)
                    st.success("Profile picture updated!")

                # Save goals from textarea
                new_goals_list = [{"Goal": goal.strip(), "Deadline": "", "Completed": False} 
                                  for goal in edited_goals.split("\n") if goal.strip()]
                st.session_state.user_profile["goals"] = new_goals_list

                # Save in user db and file
                user = st.session_state.username
                st.session_state.user_db[user]["name"] = name
                st.session_state.user_db[user]["age"] = age
                st.session_state.user_db[user]["goals"] = new_goals_list
                save_users(st.session_state.user_db)

                st.success("Profile and goals updated!")
                st.session_state.edit_mode = False
                st.rerun()

        if st.button("Cancel Edit"):
            st.session_state.edit_mode = False
            st.rerun()

    else:
        if st.button("✏️ Edit Profile"):
            st.session_state.edit_mode = True
            st.rerun()

