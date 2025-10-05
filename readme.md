# DevOps Roadmap Tracker

A **Tkinter-based desktop application** to track your DevOps learning roadmap.  
This app helps you:

- Track daily tasks from a roadmap CSV.
- Mark tasks as complete.
- View completed tasks in a separate scrollable container.
- Visualize your **streak** for consecutive days completed (GitHub-style heatmap covering 8 months).
- View a **progress dashboard** with percentage completed, tasks left, current streak, and max streak.
- Works fully offline with **progress saved in `progress.json`**.
- Optional daily notifications using `script.py`.

---

## Features

1. **All Tasks Container**
   - Scrollable list of all tasks from `roadmap.csv`.
   - “Mark Complete” button for each task.
   - Marks completion in `progress.json`.

2. **Completed Tasks Container**
   - Scrollable list showing tasks completed today.
   - Updates dynamically.

3. **Dashboard**
   - Progress bar with percentage.
   - Tasks completed vs tasks left.
   - Current streak and max streak.
   - **8-month GitHub-style streak heatmap** starting top-left.

4. **Notifications**
   - Optional script to notify you about tasks pending or completed today.

---

## Requirements

- Python 3.7+
- Packages:
  ```bash
  pip install pandas plyer

- Tkinter comes with Python standard library.

---
