
# 📚 Smart Study Buddy

**Smart Study Buddy** is a Python-based student productivity application built with Streamlit. It helps students organize their studies, manage their time, track personal goals, and reflect on their mood through a simple, interactive interface.

The project combines study planning and productivity tools in one application to encourage consistent study habits and better time management.

## ✨ Features

### 🔐 User Authentication
- User registration and login functionality.
- JSON-based user data storage.
- SHA-256 password hashing.

### 📅 Study Planner
- Organize study activities.
- Plan learning sessions and daily tasks.
- Keep study-related activities structured.

### ⏱️ Pomodoro Timer
- Use focused study sessions and breaks.
- Encourage productive study routines.
- Support better time management.

### 🎯 Goal Tracking
- Set personal study goals.
- Monitor progress toward learning objectives.
- Build consistent study habits.

### 😊 Mood Tracking
- Record mood-related information.
- Explore text-based mood analysis using TextBlob.
- Encourage reflection on study routines and well-being.

### 👤 User Profile
- Provide a personalized application experience.
- Keep user-related information organized.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Interactive web interface |
| JSON | Local user data storage |
| hashlib (SHA-256) | Password hashing |
| TextBlob | Text-based mood analysis |
| Git & GitHub | Version control |

## 📂 Project Structure

```text
Smart-Study-Buddy/
├── app.py
├── users.json
├── requirements.txt
└── README.md
```

*Note: Adjust the filenames and folders to match your actual repository. Do not upload real user credentials or private data from `users.json`.*

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or a compatible Python version.
- pip package manager.
- Git (optional, for cloning the repository).

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/Smart-Study-Buddy.git
cd Smart-Study-Buddy
```

Replace the URL with your actual GitHub repository URL.

### 2. Create a Virtual Environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

If `requirements.txt` is available:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Otherwise, install the packages required by your application:

```bash
pip install streamlit textblob
```

### 4. Run the Application

If your main application file is `app.py`:

```bash
streamlit run app.py
```

If your main file has a different name, replace `app.py` with the correct filename.

## 🧠 How It Works

1. The user opens the application through the Streamlit interface.
2. The user registers or logs in.
3. User-related information is handled using the application's JSON storage.
4. The user accesses study planning, goals, mood tracking, and productivity features.
5. The Pomodoro timer supports focused study sessions and breaks.
6. TextBlob can be used to analyze text-based mood information.

## 🔒 Security Considerations

- SHA-256 hashing is used for password-related functionality.
- Plain-text passwords should never be stored in the user data file.
- Plain SHA-256 hashing is not recommended for production password storage because it is not designed to resist password cracking. A dedicated password-hashing algorithm, such as Argon2 or bcrypt, should be used for production applications.
- JSON-based local storage is suitable for learning and prototyping but needs additional access controls and protection for multi-user production use.

## 🔮 Future Enhancements

- [ ] Add reminders for upcoming study sessions.
- [ ] Improve study progress visualizations.
- [ ] Add weekly and monthly productivity reports.
- [ ] Improve authentication and password security.
- [ ] Add persistent session management.
- [ ] Expand personalized study recommendations.
- [ ] Improve the user interface and mobile responsiveness.

These enhancements are potential future improvements, not claims of completed functionality.

## 📖 Learning Outcomes

Through this project, I explored:

- Python application development.
- Building interactive applications with Streamlit.
- User authentication and JSON data handling.
- Password hashing fundamentals.
- Text-based sentiment and mood analysis.
- Study planning and productivity feature development.

## 👩‍💻 Author

**Avantika Kashyap**

B.Tech Computer Science and Engineering  
Specialization: Artificial Intelligence and Machine Learning  
Haridwar University

## 📄 License

If you want others to reuse or modify this project, consider adding an appropriate open-source license, such as the MIT License, after deciding how you want the project to be shared.
