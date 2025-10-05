import tkinter as tk
from tkinter import ttk
import pandas as pd
import json
from datetime import date, timedelta
import os

# --- Files ---
CSV_FILE = "roadmap.csv"
JSON_FILE = "progress.json"

# --- Load CSV ---
tasks_df = pd.read_csv(CSV_FILE)

# --- Load or init progress.json ---
if os.path.exists(JSON_FILE):
    with open(JSON_FILE, "r") as f:
        progress = json.load(f)
else:
    progress = {
        "dates": [{str(date.today() + timedelta(days=i)): [] for i in range(len(tasks_df))}],
        "streak": 0,
        "start_date": str(date.today())
    }
    with open(JSON_FILE, "w") as f:
        json.dump(progress, f, indent=4)

# --- Tkinter root ---
root = tk.Tk()
root.title("DevOps Roadmap Tracker")
root.geometry("1200x700")
root.configure(bg="#1e1e1e")

# --- Styles ---
style = ttk.Style()
style.theme_use('clam')
style.configure("TLabel", background="#1e1e1e", foreground="#ffffff", font=("Arial", 12))
style.configure("TButton", font=("Arial", 10, "bold"))
style.configure("TProgressbar", troughcolor="#2d2d2d", background="#4ade80", thickness=30)

# --- Frames ---
frame_completed = tk.Frame(root, bg="#2d2d2d", bd=2, relief="groove")
frame_dashboard = tk.Frame(root, bg="#2d2d2d", bd=2, relief="groove")
frame_all = tk.Frame(root, bg="#2d2d2d", bd=2, relief="groove")

frame_completed.place(relx=0.01, rely=0.01, relwidth=0.32, relheight=0.97)
frame_dashboard.place(relx=0.34, rely=0.01, relwidth=0.32, relheight=0.97)
frame_all.place(relx=0.67, rely=0.01, relwidth=0.32, relheight=0.97)

# --- Scrollable Frame class ---
class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, bg="#2d2d2d", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas, style="TFrame")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel only when hovering
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", lambda ev: canvas.yview_scroll(int(-1*(ev.delta/120)), "units")))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

# --- Scrollable containers ---
scrollable_all_frame = ScrollableFrame(frame_all)
scrollable_completed_frame = ScrollableFrame(frame_completed)
scrollable_all = scrollable_all_frame.scrollable_frame
scrollable_completed = scrollable_completed_frame.scrollable_frame
scrollable_all_frame.pack(fill="both", expand=True)
scrollable_completed_frame.pack(fill="both", expand=True)

# --- Dashboard ---
tk.Label(frame_dashboard, text="Dashboard", font=("Arial", 16, "bold"), bg="#2d2d2d", fg="#ffffff").pack(pady=10)
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(frame_dashboard, maximum=100, variable=progress_var, length=250, style="TProgressbar")
progress_bar.pack(pady=10)
progress_label = tk.Label(frame_dashboard, text="0%", bg="#2d2d2d", fg="#ffffff", font=("Arial", 12, "bold"))
progress_label.pack()
tasks_completed_label = tk.Label(frame_dashboard, text="Tasks Completed: 0", bg="#2d2d2d", fg="#ffffff")
tasks_completed_label.pack(pady=5)
tasks_left_label = tk.Label(frame_dashboard, text="Tasks Left: 0", bg="#2d2d2d", fg="#ffffff")
tasks_left_label.pack(pady=5)

streak_label = tk.Label(frame_dashboard, text="Current Streak: 0 | Max Streak: 0", bg="#2d2d2d", fg="#4ade80", font=("Arial", 12, "bold"))
streak_label.pack(pady=10)

canvas_streak = tk.Canvas(frame_dashboard, width=300, height=120, bg="#1e1e1e", highlightthickness=0)
canvas_streak.pack(pady=5)

# --- Functions ---
def save_progress():
    with open(JSON_FILE, "w") as f:
        json.dump(progress, f, indent=4)

