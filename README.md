---
title: CarePoint
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: gradio
app_file: app.py
pinned: false
---

# 🏥 Care Point: Doctor Appointment Scheduler

[![Live Demo](https://img.shields.io/badge/Demo-Live-brightgreen.svg)](YOUR_VERCEL_OR_NETLIFY_LINK)
[![GitHub Repository](https://img.shields.io/badge/Code-GitHub-blue.svg)](https://github.com/Tanisha-negi/Care-point-appointment-scheduler.git)

## 🌟 Overview

**Care Point** is a full-stack web application designed to demonstrate the construction of a modern medical scheduling system. It allows patients to easily book, manage, and view appointments online, while giving medical staff a centralized system to manage schedules and patient data.

This project was built to showcase proficiency in connecting a robust backend with an interactive, responsive frontend.

---

## ✨ Key Features

* **Responsive Frontend:** A clean, user-friendly interface for easy navigation and booking on any device.
* **Appointment Booking:** Patients can select a doctor, view their availability in real-time, and book an open time slot.
* **Doctor Profiles:** Displays individual doctor credentials, specialization, and working hours.
* **Data Persistence:** Securely stores and retrieves doctor, patient, and appointment data.
* **Form Validation:** Client-side and server-side validation to ensure data integrity.

---

## 💻 Tech Stack

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend Framework** | **Python 3** | Core language for all server logic and data processing. |
| **Web Framework** | **Flask** | Lightweight server to manage routing, API endpoints, and template rendering. |
| **Database** | **SQLite** | Storage for appointments, doctor data, and patient information. |
| **Data Access** | **SQLAlchemy** | Managing database interactions. |
| **Authentication** |	**Flask-Login** |	Secure user registration, session management, and login system for patients/staff.
| **Email Services** |	**Flask-Mail** |	Handling automated communications for appointment confirmations and password resets.
| **Frontend** | **HTML5, CSS3, JavaScript** | Building the user interface and handling client-side interactions. |

---

## 🚀 Setup and Local Run Guide

Follow these steps to set up and run the **Care Point** application on your local machine.

### 1. Get the Code

Clone the project from GitHub and move into the project directory:

```bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/Care-Point-Appointment-Scheduler.git](https://github.com/Tanisha-negi/Care-point-appointment-scheduler.git)
cd Care-Point-Appointment-Scheduler

2. Environment Setup
It is required to use a virtual environment (venv) to isolate dependencies.

Create and activate the environment:

Bash

python -m venv venv
# Windows: .\venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
Install dependencies: (Ensure you have a complete requirements.txt file for this step)

Bash

pip install -r requirements.txt


3. Run the Application
Set the Flask environment variable: (Use set for Windows Command Prompt/PowerShell; export for macOS/Linux)

Bash

# Windows:
set FLASK_APP=app.py 

# macOS/Linux:
export FLASK_APP=app.py
Start the local development server:

Bash

flask run
The application will now be running locally. Open your web browser and navigate to http://127.0.0.1:5000/.

