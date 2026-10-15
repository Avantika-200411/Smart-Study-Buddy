
import streamlit as st

st.set_page_config(
    page_title="Smart Study Buddy",
    page_icon="📚",
    layout="wide"
)

import datetime
import hashlib
import json
import os
import secrets
import extra_streamlit_components as stx

from user_profile import profile
from mood_analyzer import mood_analyzer
from daily_planner import daily_planner
from pomodoro_timer import pomodoro_timer
from ToDo_list import ToDo_list
from daily_motivation import daily_motivation
from productivity_analytics import productivity_analytics
from study_reminders import study_reminders
from smart_scheduler import smart_scheduler
from study_export import study_export
from study_history import study_history
from study_streak import study_streak
from weekly_report import weekly_report
from daily_study_goals import daily_study_goals
from study_achievements import study_achievements
from home_dashboard import home_dashboard
from change_password import change_password

USER_FILE = "users.json"

cookie_manager = stx.CookieManager(key="study_buddy_auth")


# ---------------- CUSTOM UI ----------------
def apply_custom_style():
    st.markdown("""
    <style>
    :root {
        --ink: #252047;
        --muted: #77748f;
        --purple: #7652d6;
        --purple-dark: #5736b5;
        --lavender: #f1edff;
        --line: #e9e4f7;
        --surface: #ffffff;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 85% 0%, rgba(202, 181, 255, .24), transparent 36%),
            linear-gradient(135deg, #fbfaff 0%, #f6f4ff 55%, #fbfaff 100%);
        color: var(--ink);
    }

    .block-container {
        max-width: 1320px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, h4 {
        color: var(--ink);
        letter-spacing: -.45px;
    }

    p, label, .stMarkdown, [data-testid="stCaptionContainer"] {
        color: inherit;
    }

    /* Main sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #211747 0%, #30205f 58%, #432778 100%);
        border-right: 1px solid rgba(255,255,255,.08);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.5rem;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {
        color: #f8f6ff;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] > label {
        color: #d8d0f3;
        font-size: .76rem;
        font-weight: 700;
        letter-spacing: .09em;
        text-transform: uppercase;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] {
        gap: 5px;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label {
        background: rgba(255,255,255,.055);
        border: 1px solid transparent;
        border-radius: 11px;
        padding: 9px 11px;
        transition: background .2s ease, border-color .2s ease;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label:hover {
        background: rgba(255,255,255,.13);
        border-color: rgba(255,255,255,.14);
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
        background: linear-gradient(100deg, rgba(167,139,250,.32), rgba(255,255,255,.10));
        border-color: rgba(221,214,254,.35);
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,.14);
    }

    /* Welcome and page hero cards */
    .hero-card {
        padding: 27px 30px;
        border-radius: 22px;
        margin-bottom: 24px;
        background: linear-gradient(115deg, #ffffff 0%, #f3efff 70%, #eee8ff 100%);
        border: 1px solid #e4dcff;
        box-shadow: 0 12px 35px rgba(74, 48, 135, .07);
    }

    .hero-card h1 {
        color: #30205f;
        margin: 0 0 8px;
        font-size: 2rem;
        line-height: 1.2;
    }

    .hero-card p {
        color: #77718e;
        margin: 0;
        font-size: 1rem;
    }

    .auth-shell {
        padding: clamp(22px, 4vw, 48px);
        border-radius: 28px;
        background: rgba(255,255,255,.94);
        border: 1px solid #e9e2fb;
        box-shadow: 0 24px 70px rgba(58, 36, 108, .12);
        margin: 1rem auto 2rem;
    }

    .auth-brand {
        color: #5f3ab8;
        font-size: 1rem;
        font-weight: 800;
        letter-spacing: .22em;
        margin-bottom: 1.6rem;
    }

    .auth-banner {
        min-height: 390px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: clamp(24px, 3vw, 42px);
        border-radius: 24px;
        background:
            radial-gradient(circle at 80% 20%, rgba(255,255,255,.5), transparent 24%),
            linear-gradient(145deg, #d9ccff 0%, #a88aef 46%, #7450ca 100%);
        color: white;
        overflow: hidden;
    }

    .auth-banner h1 {
        color: white;
        font-size: clamp(1.8rem, 3vw, 2.8rem);
        line-height: 1.1;
        margin: 0 0 16px;
    }

    .auth-banner p {
        color: #f7f2ff;
        font-size: 1rem;
        line-height: 1.65;
        margin: 0;
    }

    .auth-tag {
        display: inline-block;
        width: fit-content;
        margin-top: 24px;
        padding: 8px 13px;
        border: 1px solid rgba(255,255,255,.45);
        background: rgba(255,255,255,.16);
        color: white;
        border-radius: 999px;
        font-size: .83rem;
    }

    /* Metrics, forms and interactive controls */
    [data-testid="stMetric"] {
        background: rgba(255,255,255,.94);
        border: 1px solid var(--line);
        padding: 19px;
        border-radius: 18px;
        box-shadow: 0 7px 22px rgba(45, 29, 92, .045);
    }

    [data-testid="stMetricLabel"] {
        color: var(--muted);
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: var(--ink);
        font-weight: 750;
    }

    div[data-testid="stForm"] {
        background: #fff;
        padding: 24px;
        border-radius: 20px;
        border: 1px solid var(--line);
        box-shadow: 0 8px 24px rgba(45, 29, 92, .04);
    }

    input, textarea {
        border-radius: 11px !important;
    }

    div.stButton > button,
    div.stDownloadButton > button,
    [data-testid="stFormSubmitButton"] button {
        border-radius: 12px;
        font-weight: 700;
        min-height: 44px;
        border: 1px solid #d8ccfa;
        transition: transform .15s ease, box-shadow .15s ease;
    }

    div.stButton > button[kind="primary"],
    [data-testid="stFormSubmitButton"] button[kind="primary"] {
        background: linear-gradient(100deg, #7652d6, #9b73e8);
        color: #fff;
        border: none;
    }

    div.stButton > button:hover,
    div.stDownloadButton > button:hover,
    [data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-1px);
        box-shadow: 0 7px 16px rgba(99, 65, 181, .14);
    }

    [data-testid="stProgressBar"] > div > div {
        background: linear-gradient(90deg, #7955d8, #b39af7);
        border-radius: 999px;
    }

    [data-testid="stProgressBar"] > div {
        border-radius: 999px;
        background: #e9e3f8;
    }

    [data-testid="stAlert"] {
        border-radius: 14px;
    }

    hr {
        border-color: #e6e0f3;
        margin-top: 1.4rem;
        margin-bottom: 1.4rem;
    }

    @media (max-width: 800px) {
        .block-container { padding: 1rem; }
        .auth-banner { min-height: 230px; margin-top: 20px; }
        .hero-card { padding: 22px; }
    }
    </style>
    """, unsafe_allow_html=True)

