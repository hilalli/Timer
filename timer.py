import tkinter as tk
from tkinter import messagebox
import time
import winsound
from datetime import datetime, timedelta
import pytz

class TimerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Countdown Timer and Real Time in Turkiye")

        # Timer section
        self.label_minutes = tk.Label(master, text="Minutes:", font=("Arial", 14))
        self.label_minutes.pack()

        self.entry_minutes = tk.Entry(master, font=("Arial", 14), width=10)
        self.entry_minutes.pack(pady=10)
        self.entry_minutes.bind('<Return>', lambda event: self.start_timer())  # Bind Enter key to start_timer()

        self.label_timer = tk.Label(master, text="", font=("Arial", 36))
        self.label_timer.pack(pady=20)

        self.start_button = tk.Button(master, text="Start", command=self.start_timer)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(master, text="Stop", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.restart_button = tk.Button(master, text="Restart", command=self.restart_timer, state=tk.DISABLED)
        self.restart_button.pack(pady=10)

        self.running = False
        self.remaining_time = 0
        self.update_timer()

        # Istanbul time section
        self.label_istanbul_time = tk.Label(master, text="Real Time in Turkiye:", font=("Arial", 14))
        self.label_istanbul_time.pack()

        self.label_current_time = tk.Label(master, text="", font=("Arial", 20))
        self.label_current_time.pack()

        self.update_istanbul_time()

    def start_timer(self):
        try:
            minutes = int(self.entry_minutes.get())
            if minutes <= 0:
                messagebox.showerror("Error", "Please enter a positive number of minutes.")
                return
            self.remaining_time = minutes * 60
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.restart_button.config(state=tk.DISABLED)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of minutes.")

    def stop_timer(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.restart_button.config(state=tk.NORMAL)

    def restart_timer(self):
        self.stop_timer()
        self.label_timer.config(text="")
        self.entry_minutes.delete(0, tk.END)
        self.restart_button.config(state=tk.DISABLED)

    def update_timer(self):
        if self.running and self.remaining_time > 0:
            minutes, seconds = divmod(self.remaining_time, 60)
            self.label_timer.config(text=f"{minutes:02}:{seconds:02}")
            self.remaining_time -= 1
        elif self.running and self.remaining_time == 0:
            self.label_timer.config(text="Time's up!")
            self.running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.restart_button.config(state=tk.NORMAL)
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)  # Play system default sound notification
        self.master.after(1000, self.update_timer)

    def update_istanbul_time(self):
        istanbul_timezone = pytz.timezone('Europe/Istanbul')
        istanbul_time = datetime.now(istanbul_timezone)
        istanbul_time_str = istanbul_time.strftime("%Y-%m-%d %H:%M:%S")
        self.label_current_time.config(text=istanbul_time_str)
        self.master.after(1000, self.update_istanbul_time)

# Creating the main application window
root = tk.Tk()
app = TimerApp(root)

# Running the main event loop
root.mainloop()
