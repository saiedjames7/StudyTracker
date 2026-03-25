import csv
import os
import hashlib
from datetime import datetime, date, timedelta

# File paths
USERS_FILE = "users.csv"
SESSIONS_FILE = "sessions.csv"

# CSV column headers
USER_FIELDS = ["username", "password_hash", "created_at"]
SESSION_FIELDS = ["session_id", "username", "subject", "duration_minutes", "date", "notes", "goal_minutes"]

# Converts the Password to a Hash
def hashPassword(password: str) -> str:
    #Hash a password using SHA-256. Never store plain-text passwords.#
    return hashlib.sha256(password.encode()).hexdigest()

def generate_session_id() -> str:
    #Generate a unique session ID based on current timestamp.#
    return datetime.now().strftime("%Y%m%d%H%M%S%f")

def checksIfFileExists():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=USER_FIELDS)
            writer.writeheader()

    if not os.path.exists(SESSIONS_FILE):
        with open(SESSIONS_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=SESSION_FIELDS)
            writer.writeheader()

def createUser(username: str, password: str) -> tuple[bool, str]:

    # Input validation - checking before writing to CSV
    if len(username.strip()) < 3:
        return False, "Username must be at least 3 characters."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    if " " in username:
        return False, "Username cannot contain spaces."

    # Check username is not already taken
    existing = readAllUsers()
    for user in existing:
        if user["username"].lower() == username.lower():
            return False, "Username already exists. Please choose another."

    # Write new user to CSV
    new_user = {
        "username": username.strip(),
        "password_hash": hashPassword(password),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(USERS_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=USER_FIELDS)
        writer.writerow(new_user)

    return True, "Account created successfully!"

def readAllUsers() -> list[dict]:
    #READ operation: Return all users from CSV as a list of dicts.
    checksIfFileExists()
    with open(USERS_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)

def verifyLogin(username: str, password: str) -> tuple[bool, str]:
    # Check username + password against stored hash. Returns (success: bool, message: str).

    if not username or not password:
        return False, "Please enter both username and password."

    users = readAllUsers()
    hashed = hashPassword(password)

    for user in users:
        if user["username"].lower() == username.lower():
            if user["password_hash"] == hashed:
                return True, "Login successful!"
            else:
                return False, "Incorrect password."

    return False, "Username not found."

def createSession(username: str, subject: str, duration: int,
                   session_date: str, notes: str, goal: int) -> tuple[bool, str]:
    # Add a new study session for the logged-in user. Validates all inputs before writing to CSV.

    # Input validation
    if not subject.strip():
        return False, "Subject cannot be empty."
    if duration <= 0 or duration > 1440:
        return False, "Duration must be between 1 and 1440 minutes."
    if goal < 0 or goal > 1440:
        return False, "Goal must be between 0 and 1440 minutes."

    # Validate date format
    try:
        datetime.strptime(session_date, "%Y-%m-%d")
    except ValueError:
        return False, "Date must be in YYYY-MM-DD format."

    new_session = {
        "session_id": generate_session_id(),
        "username": username,
        "subject": subject.strip(),
        "duration_minutes": duration,
        "date": session_date,
        "notes": notes.strip(),
        "goal_minutes": goal
    }

    with open(SESSIONS_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SESSION_FIELDS)
        writer.writerow(new_session)

    return True, "Session logged successfully!"

def readUserSessions(username: str) -> list[dict]:
    # Return all sessions belonging to the logged-in user. Sorted by date descending (most recent first).
    
    checksIfFileExists()
    with open(SESSIONS_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        sessions = [row for row in reader if row["username"] == username]

    # Sort by date, most recent first
    sessions.sort(key=lambda s: s["date"], reverse=True)
    return sessions

def updateSessions(session_id: str, username: str, subject: str,
                   duration: int, session_date: str, notes: str, goal: int) -> tuple[bool, str]:

    if not subject.strip():
        return False, "Subject cannot be empty."
    if duration <= 0 or duration > 1440:
        return False, "Duration must be between 1 and 1440 minutes."

    all_sessions = []
    found = False

    with open(SESSIONS_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["session_id"] == session_id and row["username"] == username:
                row["subject"] = subject.strip()
                row["duration_minutes"] = duration
                row["date"] = session_date
                row["notes"] = notes.strip()
                row["goal_minutes"] = goal
                found = True
            all_sessions.append(row)

    if not found:
        return False, "Session not found."

    with open(SESSIONS_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SESSION_FIELDS)
        writer.writeheader()
        writer.writerows(all_sessions)

    return True, "Session updated successfully!"

def deleteSession(session_id: str, username: str) -> tuple[bool, str]:
    # Remove a session by its ID. Only deletes sessions belonging to the currently logged-in user (security check).
    
    all_sessions = []
    found = False

    with open(SESSIONS_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["session_id"] == session_id and row["username"] == username:
                found = True  # Skip this row (effectively deleting it)
            else:
                all_sessions.append(row)

    if not found:
        return False, "Session not found or permission denied."

    with open(SESSIONS_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SESSION_FIELDS)
        writer.writeheader()
        writer.writerows(all_sessions)

    return True, "Session deleted."

def getStats(username: str) -> dict:

    # Calculates Summary Statistics 
    sessions = readUserSessions(username)

    if not sessions:
        return {
            "total_minutes": 0,
            "session_count": 0,
            "top_subject": "N/A",
            "current_streak": 0,
            "subjects": {}
        }

    total_minutes = sum(int(s["duration_minutes"]) for s in sessions)
    session_count = len(sessions)

    # Count minutes per subject
    subjects = {}
    for s in sessions:
        subj = s["subject"]
        subjects[subj] = subjects.get(subj, 0) + int(s["duration_minutes"])

    top_subject = max(subjects, key=subjects.get)

    # Calculate current study streak (consecutive days with at least one session)
    study_dates = set(s["date"] for s in sessions)
    streak = 0
    check_date = date.today()

    while str(check_date) in study_dates:
        streak += 1
        check_date -= timedelta(days=1)

    return {
        "total_minutes": total_minutes,
        "session_count": session_count,
        "top_subject": top_subject,
        "current_streak": streak,
        "subjects": subjects
    }