apply_custom_style()

# ---------------- AUTHENTICATION ----------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password, hashed):
    return secrets.compare_digest(hash_password(password), hashed)


def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    try:
        with open(USER_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def save_users(users):
    with open(USER_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)


def set_user_session(username, data, users):
    st.session_state.logged_in = True
    st.session_state.username = username
    st.session_state.user_db = users
    st.session_state.user_profile = {
        "name": data.get("name", ""), "age": data.get("age", 18),
        "profile_pic": data.get("profile_pic", ""),
        "goals": data.get("goals", []), "tasks": data.get("tasks", [])
    }


def restore_login():
    try:
        token = cookie_manager.get(cookie="study_buddy_token")
    except Exception:
        return False
    if not token:
        return False
    users = load_users()
    for username, data in users.items():
        if data.get("login_token") == token:
            set_user_session(username, data, users)
            return True
    return False


def logout():
    users = load_users()
    username = st.session_state.get("username", "")
    if username in users:
        users[username].pop("login_token", None)
        save_users(users)
    try:
        cookie_manager.delete("study_buddy_token")
    except Exception:
        pass
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.user_profile = {}
    st.session_state.user_db = load_users()
    st.rerun()

# ---------------- SESSION STATE ----------------
defaults = {"logged_in": False, "username": "", "user_db": load_users(), "show_signup": False, "user_profile": {}}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------- AUTH PAGES ----------------
def signup():
    st.markdown('<div class="auth-shell">', unsafe_allow_html=True)
    left, right = st.columns([1.05, 0.95], gap="large")

    with left:
        st.markdown('<div class="auth-brand">📚 SMART STUDY BUDDY</div>', unsafe_allow_html=True)
        st.markdown("## Create your account")
        st.caption("Set up your study space and start building a better routine.")

        with st.form("signup_form"):
            new_user = st.text_input("Username", key="signup_user")
            name = st.text_input("Full name", key="signup_name")
            age = st.number_input("Age", min_value=10, max_value=100, value=18, key="signup_age")
            new_pass = st.text_input("Password (minimum 8 characters)", type="password", key="signup_pass")
            confirm_pass = st.text_input("Confirm password", type="password", key="signup_confirm")
            submitted = st.form_submit_button("Create account", use_container_width=True, type="primary")

        if submitted:
            users = load_users()
            username = new_user.strip()
            if not username or not name.strip() or not new_pass:
                st.warning("Please complete all fields.")
            elif len(new_pass) < 8:
                st.warning("Use a password with at least 8 characters.")
            elif new_pass != confirm_pass:
                st.error("Passwords do not match.")
            elif username in users:
                st.warning("That username already exists. Please log in.")
            else:
                users[username] = {
                    "password": hash_password(new_pass),
                    "name": name.strip(),
                    "age": age,
                    "profile_pic": "",
                    "goals": [],
                    "tasks": []
                }
                save_users(users)
                st.session_state.user_db = users
                st.success("Account created. Choose Login from the sidebar to continue.")

    with right:
        st.markdown("""
        <div class="auth-banner">
            <div style="font-size:3rem; margin-bottom:18px;">✦</div>
            <h1>Your goals.<br>Your pace.<br>Your progress.</h1>
            <p>A calm, personal space to organize tasks, focus with a timer, and celebrate the progress you make every day.</p>
            <span class="auth-tag">PLAN • FOCUS • GROW</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def login():
    st.markdown('<div class="auth-shell">', unsafe_allow_html=True)
    left, right = st.columns([1.05, 0.95], gap="large")

    with left:
        st.markdown('<div class="auth-brand">📚 SMART STUDY BUDDY</div>', unsafe_allow_html=True)
        st.markdown("## Welcome back")
        st.caption("Sign in to continue your learning journey.")

        with st.form("login_form"):
            user = st.text_input("Username", key="login_user", placeholder="Enter your username")
            pw = st.text_input("Password", type="password", key="login_pass", placeholder="Enter your password")
            submitted = st.form_submit_button("Sign in", use_container_width=True, type="primary")

        if submitted:
            users = load_users()
            if user in users and verify_password(pw, users[user].get("password", "")):
                token = secrets.token_urlsafe(32)
                users[user]["login_token"] = token
                save_users(users)
                set_user_session(user, users[user], users)
                try:
                    cookie_manager.set(
                        "study_buddy_token",
                        token,
                        expires_at=datetime.datetime.now() + datetime.timedelta(days=1)
                    )
                except Exception:
                    pass
                st.rerun()
            else:
                st.error("Invalid username or password.")

        st.caption("Your study dashboard, tasks and progress in one place.")

    with right:
        st.markdown("""
        <div class="auth-banner">
            <div style="font-size:3rem; margin-bottom:18px;">✦</div>
            <h1>Make every<br>study session<br>count.</h1>
            <p>Plan your day, stay focused, and see your progress come together—one small step at a time.</p>
            <span class="auth-tag">YOUR PERSONAL STUDY COMPANION</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PAGE HEADER ----------------
def render_card(title, content_func):
    st.markdown(f'''<div class="hero-card"><h1>{title}</h1><p>Keep your learning organized, one session at a time.</p></div>''', unsafe_allow_html=True)
    content_func()

# ---------------- RESTORE LOGIN ----------------
if not st.session_state.logged_in:
    restore_login()

# ---------------- NAVIGATION ----------------
page_funcs = {
    "Home Dashboard": home_dashboard,
    "Profile": profile,
    "Mood Analyzer": mood_analyzer,
    "Daily Planner": daily_planner,
    "Pomodoro Timer": pomodoro_timer,
    "ToDo_list": ToDo_list,
    "Productivity Analytics": productivity_analytics,
    "Study Reminders": study_reminders,
    "Smart Scheduler": smart_scheduler,
    "Study Plan Export": study_export,
    "Study Session History": study_history,
    "Daily Study Streak": study_streak,
    "Weekly Study Report": weekly_report,
    "Daily Study Goals": daily_study_goals,
    "Study Achievements": study_achievements,
    "Change Password": change_password,
}

navigation_groups = {
    "🏠 Home": ["Home Dashboard"],
    "📖 Study Tools": ["Daily Planner", "Pomodoro Timer", "ToDo_list", "Smart Scheduler", "Study Reminders"],
    "📊 Progress": ["Productivity Analytics", "Study Session History", "Daily Study Streak", "Weekly Study Report", "Daily Study Goals", "Study Achievements", "Study Plan Export"],
    "⚙️ Account": ["Profile", "Mood Analyzer", "Change Password"],
}

# ---------------- MAIN APP ----------------
if st.session_state.logged_in:
    st.sidebar.markdown("# 📚 Smart Study Buddy")
    st.sidebar.caption(f"Welcome, {st.session_state.username}")
    st.sidebar.caption("Your personal study space")
    st.sidebar.divider()
    section = st.sidebar.radio("YOUR WORKSPACE", list(navigation_groups.keys()), key="navigation_section")
    pages = [name for name in navigation_groups[section] if name in page_funcs]
    if section == "🏠 Home":
        page = "Home Dashboard"
    else:
        page = st.sidebar.radio("OPEN A TOOL", pages, key=f"pages_{section}")
    st.sidebar.divider()
    if st.sidebar.button("🚪 Log out", use_container_width=True, key="logout_button"):
        logout()
    render_card(page, page_funcs[page])
    st.divider()
    daily_motivation()
else:
    st.sidebar.markdown("# 📚 Smart Study Buddy")
    st.sidebar.caption("Your personal study companion")
    st.sidebar.divider()
    choice = st.sidebar.radio("ACCOUNT", ["Login", "Sign Up"], key="auth_navigation")
    if choice == "Sign Up":
        signup()
    else:
        login()
