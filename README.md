# 📚 Smart Study Buddy

**Smart Study Buddy** is a Python-based student productivity application built using Streamlit. It brings study planning, time management, goal tracking, mood analysis, and productivity tools together in one interactive application.

The project is designed to help students organize daily tasks, maintain consistent study habits, monitor progress, and develop a more structured learning routine.

## ✨ Features

### 🔐 User Authentication
- User registration and login functionality.
- JSON-based user data handling.
- SHA-256 password hashing.
- Password change functionality.

### 📅 Daily Study Planner
- Organize daily study activities.
- Plan learning sessions and tasks.
- Manage to-do lists and study priorities.
- Support structured study routines.

### ⏱️ Pomodoro Timer
- Organize focused study sessions and breaks.
- Encourage concentration and time management.
- Support consistent study habits.

### 🎯 Study Goals
- Set personal study goals.
- Track progress toward learning objectives.
- Support daily goal management.

### 😊 Mood Analyzer
- Record mood-related information.
- Use TextBlob for text-based sentiment analysis.
- Encourage reflection on mood and study routines.

### 👤 User Profile
- Maintain user-related profile information.
- Support a personalized application experience.

### 📊 Productivity Analytics
- Review study-related activity and productivity information.
- Track study history.
- Generate weekly reports.
- Monitor study streaks and achievements.

### 🗓️ Smart Scheduling and Reminders
- Organize study schedules.
- Support study reminders.
- Help students manage their planned activities.

### 📤 Study Export
- Export study-related information where supported by the application.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Interactive web interface |
| JSON | Local data storage |
| `hashlib` (SHA-256) | Password hashing |
| TextBlob | Text-based sentiment analysis |
| Git | Version control |
| GitHub | Source code hosting |

## 📂 Project Structure

```text
Smart-Study-Buddy/
├── app.py
├── ToDo_list.py
├── change_password.py
├── daily_motivation.py
├── daily_planner.py
├── daily_study_goals.py
├── home_dashboard.py
├── mood_analyzer.py
├── pomodoro_timer.py
├── productivity_analytics.py
├── smart_scheduler.py
├── study_achievements.py
├── study_export.py
├── study_history.py
├── study_reminders.py
├── study_streak.py
├── user_profile.py
├── weekly_report.py
├── .gitignore
└── README.md
```

*Note: Local data files, profile images, virtual environments, and other generated files may be excluded from GitHub through `.gitignore`.*

## 🚀 Getting Started

### Prerequisites

- Python installed on your computer.
- pip package manager.
- Git (for cloning the repository).

### 1. Clone the Repository

```bash
git clone https://github.com/Avantika-200411/Smart-Study-Buddy.git
cd Smart-Study-Buddy
```

### 2. Create a Virtual Environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell does not allow the activation script to run, you can use the virtual environment's Python executable directly.

### 3. Install Dependencies

If your repository contains a `requirements.txt` file, run:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If there is no `requirements.txt`, install the packages required by your project. For the core Streamlit interface and TextBlob functionality, you can start with:

```bash
pip install streamlit textblob
```

Install any additional packages required by your other project modules.

### 4. Run the Application

From the project directory, run:

```bash
streamlit run app.py
```

Streamlit will display a local URL in your terminal. Open that URL in your browser to use the application.

## 🧠 How It Works

1. The user opens Smart Study Buddy through the Streamlit interface.
2. The user registers or logs in.
3. The application provides access to study planning and productivity features.
4. The user can manage tasks, study goals, and focused study sessions.
5. Mood analysis can process text-based input using TextBlob.
6. Study-related information can be reviewed through history, reports, streaks, and analytics features.

The exact behavior of each feature depends on its implementation in the corresponding Python module.

## 🔒 Security Considerations

- The application uses SHA-256 hashing for password-related functionality.
- Passwords should never be stored as plain text.
- Plain SHA-256 is not recommended for production password storage. Dedicated password-hashing algorithms such as Argon2 or bcrypt are better suited to this purpose.
- JSON-based local storage is useful for learning and prototyping but may need stronger access controls for production use.
- Do not upload passwords, private user information, API keys, or other sensitive data to a public repository.
- Keep local user data and generated files excluded through `.gitignore` where appropriate.

## 🔮 Future Enhancements

- Improve password security and authentication.
- Expand personalized study recommendations.
- Enhance productivity visualizations.
- Add more detailed study statistics and reports.
- Improve reminder and scheduling options.
- Enhance mobile responsiveness and user experience.
- Explore deployment so the application can be accessed online.

These are potential future improvements and are not presented as completed features.

## 📖 Learning Outcomes

Through this project, I explored:

- Python application development.
- Building interactive applications with Streamlit.
- Organizing a project into multiple Python modules.
- User authentication and JSON data handling.
- Password hashing fundamentals.
- Text-based sentiment analysis using TextBlob.
- Study planning and productivity feature development.
- Version control and project hosting using Git and GitHub.

## 👩‍💻 Author

**Avantika Kashyap**

B.Tech in Computer Science and Engineering  
Specialization: Artificial Intelligence and Machine Learning  
Haridwar University

## 📄 License

No license is specified in this README. If you want others to reuse, distribute, or modify the project, choose and add an appropriate open-source license.
