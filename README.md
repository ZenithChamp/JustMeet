# JustMeet
JustMeet
# 📍 JustMeet

JustMeet is a lightweight, Python/Flask-powered web platform designed for university students to synchronize their timetables with friends. Instead of constantly messaging people to ask if they are free, JustMeet aggregates your friend group's schedules to instantly show you who is free right now, how long their break lasts, and their likely campus location based on their class venues.

## ⚡ Core Features

*   **Friend-Group Timetable Matching:** Compares your schedule against your friend list to instantly display overlapping free windows.
*   **Real-Time Status Indicators:** Check who is currently free or stuck in a lecture slot at any given minute.
*   **Duration Tracking:** Displays exactly how much time is left before your friend's next class starts.
*   **Campus Location Anchoring:** Uses the venue data embedded in your friends' timetables to show where they are on campus (e.g., SJT, TT, SMV) during or between classes.

---

## 🛠️ Architecture & Tech Stack

The application is built as a modular, monolithic Python web application utilizing template-driven rendering:

*   **Backend Engine:** Python with **Flask** (`app.py`) handling user routing, session logic, and timetable comparison algorithms.
*   **Database Controller:** Custom Python database interface layer (`db.py`) managing user registration, secure login validation, and friend relationships.
*   **Frontend UI:** Clean, responsive semantic HTML5 templates (`home.html`, `login.html`, `reg.html`, `profile.html`, `timetable.html`) designed for fast asset loading.

---

## 📁 Repository Structure

```text
JustMeet/
├── app.py              # Main Flask application containing routing and matching logic
├── db.py               # Database configuration, helper functions, and schemas
├── home.html           # Main dashboard displaying your friend list and their live free/busy status
├── timetable.html      # Timetable input and visualization portal (slots, times, and buildings)
├── profile.html        # User profile, friend management, and circle configurations
├── login.html          # Secure login interface
├── reg.html            # User onboarding and registration setup
└── start_justmeet.bat  # Automated local environment execution script
```

---

## ⚙️ How It Works (The Logic)

1. **Timetable Parsing:** Users input their daily class slots, timing windows, and respective building locations (e.g., Slot A1 in SJT) into `timetable.html`.
2. **Relationship Mapping:** Your friend circle is managed through `profile.html` and linked in `db.py`.
3. **Live Comparison:** When you open `home.html`, the backend (`app.py`) fetches the current system day and time, cross-references it with your friends' active schedules, and extracts:
   * Whether they are currently marked as "Free".
   * The delta time until their next upcoming class slot.
   * Their current or last recorded class building location.

---

## 💻 Local Setup & Execution

The project includes an automated launch script for rapid local deployment.

### Prerequisites
* Python 3.x installed on your local machine.
* Flask package dependency installed (`pip install flask`).

### Launch Steps
1. Clone this repository to your local system:
   ```bash
   git clone https://github.com
   cd JustMeet
   ```
2. Double-click the execution script to launch the local server instantly:
   ```bash
   start_justmeet.bat
   ```
3. Open your web browser and navigate to:
   ```text
   http://127.0.0.1:5000
   ```
