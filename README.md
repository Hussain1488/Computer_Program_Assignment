# Flask Carbon Footprint Monitoring Tool

## Overview

This project is a web-based application developed using Flask that helps businesses monitor and reduce their carbon footprints. It calculates emissions based on user inputs, generates reports, and offers suggestions for improvement.

---

## Features

- **User Authentication**: Secure login and registration system.
- **Input & Calculation**: Collects data on energy use, waste, and travel, and calculates carbon emissions.
- **Reports**: Generates downloadable `.txt` reports with suggestions.
- **Dynamic Summaries**: Provides statistics and trends across multiple reports.
- **Error Handling**: Validates user inputs and handles errors gracefully.
- **Database Integration**: Uses SQLite and Flask-SQLAlchemy for storage and management.

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/Hussain1488/Computer_Program_Assignment.git
cd Computer_Program_Assignment
```

### Step 2: Create a Virtual Environment

```bash
run:
   python -m venv env
   source env/bin/activate  # On Windows, use: .\env\Scripts\activate
```

### Step 3: Install Dependencies

```bash
run:
   pip install -r requirements.txt
```

### Step 4: Initialize the Database

```bash
run:
   flask db init
   flask db migrate
   flask db upgrade
```

### Step 5: Run the Application

```bash
run:
   python app.py
```

### to run tailwindCss:

```bash
npx tailwindcss -i ./src/tailwind.css -o ./static/style/tailwind.css --watch
```