def update_dashboard():
    today_str = str(date.today())
    completed = 0
    for idx, row in tasks_df.iterrows():
        if today_str in progress['dates'][0] and row['TaskId'] in progress['dates'][0][today_str]:
            completed +=1
    total = len(tasks_df)
    percent = round(completed/total*100,1)
    progress_var.set(percent)
    progress_label.config(text=f"{percent}%")
    tasks_completed_label.config(text=f"Tasks Completed: {completed}")
    tasks_left_label.config(text=f"Tasks Left: {total-completed}")
    update_streak()

def update_streak():
    today = date.today()
    # Get sorted list of completed dates
    dates_done = []
    for day_str, tasks in progress['dates'][0].items():
        if tasks:
            dates_done.append(date.fromisoformat(day_str))
    dates_done.sort()

    # Calculate current and max streak
    streak_count = 0
    max_streak = 0
    current_streak = 0
    previous = None
    for d in dates_done:
        if previous and (d - previous).days == 1:
            streak_count +=1
        else:
            streak_count = 1
        if streak_count > max_streak:
            max_streak = streak_count
        if d == today:
            current_streak = streak_count
        previous = d
    progress['streak'] = current_streak
    streak_label.config(text=f"Current Streak: {current_streak} | Max Streak: {max_streak}")
    draw_streak_graph(dates_done)
def draw_streak_graph(dates_done):
    canvas_streak.delete("all")
    canvas_width = int(canvas_streak.winfo_width())
    if canvas_width < 10:
        canvas_width = 600  # default width
    size = 12
    gap = 4
    cols = max((canvas_width + gap) // (size + gap), 1)  # how many boxes per row

    # Start 8 months ago
    start_day = date.today() - timedelta(days=240)
    end_day = date.today()
    total_days = (end_day - start_day).days + 1

    for idx in range(total_days):
        day = start_day + timedelta(days=idx)
        row = idx // cols
        col = idx % cols
        x0 = col*(size+gap)
        y0 = row*(size+gap)
        x1 = x0 + size
        y1 = y0 + size
        color = "#4ade80" if day in dates_done else "#555555"
        outline = "#ffffff" if day == end_day else "#333333"
        canvas_streak.create_rectangle(x0, y0, x1, y1, fill=color, outline=outline)


def mark_complete(task_id):
    today_str = str(date.today())
    if today_str not in progress['dates'][0]:
        progress['dates'][0][today_str] = []
    if task_id not in progress['dates'][0][today_str]:
        progress['dates'][0][today_str].append(task_id)
    save_progress()
    refresh_tasks()

def refresh_tasks():
    for widget in scrollable_all.winfo_children():
        widget.destroy()
    for widget in scrollable_completed.winfo_children():
        widget.destroy()

    today_str = str(date.today())
    for idx, row in tasks_df.iterrows():
        # All Tasks
        frame = tk.Frame(scrollable_all, bg="#3d3d3d", pady=5)
        frame.pack(fill="x", padx=5, pady=2)
        tk.Label(frame, text=row['Task'], bg="#3d3d3d", fg="#ffffff", wraplength=200, justify="left").pack(side="left", padx=5)
        if today_str in progress['dates'][0] and row['TaskId'] in progress['dates'][0][today_str]:
            tk.Label(frame, text="✅", bg="#3d3d3d", fg="green", font=("Arial",12,"bold")).pack(side="right", padx=5)
        else:
            tk.Button(frame, text="Mark Complete", bg="#4ade80", fg="#1e1e1e", command=lambda tid=row['TaskId']: mark_complete(tid)).pack(side="right", padx=5)

        # Completed Tasks
        if today_str in progress['dates'][0] and row['TaskId'] in progress['dates'][0][today_str]:
            frame_c = tk.Frame(scrollable_completed, bg="#3d3d3d", pady=5)
            frame_c.pack(fill="x", padx=5, pady=2)
            tk.Label(frame_c, text=row['Task'], bg="#3d3d3d", fg="#4ade80", wraplength=200, justify="left").pack(side="left", padx=5)

    update_dashboard()

# --- Initialize ---
refresh_tasks()
root.mainloop()
